from header import *
from dataloader import *
from models import *
from config import *
import sys
sys.path.append('../data/')
from dpr_1024 import Retriever

def parser_args():
    parser = argparse.ArgumentParser(description='train parameters')
    parser.add_argument('--dataset', default='ecommerce', type=str)
    parser.add_argument('--model', type=str)
    parser.add_argument('--decoding_method', type=str)
    parser.add_argument('--recall_topk', type=int, default=20)
    return parser.parse_args()

def main_generation(**args):
    retriever = Retriever(f'../data/{args["dataset"]}_1024/base_data_128.txt', 200, f'../data/dpr_{args["dataset"]}_1024', 0)
    args['mode'] = 'test'
    config = load_config(args)
    args.update(config)
    agent = load_model(args)
    agent.load_model(f'{args["root_dir"]}/ckpt/wikitext103/copyisallyouneed/best_2003_400000.pt')
    print(f'[!] init model over')

    torch.manual_seed(1.0)
    torch.cuda.manual_seed_all(1.0)

    collection = []
    with open(f'../data/{args["dataset"]}_1024/test.txt') as f:
        # collect the valid prefixes
        texts = []
        for line in tqdm(f.readlines()):
            ids = agent.model.tokenizer.encode(line, add_special_tokens=False)
            # prefix contains 50% tokens
            prefix_length = len(ids) // 2
            prefix = ids[:prefix_length]
            reference = ids[prefix_length:]
            
            prefix = agent.model.tokenizer.decode(prefix)
            reference = agent.model.tokenizer.decode(reference)
            texts.append((prefix, reference))
        print(f'[!] collect {len(texts)} valid samples which have at least 32 tokens in prefix')
        for prefix, reference in tqdm(texts[:500]):
            text, candidates = agent.generate_one_sample(prefix, retriever, decoding_method=args["decoding_method"], top_k=0, top_p=0.95, temp=1.)
            collection.append({
                'prefix': prefix, 
                'reference': reference, 
                'text': text, 
                'phrases': candidates
            })
    return collection

if __name__ == "__main__":
    args = vars(parser_args())
    result = main_generation(**args)
    with open(f'{args["dataset"]}_copyisallyouneed_result_{args["decoding_method"]}_v2.json', 'w') as f:
        json.dump(result, f, indent=4)
