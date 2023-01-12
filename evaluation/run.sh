#!/bin/bash

cuda=$1
# file_name=raw_files/wikitext103_gpt2_result_nucleus_sampling.json
file_name=raw_files/wikitext103_gpt2_result_greedy.json
# file_name=raw_files/en_wiki_copyisallyouneed_result_nucleus_sampling.json
# file_name=raw_files/wikitext103_neurlab_gpt2_result_nucleus_sampling_v2.json
# file_name=raw_files/en_wiki_knnlm_result_nucleus_sampling_full.json
# file_name=raw_files/en_wiki_knnlm_result_greedy_full.json
# file_name=raw_files/lawmt_gpt2_result_greedy_v2.json
# file_name=raw_files/en_wiki_gpt2_result_greedy_v2.json
# file_name=raw_files/en_wiki_gpt2_result_nucleus_sampling_v2.json

# coherence
CUDA_VISIBLE_DEVICES=$cuda python coherence/test.py --test_path $file_name

# mauve
# python mauve/test.py --test_path $file_name --device $cuda

# diversity
python diversity/test.py --test_path $file_name
