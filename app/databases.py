import os
import logging
import pyodbc
from typing import Any
from datetime import datetime, timezone
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
import struct

environment = os.environ.get("ENVIRONMENT", default="dev")

def db_aad_token_struct() -> bytes:
    """
    Uses AzureCli login state to get a token for the database scope
    Used when running 'make serve-dev'.

    Kindly leveraged from this SO answer: https://stackoverflow.com/a/67692382
    """
    credential = DefaultAzureCredential()
    token = credential.get_token("https://database.windows.net/")[0]

    token_bytes = bytes(token, "UTF-16 LE")

    return struct.pack("=i", len(token_bytes)) + token_bytes

def odbc_cursor() -> Any:
    """
    ODBC cursor for running queries against the MSSQL feature store.

    Documentation: https://github.com/mkleehammer/pyodbc/wiki
    """

    connection_string = os.environ["FEATURE_STORE_CONNECTION_STRING"]

    if "authentication" not in connection_string.lower():
        SQL_COPT_SS_ACCESS_TOKEN = 1256
        attrs_before = {SQL_COPT_SS_ACCESS_TOKEN: db_aad_token_struct()}
    else:
        attrs_before = {}

    connection = pyodbc.connect(connection_string, attrs_before=attrs_before)
    cursor = connection.cursor()
    logging.info("ODBC connection cursor created.")
    return cursor


def cosmos_client() -> "CosmosClient":
    """
    CosmosDB client for connecting with the state store.

    Documentation: https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/sdk-python
    """

    client = CosmosClient(
        os.environ["COSMOSDB_ENDPOINT"],
        credential=(
            DefaultAzureCredential()
            if environment != "local"
            else os.environ["COSMOSDB_KEY"]
        ),
        connection_verify=(environment != "local"),
    )
    logging.info("Cosmos client created.")
    return client


class CosmosDBLongCallbackManager:
    '''
    Use CosmosDB as a cache. Takes inputs of 
        cosmos_client as above
        database_name
        container_name (created if does not exist)
        expiry time (in seconds)
        partition_key (optional; else "/Id").

    the "get" method retrieves the cached value 
    unless it is expired.

    the "set" method inputs a value to the cache
    '''
    def __init__(
        self,
        cosmos_client: CosmosClient,
        database_name: str,
        container_name: str,
        expire: int,
        partition_key: str = "/Id",
    ):
        self.client = cosmos_client
        self.database_name = database_name
        self.container_name = container_name
        self.expire = expire
        self.partition_key = partition_key


    def is_expired(self, item):
        if not item or "timestamp" not in item or "expire" not in item:
            return True
        timestamp = datetime.fromisoformat(item["timestamp"])
        expire_seconds = item["expire"]
        now = datetime.now(timezone.utc)
        seconds_since_timestamp = (now - timestamp).total_seconds()
        if seconds_since_timestamp > expire_seconds:
            logging.info(
                f"Now:{now}. timestamp: {timestamp}. seconds_since_stimestamp: {seconds_since_timestamp}"
            )
            return True
        return False

    def get_database_client(self):
        return self.client.get_database_client(self.database_name)

    def get_container_client(self):
        return self.get_database_client().get_container_client(self.container_name)

    def get(self, cache_key):
        container = self.get_container_client()
        query = f'SELECT * FROM c WHERE c.id = "{cache_key}"'
        items = list(container.query_items(query, enable_cross_partition_query=True))

        if not items:
            return None

        item = items[0]

        if self.is_expired(item):
            return None

        else:
            return item.get("value")

    def set(self, value, cache_key):
        container = self.get_container_client()
        if isinstance(value, datetime):
            value = value.isoformat()
        item = {
            "id": cache_key,
            "value": value,
            "expire": self.expire,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self.partition_key is not None:
            item[self.partition_key] = self.partition_key

        query = f'SELECT * FROM c WHERE c.id = "{cache_key}"'
        items = list(container.query_items(query, enable_cross_partition_query=True))

        if items:
            container.upsert_item(item)

        else:
            container.create_item(item)
