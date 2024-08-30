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

FIELD_VALUE = ""
PROMPT_PREFIX = "Rewrite this prompt to be suitable for a text-to-image generator. Return the rewritten prompt only:"
OLLAMA_AVAILABLE = False
LANGCHAIN_COMMUNITY_AVAILABLE = False
MODELS_AVAILABLE = False
PREFERRED_MODEL = 'gnokit/improve-prompt:latest'
OLLAMA_MODELS = ("None Installed",)
DEFAULT_MODEL = ""

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    FIELD_VALUE = "To use this node, please run 'pip install ollama'"

if OLLAMA_AVAILABLE:
    try:
        from langchain_community.llms import Ollama
        LANGCHAIN_COMMUNITY_AVAILABLE = True
    except ImportError:
        FIELD_VALUE = "To use this node, please run 'pip install langchain-community'"

if OLLAMA_AVAILABLE and LANGCHAIN_COMMUNITY_AVAILABLE:
    try:
        llms = ollama.list()
        OLLAMA_MODELS = tuple(sorted(model['name'] for model in llms['models']))
        if len(OLLAMA_MODELS) > 0:
            MODELS_AVAILABLE = True
            DEFAULT_MODEL = PREFERRED_MODEL if PREFERRED_MODEL in OLLAMA_MODELS else OLLAMA_MODELS[0]
        else:
            OLLAMA_MODELS = ("None Installed",)
            FIELD_VALUE = f"To use this node, please run 'ollama pull {PREFERRED_MODEL}'"
    except Exception as e:
        OLLAMA_MODELS = ("None Installed",)
        DEFAULT_PROMPT = "OLLAMA_MODELS'"
        FIELD_VALUE = f"To use this node, please run 'ollama pull {PREFERRED_MODEL}'"

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
    value: str = InputField(default=FIELD_VALUE, description="Image prompt", ui_component=UIComponent.Textarea)
    model: Literal[OLLAMA_MODELS] = InputField(default=DEFAULT_MODEL, description="The Ollama model to use")
    offload_from_gpu: bool = InputField(default=False, description="Offload LLM after execution")
    
    def invoke(self, context: InvocationContext) -> EnhancePromptOutput:
        if not MODELS_AVAILABLE:
            return EnhancePromptOutput(prompt="")

        kwargs = {'keep_alive': 0} if self.offload_from_gpu else {}
        llm = Ollama(model=self.model, **kwargs)
        user_input = self.value
        response = llm.invoke(PROMPT_PREFIX + user_input)
        return EnhancePromptOutput(value=response.strip())
