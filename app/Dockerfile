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

FROM python:3.10.10-bullseye

# Create and run commands in /app inside the container
WORKDIR /app

# Install the azure cli
RUN apt-get update \
    && apt-get -y --no-install-recommends install ca-certificates curl apt-transport-https lsb-release gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -sLS https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /etc/apt/keyrings/microsoft.gpg > /dev/null \
    && chmod go+r /etc/apt/keyrings/microsoft.gpg \
    && AZ_REPO=$(lsb_release -cs) \
    && echo "deb [arch=`dpkg --print-architecture` signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" | \
    tee /etc/apt/sources.list.d/azure-cli.list \
    && apt-get update \
    && apt-get -y --no-install-recommends install azure-cli

# Install the odbc Drivers to access the database
RUN apt-get update \
    && apt-get install -y --no-install-recommends locales apt-transport-https \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list \
        > /etc/apt/sources.list.d/mssql-release.list \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen \
    && apt-get update \
    && apt-get -y --no-install-recommends install unixodbc-dev libodbc1 \
    && ACCEPT_EULA=Y apt-get -y --no-install-recommends install msodbcsql18

# Get requirements for pip install
COPY requirements.txt /app/

# Install the Python dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Create and use a non-root user
RUN useradd -m appUser
USER appUser

# Copy the required files into the working directory
COPY . /app/

# Serve the app on port 8000
CMD gunicorn --bind 0.0.0.0:8000 app:server
