import pickle


def s3_cache(s3_client, bucket, key):
    def wrap(func):
        def wrapper(*args, **kwargs):
            updated_at = s3_client.get_file_updated_at(bucket, key)
            if updated_at:
                print('in here')
                return pickle.loads(s3_client.get_file_contents(bucket, key))

            print('out here')
            contents = func(*args, **kwargs)

            s3_client.put_file_contents(bucket, key, pickle.dumps(contents))

            return contents

        return wrapper

    return wrap
