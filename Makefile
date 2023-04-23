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
# limitations under the License.
.PHONY: help

SHELL:=/bin/bash
MAKEFILE_FULLPATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MAKEFILE_DIR := $(dir $(MAKEFILE_FULLPATH))

target_title = @echo -e "🌱$(1)..."

define run  # Arguments: envrionment name, script path
	$(call target_title, "Running $(2) with envrionment=$(1)") \
	&& . ${MAKEFILE_DIR}/scripts/load_env.sh $(1) \
	&& ${MAKEFILE_DIR}/$(2)
endef

help: ## Show this help
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%s\033[0m|%s\n", $$1, $$2}' \
        | column -t -s '|'
	@echo

deploy: build ## Deploy this app
	$(call target_title, "Deploying") \
	&& . ${MAKEFILE_DIR}/scripts/load_env.sh \
	&& ${MAKEFILE_DIR}/scripts/deploy.sh

build:  ## Build the docker image
	$(call target_title, "Building") \
	&& . ${MAKEFILE_DIR}/scripts/load_env.sh \
	&& ${MAKEFILE_DIR}/scripts/build.sh

serve-local:  ## Serve the app locally with docker services
	$(call run,local,local/serve.sh)

stop-local:  ## Stop a locally running version
	$(call run,local,local/stop.sh)

serve-dev:  ## Serve the app locally with remote services
	$(call run,dev,scripts/serve_dev.sh)
