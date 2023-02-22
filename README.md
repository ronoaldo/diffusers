# Running Stable Diffusion using HuggingFace Diffisuers on AMD GPUs

This is a simple script to help you get up and running with Stable Diffusion
models on you computer using AMD GPU, powered by ROCM project, from AMD.

The idea is to use a base container image produced by AMD, with the ROCM stack
installed, and then install the Python tools needed to run Stable Diffusion. The
helper script and Dockerfile allow one to build such a custom container and
eventually install other tools as needed.

After that, you can enter the container using an interactive command prompt, and
from there, execute Stable Diffusion inferences. There is a helper script that
acts as an CLI for the proccess.

## Executing the demo script

You need to have Docker installed on your host to get started, and a recent
Linux Kernel with updated AMD drivers and firmware. This was tested using Debian
11 + Kernel from Backports, and using Firmware from Debian Unstable.

To get started, it should be enough to just run:

    ./rocm-docker.sh

The script `rocm-docker.sh` will build the container and run the Bash prompt.
For the first time, it will download a lot of software that is required for the
GPU to work. After that, it will launch the container using the AMD recommended
configuration. Note here that we are exposing the hardware to the container and
some options may not be suited for a production setup, like
`seccomp=unconfined`. Exercise caution as to where you run this script, and to
what software you download into the container.

The script will also mount the root folder of this repository as a volume, so you
can retain some files outside of the container and do not need to redownload them
every time. Specifically, it will:

1. Use the /home/rocm-user/workspace path on the container to mount the volume.
2. Use the /home/rocm-user/workspace/huggingface path as the caching directory
   for the Diffusers file download.
3. Use the /home/rocm-user/workspace/output to save iamges from the demo Python
   script 

Make sure that you have enough disk space to run the python script. In my
testing it used around 5G of space for the model download cache.

After running rocm-docker.sh, you should be presented with the a bash prompt
like this:

    rocm-user@8c5dbe3e9d8a:~/workspace$

You can now run the demo script with:

    python3 ./stable-diffusion-v2-1.py

This script works as a shell prompt for generating images, and accepts
two special control prompts:

1. `seed=INTEGER_VALUE`: to set a custom seed; by default a random seed is
   create on startup and reused for all prompts.
2. `steps=INTEGER_VALUE`: to set the number of steps do execute, by default
   it will use 50.
3. `quit`: to finalize the session.

The script will display something like this after you start it up:

```
rocm-user@8c5dbe3e9d8a:~/workspace$ python3 stable-diffusion-v2-1.py 
Fetching 13 files: 100%|███████████████████████████████████████████████████████████████████████| 13/13 [00:00<00:00, 224386.63it/s]
/home/rocm-user/.local/lib/python3.8/site-packages/transformers/models/clip/feature_extraction_clip.py:28: FutureWarning: The class CLIPFeatureExtractor is deprecated and will be removed in version 5 of Transformers. Please use CLIPImageProcessor instead.
  warnings.warn(
stable-diffusion v2-1: seed=17186290256173197591, steps=50, type 'quit' to exit
diffuse>
```

The `diffuse>`  prompt is where you need to type your inference prompt. If you type
something like `a cat wearing a red hat near a penguim`, it should create something
like this:

```
diffuse> a cat wearing a red hat near a penguim
  0%|                                                                                                       | 0/50 [00:00<?, ?it/s]MIOpen(HIP): Warning [SQLiteBase] Missing system database file: gfx1030_36.kdb Performance may degrade. Please follow instructions to install: https://github.com/ROCmSoftwarePlatform/MIOpen#installing-miopen-kernels-package
100%|██████████████████████████████████████████████████████████████████████████████████████████████| 50/50 [01:49<00:00,  2.19s/it]
Result: StableDiffusionPipelineOutput(images=[<PIL.Image.Image image mode=RGB size=768x768 at 0x7F20A1A45FA0>], nsfw_content_detected=None)
Image saved at ./output/a-cat-wearing-a-red-hat-near-a-penguim_50_17186290256173197591.png
```

The file created can be viewed in your file explorer, under the `output` folder. For the
seed I used while writing this tutorial, this is what I got:

![Cat Image](./output/a-cat-wearing-a-red-hat-near-a-penguim_50_17186290256173197591.png)