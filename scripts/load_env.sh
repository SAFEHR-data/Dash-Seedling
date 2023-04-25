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

# Load envrionment variables. Usage: . load_env.sh dev

set -o errexit
set -o pipefail
set -o nounset

function export_addtional_env_vars_for_local_services(){
    echo "Exporting additional vars for emulated SQL server and CosmosDB"

    # Admin username and password for the SQL server. The username must be "sa"
    export LOCAL_MSSQL_USERNAME="sa"
    export LOCAL_MSSQL_PASSWORD="aStrongPa@sword"

    # See: https://learn.microsoft.com/en-us/azure/cosmos-db/docker-emulator-linux
    export LOCAL_COSMOS_IP_ADDRESS="`ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}' | head -n 1`"
}

function export_locally_defined_env(){
    set -a
    source "$ENVIRONMENT_FILEPATH"
    set +a
    echo "Exported environment variables in .env.$ENVIRONMENT"
}

if [[ $# -eq 0 ]] ; then
    echo "Expecting \$ENVIRONMENT to be set"
else
    export ENVIRONMENT="$1"
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ENVIRONMENT_FILEPATH="${SCRIPT_DIR}/../.env.$ENVIRONMENT" 

if [ -f "$ENVIRONMENT_FILEPATH" ]; then
    export_locally_defined_env
else
    echo "Running in CI. Expecting environment variables to be set"
    export LOCAL_IMAGE_NAME="app"
fi

if [ "$ENVIRONMENT"  == "local" ]; then
    export_addtional_env_vars_for_local_services
fi
