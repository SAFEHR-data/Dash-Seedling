#  Copyright (c) University College London Hospitals NHS Foundation Trust
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
from dash import Dash, html, dcc
from typing import Any
import plotly.express as px
import pandas as pd

app = Dash(__name__)
server = app.server
environment = os.environ.get("ENVIRONMENT", default="dev")

df = pd.DataFrame({
    "Seeds": ["Hibiscus"],
    "Amount": [1],
})

fig = px.bar(df, x="Seeds", y="Amount", barmode="group")

app.layout = html.Div(children=[
    html.H1(children=f'Dash app'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


def odbc_cursor() -> Any:
    """
    ODBC cursor for running queries against the MSSQL feature store.

    Documentation: https://github.com/mkleehammer/pyodbc/wiki
    """
    import pyodbc

    connection = pyodbc.connect(os.environ["FEATURE_STORE_CONNECTION_STRING"])
    return connection.cursor()


def cosmos_client() -> "CosmosClient":
    """
    CosmosDB client for connecting with the state store.

    Documentation: https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/sdk-python
    """
    from azure.cosmos import CosmosClient
    from azure.identity import DefaultAzureCredential

    client = CosmosClient(
        os.environ["COSMOSDB_ENDPOINT"],
        credential=(DefaultAzureCredential() if environment != "local"
                    else os.environ["COSMOSDB_KEY"]),
        connection_verify=(environment != "local")
    )
    return client


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8000, debug=(environment == "local"))
