"""Common Router"""

from flask import Blueprint

from app.api.v1.router import router as v1_router

router = Blueprint("api", __name__, url_prefix="/api")
router.register_blueprint(v1_router)
