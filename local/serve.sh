#!/bin/bash
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

set -o errexit
set -o pipefail
set -o nounset

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ARCHITECTURE=$(uname -m)

if [ "${ENVIRONMENT}" != "local" ]; then
    echo "\$ENVIRONMENT must be set to local in order to serve locally"
    exit 1
fi

if [ "${ARCHITECTURE}" == "arm64" ]; then
    echo "Serving locally is not supported on arm. CosmosDB docker container fails: https://github.com/Azure/azure-cosmos-db-emulator-docker/issues/54"
    exit 1
fi

docker compose -p "${APP_NAME}" -f "${SCRIPT_DIR}/docker-compose.yml" up --build -d

echo "Local stack created"
echo "App:          http://localhost:${LOCAL_APP_PORT}"
echo "SQL server:   host=localhost:${LOCAL_MSSQL_PORT} username=${LOCAL_MSSQL_USERNAME} password=${LOCAL_MSSQL_PASSWORD}"
echo "Check status: docker compose -p ${APP_NAME} ps"
