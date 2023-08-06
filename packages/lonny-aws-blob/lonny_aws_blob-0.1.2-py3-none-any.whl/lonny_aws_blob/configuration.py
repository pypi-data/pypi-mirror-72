import boto3

client_sdb = boto3.client("sdb")

class Configuration:
    domain = "lonny_aws_blob"
    sys_prefix = "sys"
    lock_retry_seconds = 2
    default_lock_stale_minutes = 5


def init():
    client_sdb.create_domain(
        DomainName = Configuration.domain
    )
