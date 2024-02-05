"""App"""

from flask import Flask

from app.api.router import router
from app.logger import logger, logger_handler
from app.services import pydantic_spec


def create_app() -> Flask:
    logger.info("--starting the app--")
    app = Flask(__name__)

    app.logger.addHandler(logger_handler)
    pydantic_spec.api_spec.register(app)

    app.register_blueprint(router)

    logger.info("--the app has started--")
    return app
