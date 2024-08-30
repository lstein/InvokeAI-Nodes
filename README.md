# InvokeAI-Nodes

This repository contains workflow nodes designed to add features to
the [InvokeAI](https://invoke-ai.github.io/InvokeAI) text to image 
generator.

Currently this repo contains just one node, but may grow with time.

## Enhance Prompt for Ollama

The EnhancePrompt Invocation uses a local [Ollama](https://ollama.ai)
large language model server to enhance prompts by adding additional
qualifiers to a prompt provided by the user. For example:

Input Prompt:
```bears having a picnic```

Enhanced Prompt:
```
Realistic, whimsical picnic scene featuring playful bears basking in a
sun-drenched meadow, surrounded by vibrant wildflowers and lush
greenery. Bears are adorned with colorful picnic blankets, hats, and
sunglasses, indulging in a feast of fresh berries, nuts, and
honey. The sky is clear and blue, casting a warm glow over the scene.
```

![image](https://github.com/user-attachments/assets/18e2d03b-a419-4c8e-a5c9-982edf640d98)

It does this by passing the input prompt to an Ollama LLM server
running on the same server as InvokeAI with a prompt to "rewrite the
input in a for suitable for a text-to-image-generator." The rewritten
prompt can then be passed on to a Compel mode for positive or negative
text conditioning.

Although the node will work with any Ollama-compatible LLM, I 
recommend using
[gnokit/improve-prompt](https://ollama.com/gnokit/improve-prompt), a
small (2B parameter) model that was specifically trained for prompt
enhancement. Using this model will help avoid out of memory errors on
CUDA systems when Invoke and the Ollama server contend with each other
for VRAM.

Alternatively, if you find yourself getting OOM errors, you can enable
the "Offload From GPU" option, which will purge the LLM model from
VRAM immediately after running it. The only drawback of this it that
it will cause a small delay before image rendering starts.

### Installation

It is assumed that you already have an Ollama server up and running on
the same system you run InvokeAI on.

1. Activate the InvokeAI virtual environment ("developer's console")
   using the `invoke.bat` script, or manually.
   
2. Install the `ollama` and `langchain-community` modules:
   ```
   pip install ollama langchain-community
   ```

3. Install the `gnokit/improve-prompt` model:
   ```
   ollama pull gnokit/improve-prompt
   ```
   
4. Copy the directory `enhance_prompt` and its contents into the `nodes`
   directory of your InvokeAI root folder. It should look like this:
   ```
   INVOKEAI_ROOT
   ├── nodes
       ├── enhance_prompt
       │   ├── enhanceprompt.py
       │   └── __init__.py

   ```
5. Restart InvokeAI to pick up the new node.

You'll now be able to search the workflow editor for an "Enhanced
Prompt". Select the LLM model you wish to use, type in a simple
prompt, and hook the node's Value output to the Prompt input of 
a Prompt node as shown in the screencap above.

Have fun!

Copyright (c) 2024 Lincoln Stein. See [LICENSE] for usage terms.
