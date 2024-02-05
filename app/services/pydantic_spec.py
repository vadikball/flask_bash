"""Api Spec"""

from flask_pydantic_spec import FlaskPydanticSpec  # type: ignore

api_spec = FlaskPydanticSpec("flask", title="Example API", version="v1.0", path="doc")
