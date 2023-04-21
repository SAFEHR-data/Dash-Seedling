import logging
from typing import Optional

from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.trace import config_integration
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.trace.tracer import Tracer
from opencensus.ext.azure.common.protocol import Envelope

def telemetry_processor_callback_function(envelope: Envelope):
    envelope.tags['ai.cloud.role'] = 'model-api'
    

class ExceptionTracebackFilter(logging.Filter):
    """
    If a record contains 'exc_info', it will only show in the 'exceptions' section of Application Insights without showing
    in the 'traces' section. In order to show it also in the 'traces' section, we need another log that does not contain 'exc_info'.
    """
    def filter(self, record: logging.LogRecord):

        if record.exc_info:
            logger = logging.getLogger(record.name)
            _, exception_value, _ = record.exc_info
            message = f"{record.getMessage()}\nException message: '{exception_value}'"
            logger.log(record.levelno, message)

        return True


def initialize_logging(environment: str, logging_level: int, correlation_id: Optional[str] = None):
    """
    Adds the Application Insights handler for the root logger and sets the given logging level.
    Creates and returns a logger adapter that integrates the correlation ID, if given, to the log messages.

    :param logging_level: The logging level to set e.g., logging.WARNING.
    :param correlation_id: Optional. The correlation ID that is passed on to the operation_Id in App Insights. This is a unique ID that is assigned to every transaction/operation. So, when a transaction becomes distributed across multiple services, we can follow that transaction across different services using the logging information.
    :returns: A newly created logger adapter.
    """
    logger = logging.getLogger()

    try:
        # picks up os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"] automatically
        azurelog_handler = AzureLogHandler()
        azurelog_handler.add_telemetry_processor(telemetry_processor_callback_function)
        azurelog_handler.addFilter(ExceptionTracebackFilter())
        logger.addHandler(azurelog_handler)
    except ValueError as e:
        if environment == "local":
            logger.info(f"Application Insights logger handler not set.: {e}") 
        else:
            logger.error(f"Failed to set Application Insights logger handler: {e}")
            raise e 
        

    config_integration.trace_integrations(['logging'])
    logging.basicConfig(level=logging_level, format='%(asctime)s %(message)s')
    Tracer(sampler=AlwaysOnSampler())
    logger.setLevel(logging_level)

    extra = {}

    if correlation_id:
        extra = {'traceId': correlation_id}

    adapter = logging.LoggerAdapter(logger, extra)
    adapter.debug(f"Logger adapter initialized with extra: {extra}")
