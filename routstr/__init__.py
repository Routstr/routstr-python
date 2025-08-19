import os
from .patch import patch_openai

# api key is not used for routstr, but it is required by openai
os.environ["OPENAI_API_KEY"] = "x-cashu"

__all__ = [
    "patch_openai",
]
