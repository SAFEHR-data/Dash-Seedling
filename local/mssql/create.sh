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

function server_is_initialising() {
    
    exit_code=$(/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -Q "SELECT 1" &> /dev/null ; echo $?)

    if [ $exit_code -ne 0 ]; then
        echo "Server is initalising"
        return 0
    else
        return 1
    fi
}

while server_is_initialising; do
    sleep 5
done

/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -d master -i create.sql
echo "Created database from create.sql"
