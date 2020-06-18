import typing

import boto3  # type: ignore
import botocore  # type: ignore
import pickle

T = typing.TypeVar("T")


class S3Client:
    def __init__(self) -> None:
        self.s3 = boto3.resource("s3")

    def _get_file_obj(self, bucket: str, key: str) -> typing.Any:
        return self.s3.Object(bucket, key)

    def _get_file_updated_at(self, bucket: str, key: str) -> typing.Optional[str]:
        try:
            return typing.cast(str, self._get_file_obj(bucket, key).last_modified)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return None
            else:
                raise

    def _get_file_contents(self, bucket: str, key: str) -> bytes:
        obj = self._get_file_obj(bucket, key)

        return typing.cast(bytes, obj.get()["Body"].read())

    def get_or_create_file(
        self, bucket: str, key: str, generator: typing.Callable[[], T]
    ) -> T:
        updated_at = self._get_file_updated_at(bucket, key)
        if updated_at:
            return typing.cast(
                T, pickle.loads(self._get_file_contents(bucket, key), encoding="str")
            )

        contents = generator()

        self._put_file_contents(bucket, key, pickle.dumps(contents))

        return contents

    def _put_file_contents(self, bucket: str, key: str, contents: bytes) -> None:
        try:
            self.s3.Object(bucket, key).put(Body=contents)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchBucket":
                self.s3.create_bucket(
                    Bucket=bucket,
                    CreateBucketConfiguration={"LocationConstraint": "us-west-2"},
                )
            else:
                raise

            self.s3.Object(bucket, key).put(Body=contents)
