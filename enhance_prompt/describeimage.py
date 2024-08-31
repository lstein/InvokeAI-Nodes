# Copyright (c) 2024 Lincoln D. Stein

import base64
import io
from typing import Literal
from invokeai.invocation_api import (
    BaseInvocation,
    BaseInvocationOutput,
    InvocationContext,
    invocation,
    invocation_output,
    ImageField,
    InputField,
    OutputField,
)

from .common import OllamaSettings

PREFERRED_MODEL = "llava:latest"

ollama_settings = OllamaSettings(
    prompt_prefix="Summarize the contents of this image briefly."
)
error_message = ollama_settings.message
error_message = (
    error_message or f"To use this node, please run 'ollama pull {PREFERRED_MODEL}'"
    if not ollama_settings.models
    else "Ready"
)
models = ollama_settings.models or ("None Installed",)
default_model = PREFERRED_MODEL if PREFERRED_MODEL in models else models[0]


@invocation_output("DescribeImageOutput")
class DescribeImageOutput(BaseInvocationOutput):
    """Description of the image"""

    description: str = OutputField(default=None, description="Description of the image")


@invocation(
    "DescribeImage",
    title="Describe an image",
    tags=["image", "classification", "prompt", "ollama"],
    category="image",
    version="1.0.0",
)
class DescribeImageInvocation(BaseInvocation):
    """Use the local Ollama model to extract descriptive data from an image"""

    # Inputs
    image: ImageField = InputField(description="The image to describe")
    model: Literal[models] = InputField(
        default=default_model, description="The Ollama model to use"
    )
    offload_from_gpu: bool = InputField(
        default=False, description="Offload LLM after execution"
    )
    status_message: str = InputField(
        default=error_message, description="Status Messages"
    )

    def invoke(self, context: InvocationContext) -> DescribeImageOutput:
        if not ollama_settings.models:
            return DescribeImageOutput(value="")

        kwargs = {"keep_alive": 0} if self.offload_from_gpu else {}
        llm = ollama_settings.get_model(model=self.model, **kwargs)

        # convert the image into a PNG, base64 encode it, and convert to string
        image = context.images.get_pil(self.image.image_name)
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        image_data = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

        response = llm.invoke(
            ollama_settings.prompt_prefix,
            images=[
                image_data,
            ],
        )

        return DescribeImageOutput(description=response.strip())
