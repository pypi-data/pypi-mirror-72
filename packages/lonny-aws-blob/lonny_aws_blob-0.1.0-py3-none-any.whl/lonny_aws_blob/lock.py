from .configuration import Configuration
from .logger import logger
from logging import DEBUG
from contextlib import contextmanager
from datetime import datetime, timedelta
import boto3
import botocore
import time

client_sdb = boto3.client("sdb")

CREATE_DT = "create_dt"
LOCK_PREFIX = f"{Configuration.sys_prefix}::lock::"
ERROR_CODE = "ConditionalCheckFailed"

def _format_timestamp(datetime):
    return datetime.strftime("%Y-%m-%d %H:%M:%S")

def purge_stale_locks(older_than = timedelta(minutes = Configuration.default_lock_stale_minutes), *, next_token = None):
    create_dt = _format_timestamp(datetime.utcnow() - older_than)
    output = client_sdb.select(
        SelectExpression = f"""
            select itemName() from {Configuration.domain}
            where itemName() like '{LOCK_PREFIX}%'
            and {CREATE_DT} < '{create_dt}'
        """,
        ConsistentRead = True,
        ** dict() if next_token is None else dict(NextToken = next_token)
    )

    next_token = output.get("NextToken")
    rows = output.get("Items", list())
    for row in rows:
        client_sdb.delete_attributes(
            DomainName = Configuration.domain,
            ItemName = row["Name"]
        )
        
    logger.info(f"Deleted {len(rows)} stale locks")
    if next_token is not None:
        purge_stale_locks(older_than, next_token = next_token)

class Lock:
    def __init__(self, name):
        self.name = f"{LOCK_PREFIX}{name}"

    def _log(self, level, msg):
        logger.log(level, f"Lock({self.name}): {msg}")

    def _acquire_lock(self):
        try:
            create_dt = _format_timestamp(datetime.utcnow())
            client_sdb.put_attributes(
                DomainName = Configuration.domain,
                ItemName = self.name,
                Attributes = [
                    dict(Name = CREATE_DT, Value = create_dt)
                ],
                Expected = dict(
                    Name = CREATE_DT,
                    Exists = False
                )
            )
        except botocore.exceptions.ClientError as err:
            if err.response["Error"]["Code"] == ERROR_CODE:
                return False
            raise
        return True

    def _release_lock(self):
        client_sdb.delete_attributes(
            DomainName = Configuration.domain,
            ItemName = self.name
        )

    @contextmanager
    def lock(self):
        try:
            transient_log = False
            while not self._acquire_lock():
                if not transient_log:
                    transient_log = True
                    self._log(DEBUG, "Failed to acquire lock. We will retry")
                time.sleep(Configuration.lock_retry_seconds)
            self._log(DEBUG, "Lock acquired")
            yield
        finally:
            self._log(DEBUG, "Lock yielded")
            self._release_lock()