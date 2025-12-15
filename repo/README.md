# llm-model-generation

## Installation

Generation of the conda environment:
```shell
conda create -n llm-model-generation python=3.8
conda activate llm-model-generation
pip install -r requirements.txt
```

To use gpt-3/chatgpt, you have to add the Open AI token to an environment variable
```shell
export OPEN_AI_TOKEN=your_token
```

To use HuggingFace models (e.g., GPT-NEO), you have to add the HF token:
```shell
export HF_TOKEN=your_token
```

## Usage

Just run the following command:
```shell
python main.py
```

The default arguments are in `config.yaml`.

```yaml
wandb: # <- wandb stuff
  activate: False
  project: "llm-model-generation"
  entity: "" #TODO

input_output: # <- input csv and output folder
  csv: "test.csv"  # Note: when using Chain of thought prompt, you should put "models_cot.csv". Otherwise, ""models.csv". 
  output_folder: runs/${running_params.llm}

running_params: # <- params that establish the generation process
  cot: 0  # chain of thought, 0: not use chain of thought. 1: use chain of thought.
  shots: ["H2S"] # <- list of models (Names of the models). In the current setting, it is a one-shot prompt with H2S being the example in the prompt. You can make it two-shot by: shots: ["BTMS", "H2S-Short"]
# for the few shot. 
# Zero shot is supported by placing an empty list []
# If you want to use Chain of thought prompt, make sure csv: "models_cot.csv" and shots: ["H2S"], cot = 1
  llm: "gpt3" # <- name of the language model, currently gpt3, chatgpt, EleutherAI/gpt-neo-2.7B
  temperature: 0.5
  max_tokens: 2048
  top_p: 1
  frequency_penalty: 0
  presence_penalty: 0
```

Then you can simply then let gpt3 generate the result with one-shot prompt by using:
```shell
python main.py 
```


The arguments can be changed so easily. For instance, let's set another language model:
```shell
python main.py running_params.llm=EleutherAI/gpt-neo-2.7B
```