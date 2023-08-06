import boto3, json
from logging import DEBUG
from .lock import Lock
from .configuration import Configuration
from .logger import logger

BLOB_PREFIX = f"{Configuration.sys_prefix}::blob::"

client_sdb = boto3.client("sdb")

def query(selectors = dict(), *, next_token = None):
    predicates = [f"{k} = '{v}'" for k,v in selectors.items()]
    predicates.append(f"itemName() like '{BLOB_PREFIX}%'")
    output = client_sdb.select(
        SelectExpression = f"""
            select itemName() from {Configuration.domain}
            where {" and ".join(predicates)}
        """,
        ** dict() if next_token is None else dict(NextToken = next_token)
    )

    next_token = output.get("NextToken")
    rows = output.get("Items", list())
    for row in rows:
        name = row["Name"][len(BLOB_PREFIX):]
        yield Blob(name)
    logger.debug(f"Retrieved {len(rows)} blobs")
    if next_token is not None:
        for blob in query(selectors, next_token = next_token):
            yield blob

class Blob:
    def __init__(self, name):
        self.name = f"{BLOB_PREFIX}{name}"
        self._lock = Lock(self.name)

    def _log(self, level, msg):
        logger.log(level, f"Blob({self.name}): {msg}")

    def get(self):
        attrs = client_sdb.get_attributes(
            DomainName = Configuration.domain,
            ItemName = self.name,
            ConsistentRead = True
        ).get("Attributes", list())
        return { x["Name"] : x["Value"] for x in attrs }

    def atomic(self):
        return self._lock.lock()

    def update(self, ** kwargs):
        if len(kwargs) == 0:
            return
        self._log(DEBUG, f"Setting attributes: {json.dumps(kwargs)}")
        client_sdb.put_attributes(
            DomainName = Configuration.domain,
            ItemName = self.name,
            Attributes = [
                dict(Name = k, Value = v, Replace = True) for k,v in kwargs.items()
            ]
        )

    def destroy(self):
        self._log(DEBUG, "Deleting blob")
        client_sdb.delete_attributes(
            DomainName = Configuration.domain,
            ItemName = self.name
        )


    