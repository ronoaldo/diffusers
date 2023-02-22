#!/bin/bash
set -e
set -x

IMAGE=ronoaldo/diffusers

BASEDIR="$(dirname $0)"
BASEDIR="$(readlink -f "$BASEDIR")"

docker build -t $IMAGE .

docker run \
	--rm \
	-it \
	--device=/dev/kfd \
	--device=/dev/dri \
	--shm-size 16G \
	--group-add video \
	--group-add render \
	--cap-add=SYS_PTRACE \
	--security-opt seccomp=unconfined \
	--workdir /home/rocm-user/workspace \
	-e HF_HOME=/home/rocm-user/workspace/huggingface \
	-v $BASEDIR:/home/rocm-user/workspace \
	$IMAGE
