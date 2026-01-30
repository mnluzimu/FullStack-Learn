git clone --depth 1 git@gitee.com:mnluzimu/LLaMA-Factory-WebGen-Agent2.git

conda create -p /mnt/cache/luzimu/code_agent/LLaMA-Factory-WebGen-Agent2/env/llama-factory python==3.11 -y
conda activate /mnt/cache/luzimu/code_agent/LLaMA-Factory-WebGen-Agent2/env/llama-factory

cd /mnt/cache/luzimu/code_agent/LLaMA-Factory-WebGen-Agent2

pip install -e ".[torch,metrics]" --no-build-isolation

pip install wandb

pip install -e ".[torch,metrics,deepspeed]" --no-build-isolation

# /mnt/cache/luzimu/code_agent/LLaMA-Factory-WebGen-Agent2/src_my/train/llama3_full_sft_single-node.sh works


# Need to install mcore_adapter for megatron training

pip install megatron-core
pip install "git+https://github.com/alibaba/roll.git#subdirectory=mcore_adapter"

# ValueError: apply_rope_fusion is not available. Please install TE >= 1.4 or Apex.
# Need to install either NVIDIA Transformer-Engine (TE) ≥ 1.4 or NVIDIA Apex (built with --cuda_ext).
# Try to install NVIDIA Transformer-Engine (TE) ≥ 1.4
# current image: lm4science-ccr/ubuntu22.04-cuda12.8-cudnn9:v1.0.0

# ①  activate the same virtual-env / conda-env in which you run LLaMA-Factory
# ②  remove any old copy
pip uninstall -y transformer_engine

# ③  clone and build
cd /mnt/cache/luzimu/code_agent
git clone https://github.com/NVIDIA/TransformerEngine.git
cd TransformerEngine

# If you have multiple GPUs or non-default CUDA install, point the build at it:
#   export CUDA_HOME=/usr/local/cuda-12.4          # adapt if needed
#   export TORCH_CUDA_ARCH_LIST="8.6;8.9;9.0"      # Ada / Hopper …

python -m pip install -v --no-build-isolation .

# seems to have failed with: ModuleNotFoundError: No module named 'pybind11'

# 2) Install all build-time prerequisites
pip install -U pip wheel setuptools
pip install ninja cmake pybind11               # ✹ the missing one
# If you also miss Cython:
pip install cython

# 3) Clean any half-finished build
rm -rf build dist *.egg-info

# 4) Re-run the build
python -m pip install -v --no-build-isolation .


# /mnt/cache/luzimu/code_agent/LLaMA-Factory-WebGen-Agent2/src_my/train/qwen3_coder_30b_full_single-node.sh now works

# Now start installing flash_attn

pip install flash-attn --no-build-isolation
# flash_attn seems not to have been used?

# Build apex
cd /mnt/cache/luzimu/code_agent
git clone https://github.com/NVIDIA/apex
cd apex

NVCC_APPEND_FLAGS="--threads 4" APEX_PARALLEL_BUILD=8 APEX_CPP_EXT=1 APEX_CUDA_EXT=1 pip install -v --no-build-isolation .

conda create -p /mnt/cache/luzimu/code_agent/LLaMA-Factory-WebGen-Agent2/env/llama-factory-fix --clone /mnt/cache/luzimu/code_agent/LLaMA-Factory-WebGen-Agent2/env/llama-factory

conda activate /mnt/cache/luzimu/code_agent/LLaMA-Factory-WebGen-Agent2/env/llama-factory-fix

jq -r '.git_sha' /mnt/cache/luzimu/code_agent/LLaMA-Factory-WebGen-Agent2/outs/mca/qwen3_coder_30b_full_fullstack-agent_nextjs-nestjs_977-681_new/checkpoint-700/iter_0000001/dist_optimizer/metadata.json

pip install megatron-core==0.3.0