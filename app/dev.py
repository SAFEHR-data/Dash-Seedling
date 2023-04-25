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
import struct


def db_aad_token_struct() -> bytes:
    """
    Uses AzureCli login state to get a token for the database scope

    Kindly leveraged from this SO answer: https://stackoverflow.com/a/67692382
    """
    from azure.identity import DefaultAzureCredential

    credential = DefaultAzureCredential()
    token = credential.get_token("https://database.windows.net/")[0]

    token_bytes = bytes(token, "UTF-16 LE")

    return struct.pack("=i", len(token_bytes)) + token_bytes
