# 🌱 Dash-Seedling

Template repository for building [dash](https://dash.plotly.com/) apps on [FlowEHR](https://github.com/UCLH-Foundry/FlowEHR).

> **Warning**
> This repository is a _work in progress_. We're working towards a v0.1.0 release


## Deploying

### Fully local

For debugging locally without any remote Azure services, Seedlings provide a basic Docker Compose file for mocking backend services. This is useful in the initial stages of bootstrapping your app.

1. Create and configure the local configuration file
```
cp .env.local.sample .env.local
```

2. Run `make serve-local` to build the sample Dash Docker container and serve it locally

```
make serve-local
# ...
# App: http://localhost:8050
```

and stop with `make stop-local`.

> **Note**
> Local serving does not work on ARM, including Apple M chips. We recommend using [GitHub Codespaces](https://github.com/features/codespaces) if local serving is required.

### Local with Azure services

When you want to test your app with services from a FlowEHR dev environment (including its synthetic feature data), you can contact your FlowEHR admin for the appropriate connection strings and provide them in the following steps:

1. Create and configure the configuration file, replacing `__CHANGE_ME__` with appropriate values
```
cp .env.dev.sample .env.dev
```

2. Run `az login` to login to the Azure CLI

3. Run `make serve-dev`

### CI

Please contact a FlowEHR admin to deploy to the FlowEHR infrastructure where a 
managed repository will be created with credentials to deploy to the cloud.
