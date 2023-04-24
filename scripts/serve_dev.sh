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

# Build in a subshell for the parent architecture
( 
    cd "$SCRIPT_DIR"/../app/
    docker build -t "$LOCAL_IMAGE_NAME" .
)

echo "Running $LOCAL_IMAGE_NAME container.."
echo "App:  http://localhost:${LOCAL_APP_PORT}"

# dot-files with quotes are not supported by docker. See: https://github.com/docker/cli/issues/3630
docker run \
    -p "${LOCAL_APP_PORT}:8000" \
    --mount type=bind,src="$SCRIPT_DIR"/../app,dst=/app \
    --mount type=bind,src="$HOME/.azure/",dst=/home/appUser/.azure/ \
    --env APPLICATIONINSIGHTS_CONNECTION_STRING \
    --env FEATURE_STORE_CONNECTION_STRING \
    --env COSMOSDB_ENDPOINT \
    --env DEBUG \
    "$LOCAL_IMAGE_NAME" \
    /bin/bash -c "python app.py"
