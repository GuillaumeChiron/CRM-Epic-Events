import os

import sentry_sdk
from dotenv import load_dotenv

load_dotenv()


def init_sentry() -> None:
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
        traces_sample_rate=0,
        send_default_pii=False,
    )
