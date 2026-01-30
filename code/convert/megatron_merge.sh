# root directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../..

mca_path=$1
hf_path=$2

python scripts/megatron_merge.py \
  $mca_path \
  $hf_path \
  --bf16 \
  --convert_model_max_length 262144