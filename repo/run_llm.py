import json
import os

import openai
import requests
from tqdm import tqdm

# openai.api_key = os.environ['OPEN_AI_TOKEN']
# HF_TOKEN = os.environ['HF_TOKEN']
GPT3_OPEN_AI_ENGINE = 'text-davinci-003'
CHAT_GPT_OPEN_AI_ENGINE = 'text-chat-davinci-002-20221122'
API_URL = "https://api-inference.huggingface.co/models"


def query_hf(payload, model, parameters=None, options={'use_cache': False}):
    response = requests.post("http://localhost:11434/api/generate", json=payload)

    if response.status_code == 200:
        return response.json()["response"]
    else:
        print(f"response: {response}")
        print(f"Error calling LLM: {response.status_code} {response.reason}")
        raise Exception


def run_llm(prompts, llm, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
    generated_texts = []
    if llm == 'gpt3' or llm == 'chatgpt':
        engine = GPT3_OPEN_AI_ENGINE if llm == 'gpt3' else CHAT_GPT_OPEN_AI_ENGINE
        for dic in tqdm(prompts, desc='Inference'):
            response = openai.Completion.create(
                engine=engine,
                prompt=dic["prompt"],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty
            )
            generated_text = response['choices'][0]['text']
            generated_texts.append({"description": dic["description"],
                                    "generated_text": generated_text,
                                    "name": dic["name"],
                                    "prompt": dic["prompt"]})
    else:
        for dic in tqdm(prompts, desc='Inference'):
            parameters = {
                "max_new_tokens": 250,
                # TODO max_new_tokens is harcoded
                # TODO we will have problems with the length of the input sequences
                "temperature": temperature,
                'end_sequence': "###"
                # TODO, this is also harcoded
                # TODO penalty, top_p, and other parameters
            }
            response = query_hf(payload=dic,
                                model=llm,
                                parameters=parameters,
                                options={'use_cache': False})

            # TODO here, the response also includes the prompt :(
            generated_texts.append({"description": dic["description"],
                                    "generated_text": response,
                                    "name": dic["name"],
                                    "prompt": dic["prompt"]})
    return generated_texts



def run_llm_chatGPT(prompts, llm, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
    generated_texts = []    
    # for dic in tqdm(prompts, desc='Inference'):
    #     print(dic['prompt'])
    #     return
    
    if llm == 'chatgpt':
        for dic in tqdm(prompts, desc='Inference'):            
            # for ele in dic['prompt']:
            #     print(str(ele))
            
            # return
            
            # see documentation at https://platform.openai.com/docs/guides/chat
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=dic['prompt']
            )

            generated_text = completion['choices'][0]['message']['content']
            generated_texts.append({"description": dic["description"],
                                    "generated_text": generated_text,
                                    "name": dic["name"],
                                    "prompt": str(dic["prompt"]) })
    else:
        for dic in tqdm(prompts, desc='Inference'):
            parameters = {
                "max_new_tokens": 250,
                # TODO max_new_tokens is harcoded
                # TODO we will have problems with the length of the input sequences
                "temperature": temperature,
                'end_sequence': "###"
                # TODO, this is also harcoded
                # TODO penalty, top_p, and other parameters
            }
            response = query_hf(payload=dic["prompt"],
                                model=llm,
                                parameters=parameters,
                                options={'use_cache': False})
            print("Response: ", response)
            print("Response: ", response)
            print("Response: ", response)
            # TODO here, the response also includes the prompt :(
            generated_texts.append({"description": dic["description"],
                                    "generated_text": response[0]['generated_text'][len(dic["prompt"]):],
                                    "name": dic["name"],
                                    "prompt": dic["prompt"]})
    return generated_texts


def test_chatgpt():

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "I am interested in the world series"},
                {"role": "assistant", "content": "Who won the world series in 2020?"},
                {"role": "user", "content": "Who won the world series in 2020?"},
                
            ]
        )

    return(completion)
    
  
if __name__=="__main__":        
    print(test_chatgpt()['choices'][0]['message']['content'])
    
