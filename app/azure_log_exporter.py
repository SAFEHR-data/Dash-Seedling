import logging
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler

def setup_azurelog_exporter(environment: str, app: any, instrumentation_key: str):
    try:
        FlaskMiddleware(
            app,
            exporter=AzureExporter(connection_string=instrumentation_key),
            sampler=ProbabilitySampler(rate=1.0),
        )
        logging.info("Azure Log exporter initialised.")
    except Exception as e:
        if environment == "local":
            logging.info(f"Flask middleware - Azure Log Exporter not set.: {e}")
        else:
            logging.error(f"Failed to set Flask middleware - Azure Exporter: {e}")
            raise e
