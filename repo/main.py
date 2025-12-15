import json
import os

import hydra
import pandas as pd
import wandb
from omegaconf import DictConfig

from prompt_generation import generate_prompts
from prompt_generation import generate_prompts_chatgpt
from prompt_generation import generate_prompts_chatgpt_COT

from run_llm import run_llm
from run_llm import run_llm_chatGPT


def save_results(outputs, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for o in outputs:
        with open(os.path.join(output_folder, f'{o["name"]}.json'), 'w') as f:
            json.dump(o, f)


def save_results_wandb(outputs, args):
    wandb.init(config=args, project=args.wandb.project, entity=args.wandb.entity)
    outputs_df = pd.DataFrame(outputs)
    wandb.log({'result': outputs_df})


@hydra.main(version_base=None, config_path=".", config_name="config")
def main(cfg: DictConfig):
    dataset = pd.read_csv(cfg.input_output.csv)
    
    if True:
        prompts = generate_prompts(dataset, cfg.running_params.shots)
        outputs = run_llm(prompts, "", cfg.running_params.temperature,
                        cfg.running_params.max_tokens, cfg.running_params.top_p, cfg.running_params.frequency_penalty,
                        cfg.running_params.presence_penalty)
        
    elif cfg.running_params.llm == 'chatgpt':
        
        # Chain of Thought
        # 1 == use COT
        # 0 == not use COT
        COT = cfg.running_params.cot 
        
        if COT == 0:
            prompts = generate_prompts_chatgpt(dataset, cfg.running_params.shots)
        elif COT == 1:
            prompts = generate_prompts_chatgpt_COT(dataset, cfg.running_params.shots)
            
        outputs = run_llm_chatGPT(prompts, cfg.running_params.llm, cfg.running_params.temperature,
                        cfg.running_params.max_tokens, cfg.running_params.top_p, cfg.running_params.frequency_penalty,
                        cfg.running_params.presence_penalty)
         
        
    save_results(outputs, cfg.input_output.output_folder)

    if cfg.wandb.activate:
        save_results_wandb(outputs, cfg)


if __name__ == '__main__':
    main()
