# Copyright (c) 2024 Lincoln D. Stein

from typing import Literal
from invokeai.invocation_api import (
    BaseInvocation,
    BaseInvocationOutput,
    InvocationContext,
    invocation,
    invocation_output,
    InputField,
    OutputField,
    UIComponent,
)
from .common import OllamaSettings

PREFERRED_MODEL = 'gnokit/improve-prompt:latest'

ollama_settings = OllamaSettings(prompt_prefix="Rewrite this prompt to be suitable for a text-to-image generator. Return the rewritten prompt only:")
error_message = ollama_settings.message
error_message = error_message or f"To use this node, please run 'ollama pull {PREFERRED_MODEL}'" if not ollama_settings.models else ''
models = ollama_settings.models or ("None Installed",)
default_model = PREFERRED_MODEL if PREFERRED_MODEL in models else models[0]
@invocation_output("EnhancePromptOutput")
class EnhancePromptOutput(BaseInvocationOutput):
    """Enhanced prompt output"""
    value: str = OutputField(default=None, description="The enhanced prompt string")

@invocation(
    "EnhancePromptInvocation",
    title="Enhance a prompt using a local LLM",
    tags=["prompt", "enhance", "improve", "ollama"],
    category="prompt",
    version="1.0.0",
)
class EnhancePromptInvocation(BaseInvocation):
    """Use the local Ollama model to enhance a prompt"""

    # Inputs
    value: str = InputField(default=error_message, description="Image prompt", ui_component=UIComponent.Textarea)
    model: Literal[models] = InputField(default=default_model, description="The Ollama model to use")
    offload_from_gpu: bool = InputField(default=False, description="Offload LLM after execution")
    
    def invoke(self, context: InvocationContext) -> EnhancePromptOutput:
        if not ollama_settings.models:
            return EnhancePromptOutput(prompt="")

        kwargs = {'keep_alive': 0} if self.offload_from_gpu else {}
        llm = ollama_settings.get_model(model=self.model, **kwargs)
        user_input = self.value
        response = llm.invoke(ollama_settings.prompt_prefix + user_input)
        return EnhancePromptOutput(value=response.strip())
