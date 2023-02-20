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

FROM mcr.microsoft.com/mssql/server:2022-RTM-GDR1-ubuntu-20.04

COPY *.sh *.sql ./

ARG LOCAL_MSSQL_USERNAME
ARG LOCAL_MSSQL_PASSWORD

ENV ACCEPT_EULA "Y"
ENV SA_USERNAME ${LOCAL_MSSQL_USERNAME}
ENV SA_PASSWORD ${LOCAL_MSSQL_PASSWORD}
CMD ["./entrypoint.sh"]
