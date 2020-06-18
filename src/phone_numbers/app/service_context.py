from typing import NamedTuple

from phone_numbers.clients.s3 import S3Client


class Clients(NamedTuple):
    s3: S3Client


class ServiceContext(NamedTuple):
    clients: Clients


s3 = S3Client()


service_context = ServiceContext(clients=Clients(s3=s3))
