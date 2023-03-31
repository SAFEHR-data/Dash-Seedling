# 🌱 Dash-Seedling

Template repository for building [dash](https://dash.plotly.com/) apps on [FlowEHR](https://github.com/UCLH-Foundry/FlowEHR).

> **Warning**
> This repository is a _work in progress_. We're working towards a v0.1.0 release


## Deploying

### Locally

1. Configure the local configuration file
```
cp .env.sample .env
```

2. Run `make serve-local` to build the sample Dash Docker container and serve it locally

```
make serve-local
# ...
# App: http://localhost:8050
```

and stop with `make stop-local`.

> **Note**
> Local serving does not work on ARM, including Apple M chips.

### CI

Please contact a FlowEHR admin to deploy to the FlowEHR infrastructure where a 
managed repository will be created with credentials to deploy to the cloud.

To add runtime environment variables into your app follow the [example diff](https://github.com/UCLH-Foundry/Dash-Seedling/compare/335ba5c85d8ec9c1e1ecaf32d86fb1c9b96e37a4...15fa63f6f9a62bfece8f35b1ee5c321b3ce22973) to add a connection string stored as a GitHub secret or variable. This must be performed by a code owner.
