import logging
import sentry_sdk
from decouple import config
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration


logging.basicConfig(format="%(asctime)s - %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)
sentry_sdk.init(
    dsn=config("SENTRY_URL", default="https://foo@sentry.io/123"),
    integrations=[sentry_logging, AwsLambdaIntegration()],
)


def example(value_a, value_b):
    """
      This is an function example to run test
    """
    return value_a + value_b


def entrypoint_lambda(event=None, context=None):
    """
      This is an entrypoint to lambda
    """
    logger.info("Function default to run on aws")
    logger.info(f"Result sum(1,2) : {example(1,2)}")
