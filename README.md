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
