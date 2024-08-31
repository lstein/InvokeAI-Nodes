# Copyright (c) 2024 Lincoln D. Stein

from pydantic import BaseModel, Field, PrivateAttr
from typing import Tuple


class OllamaSettings(BaseModel):
    """Common configuration settings for Ollama"""

    prompt_prefix: str = Field(
        default="", description="Prompt prefix for this model's operation"
    )
    ollama_available: bool = Field(
        default=False, description="Is the Ollama module installed?"
    )
    langchain_available: bool = Field(
        default=False, description="Is Langchain community installed?"
    )
    models: Tuple[str] = Field(
        default_factory=tuple, description="List of Ollama model names"
    )
    message: str = Field(
        default="", description="An error message to display when a prereq is missing"
    )
    _ollama: type | None = PrivateAttr(default=None)

    def model_post_init(self, __context) -> None:
        try:
            import ollama

            self.ollama_available = True
        except ImportError:
            self.message += "To use this node, please run 'pip install ollama'"

        try:
            from langchain_community.llms import Ollama

            self._ollama = Ollama
            self.langchain_available = True
        except ImportError:
            self.message += (
                "\nTo use this node, please run 'pip install langchain-community'"
            )

        if not (self.ollama_available and self.langchain_available):
            return

        llms = ollama.list()
        self.models = tuple(sorted(model["name"] for model in llms["models"]))

    def get_model(self, model: str, **kwargs):
        return self._ollama(model=model, **kwargs)
