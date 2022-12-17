#!/bin/bash

# CUDA_VISIBLE_DEVICES=7 python gpt2_test.py --dataset en_wiki --model gpt2 --decoding_method greedy &
# CUDA_VISIBLE_DEVICES=6 python gpt2_test.py --dataset en_wiki --model gpt2 --decoding_method nucleus_sampling &

CUDA_VISIBLE_DEVICES=2 python gpt2_test.py --dataset en_wiki --model gpt2 --decoding_method greedy &
CUDA_VISIBLE_DEVICES=4 python gpt2_test.py --dataset en_wiki --model gpt2 --decoding_method nucleus_sampling &
