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

PREFERRED_MODEL = "gnokit/improve-prompt:latest"
SYSTEM_MESSAGE = {
    '<prompt enhancement off>' : None,
    
    'terse' : """
Instructions:
- Enhance the human's prompt for text-to-image generation.
- Take the original prompt and add style, atmosphere and context.
- Return the enhanced prompt only without a label or explanation.
- Be concise.
- Do not use more than 20 words.
""",

    'medium' : """
Instructions:
- Enhance the human's prompt for text-to-image generation.
- Take the original prompt and add style, descriptive details, atmosphere and context.
- Return the enhanced prompt only without a label or explanation.
- Be moderately verbose.
- Do not use more than 40 words.
""",

    'baroque' : """
Instructions:
- Enhance the human's prompt for text-to-image generation.
- Using florid prose, enhance the original prompt and expand upon it, adding more descriptive details, sensory information, and context to create a vivid and compelling image.
- Return the enhanced prompt only without a label or explanation.
- Use flowery, verbose language.
- Do not use more than 100 words.
"""
}

ollama_settings = OllamaSettings()
error_message = ollama_settings.message
error_message = (
    error_message or f"To use this node, please run 'ollama pull {PREFERRED_MODEL}'"
    if not ollama_settings.models
    else ""
)
models = ollama_settings.models or ("None Installed",)
default_model = PREFERRED_MODEL if PREFERRED_MODEL in models else models[0]
verbosity_levels = tuple(SYSTEM_MESSAGE.keys())

@invocation_output("EnhancePromptOutput")
class EnhancePromptOutput(BaseInvocationOutput):
    """Enhanced prompt output"""

    enhanced_prompt: str = OutputField(
        default=None, description="The enhanced prompt string"
    )


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
    prompt: str = InputField(
        default=error_message,
        description="Image prompt",
        ui_component=UIComponent.Textarea,
    )
    model: Literal[models] = InputField(
        default=default_model,
        description="The Ollama model to use"
    )
    verbosity: Literal[verbosity_levels] = InputField(
        default='medium',
        description="The level of detail in the enhanced prompt",
    )
    offload_from_gpu: bool = InputField(
        default=True,
        description="Offload LLM after execution"
    )

    def invoke(self, context: InvocationContext) -> EnhancePromptOutput:
        user_input = self.prompt
        if not ollama_settings.models:
            return EnhancePromptOutput(enhanced_prompt=user_input)
        if not SYSTEM_MESSAGE[self.verbosity]:
            return EnhancePromptOutput(enhanced_prompt=user_input)

        kwargs: dict[str, str|int] = {"keep_alive": 0} if self.offload_from_gpu else {}
        kwargs["system"] = SYSTEM_MESSAGE[self.verbosity]
        llm = ollama_settings.get_model(model=self.model, **kwargs)
        response = llm.invoke(user_input)
        return EnhancePromptOutput(enhanced_prompt=response.strip())
