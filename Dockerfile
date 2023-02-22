FROM rocm/rocm-terminal

ENV PATH=$PATH:/home/rocm-user/.local/bin

# Non-root user setup - need to add the group render(107)
USER root
RUN addgroup render --gid 107 && \
    adduser rocm-user render

# Libraries and tools
RUN apt-get update && \
    apt-get install \
        python3 python3-pip python3-venv \
        miopenkernels-gfx1030-36kdb -yq

# Setup HuggingFace/PyTorch/Model
WORKDIR /home/rocm-user
USER rocm-user
RUN pip3 install --user --upgrade pip && \
    pip3 install --user --upgrade torch torchvision torchaudio \
        --extra-index-url https://download.pytorch.org/whl/rocm5.2 && \
    pip3 install --user diffusers transformers scipy ftfy accelerate safetensors unidecode

# Entrypoint
ENTRYPOINT [ "bash" ]
