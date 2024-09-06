# InvokeAI-Nodes

This repository contains workflow nodes designed to add features to
the [InvokeAI](https://invoke-ai.github.io/InvokeAI) text to image 
generator.

Currently this repo contains two nodes:
- [Enhance Prompt Node](#enhance-prompt-node) -- Use an LLM to make your simple prompts fancy
- [Describe Image Node](#describe-image-node) -- Use an LLM to describe the contents of an uploaded image

## Enhance Prompt Node

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

### Verbosity

The *Verbosity* menu has four levels:

* <prompt enhancement off>
* terse
* medium
* baroque

As its name implies, **<prompt enhancement off>** will disable prompt 
rewriting completely and pass through the prompt unchanged.

Using the recommended `gnokit/improve-prompt` model, the remaining
verbosity settings will have these effects:

**terse** will produce a concise prompt that adheres more strictly to
the input text. It may add backgrounds and styles if they were not
specified in the input prompt.

**medium** produces a longer prompt that adds whimsical details,
atmospheric descriptions, and other qualifiers.

**baroque** produces a long-winded prompt with florid, poetic, often
grandiose language that is equally likely to confuse or inspire the
downstream image generation. Be aware that the enhanced prompts
created with this setting will sometimes exceed the token limit.

Because we are working with a small LLM, this node will add another
source of variability to your images. You may wish to use a constant
random seed to the denoising step in order to see variation
originating from the prompt.

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
   
4. Download this repo and copy the directory `enhance_prompt` and its contents into the `nodes`
   directory of your InvokeAI root folder. It should look like this:
   ```
   INVOKEAI_ROOT
   ├── nodes
       ├── enhance_prompt
           ├── enhanceprompt.py
           ├── describeimage.py
           ├── common.py
           └── __init__.py

   ```
5. Restart InvokeAI to pick up the new node.

You'll now be able to search the workflow editor for an "Enhanced
Prompt". Select the LLM model you wish to use, type in a simple
prompt, and hook the node's Enhanced Prompt output to the Prompt input of 
a Prompt node as shown in the screencap above.

---

## Describe Image Node

The DescribeImage Invocation uses a local [Ollama](https://ollama.ai)
large language model server to describe the contents of any image. You can use
the output description as an input prompt, or modify it in some way.

In this screenshot, we've taken the picnicking bears image from the previous [Enhance Prompt](#enhance-prompt-node) example,
passed it through the Describe Image node, and then used the resulting description as an SDXL image generation prompt:

```
The image depicts a group of anthropomorphic bears dressed in clothing and accessories that resemble human summer
attire, gathered on a picnic blanket in a scenic outdoor setting. They are positioned as if sitting around a picnic,
with a basket of food, including sandwiches and fruit, placed in the center. The bears are various shades of brown
and have features such as ears, claws, and tails that distinguish them from humans. In the background, there is a
mountainous landscape under a clear blue sky. The scene conveys a sense of leisure and relaxation,
typical of a family picnic.
```

![image](https://github.com/user-attachments/assets/8daed3dc-d0b2-4d0e-945d-cedd169dabeb)

Only some Ollama models have computer vision abilities. The one I have used is [llava](https://ollama.com/library/llava). 
This LLM uses about 8 GB of VRAM, so I recommend to set the "Offload From Gpu" setting to True. This will load the 
LLM during image processing, and unload it before the next step in the workflow.

### Installation

It is assumed that you already have an Ollama server up and running on
the same system you run InvokeAI on.

1. Activate the InvokeAI virtual environment ("developer's console")
   using the `invoke.bat` script, or manually.
   
2. Install the `ollama` and `langchain-community` modules:
   ```
   pip install ollama langchain-community
   ```

3. Install the `llava` model:
   ```
   ollama pull llava
   ```
   
4. Download this repo and copy the directory `enhance_prompt` and its contents into the `nodes`
   directory of your InvokeAI root folder. It should look like this:
   ```
   INVOKEAI_ROOT
   ├── nodes
       ├── enhance_prompt
           ├── enhanceprompt.py
           ├── describeimage.py
           ├── common.py
           └── __init__.py

   ```
5. Restart InvokeAI to pick up the new node.

You'll now be able to search the workflow editor for the "Describe an Image" node. 
Select the LLM model you wish to use, upload an image file,
and hook the node's Description output to a Prompt node, or whatever you desire.


Copyright (c) 2024 Lincoln Stein. See [LICENSE]() for usage terms.
