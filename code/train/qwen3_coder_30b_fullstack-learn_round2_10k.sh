# root directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../..

export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export TOKENIZERS_PARALLELISM=false

wandb login $WANDB_API_KEY

USE_MCA=1 NVTE_FLASH_ATTN=1 NNODES=$WORLD_SIZE NODE_RANK=$RANK MASTER_ADDR=$MASTER_ADDR MASTER_PORT=29500 llamafactory-cli train examples/megatron/qwen3_coder_30b_fullstack-learn_round2_10k.yaml