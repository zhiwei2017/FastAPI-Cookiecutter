{% if cookiecutter.use_oauth == "Yes" -%}
from .auth import AuthUser
{% endif %}