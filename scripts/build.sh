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

if [ "${ARCHITECTURE}" == "arm64" ]; then
    DOCKER_BUILD_COMMAND="docker buildx build --platform linux/amd64"
else
    DOCKER_BUILD_COMMAND="docker build"
fi

echo "Building ${LOCAL_IMAGE_NAME} for amd64..."

cd "${SCRIPT_DIR}/../app/"
eval "${DOCKER_BUILD_COMMAND} -t ${LOCAL_IMAGE_NAME} ."
cd -
