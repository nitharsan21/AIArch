# run from root directory
# bash scripts/core/4_create_structure_dataset.sh

input_directory='./data/images/structure'
output_directory='./data/datasets/structure'
module='structure_plan'
step='generate_dataset'

python ./main/core.py \
  --module=$module \
  --step=$step \
  --input_directory=$input_directory \
  --output_directory=$output_directory
