PROBLEM_STATEMENT = "Generate the lists of model classes and associations from a given description."

TASK_DESCRIPTION = """Create a class diagram for the following description by giving the enumerations, classes, and relationships using format:
Enumerations:
enumerationName(literals)
(there might be no or multiple enumerations)

Class:
className(attributeType attributeName (there might be multiple attributes))
(there might be multiple classes)

Relationships
mul1 class1 associate mul2 class2 (class1 and2 are classes above. mul1 and mul2 are one of the following options[0..*, 1, 0..1, 1..*])
(there might be multiple associations)

class1 inherit class2 (class1 and class2 are classes above)
(there might be multiple inheritance)

mul1 class1 contain mul2 class2 (class1 and2 are classes above. mul1 and mul2 are one of the following options[0..*, 1, 0..1, 1..*])
(there might be multiple composition)
"""

SEP = '###'


def generate_prompts(dataset, shots):
    descriptions = list(dataset[~dataset.Name.isin(shots)]["Description"])
    names = list(dataset[~dataset.Name.isin(shots)]["Name"])
    if shots:
        description_shots = list(dataset[dataset.Name.isin(shots)]["Description"])
        classes_shots = list(dataset[dataset.Name.isin(shots)]["Classes"])
        associations_shots = list(dataset[dataset.Name.isin(shots)]["Associations"])

        prompt_shots = []
        for description_shot, classes_shot, associations_shot in zip(description_shots, classes_shots,
                                                                     associations_shots):
            # ignore classes title since it's already in the input
            shot = f"Description: {description_shot}\n" \
                   f"\n{classes_shot}\n" \
                   f"Relationships:\n{associations_shot}\n" \
                   f"{SEP}"
            prompt_shots.append(shot)
        prompt_shots = '\n'.join(prompt_shots)
        header = PROBLEM_STATEMENT + '\n' + prompt_shots
    else:
        header = PROBLEM_STATEMENT + '\n' + TASK_DESCRIPTION

    prompt_list = []
    for i, d in zip(names, descriptions):
        prompt_string = f"{header}\n" \
                        f"Description: {d}\n" 
        prompt_list.append({"description": d,
                            "model": "llama3.2",
                            "prompt": prompt_string,
                            "system": "",
                            "stream": False,
                            "name": i})

    return prompt_list


def create_prompt_1shot(system_prompt, task_in_prompt, solution,  task_todo):
  messages=[
    {"role": "system", "content": f"{system_prompt}"},
    {"role": "user", "content": f"{task_in_prompt}"},
    {"role": "assistant", "content": f"{solution}"},
    {"role": "user", "content": f"{task_todo}"}
  ]
    
  return messages

#   messages=[
#     {"role": "system", "content": f"{system_prompt}"},
#     {"role": "user", "content": f"{task_in_prompt}"},
#     {"role": "assistant", "content": f"{solution}"},
#     {"role": "user", "content": f"{task_todo}"}
#   ]



def generate_prompts_chatgpt(dataset, shots):
    descriptions = list(dataset[~dataset.Name.isin(shots)]["Description"])
    names = list(dataset[~dataset.Name.isin(shots)]["Name"])
    if shots:
        description_shots = list(dataset[dataset.Name.isin(shots)]["Description"])
        classes_shots = list(dataset[dataset.Name.isin(shots)]["Classes"])
        associations_shots = list(dataset[dataset.Name.isin(shots)]["Associations"])

        # prompt_shots = []
        message = [
            {"role": "system", "content": f"{PROBLEM_STATEMENT}"},
            # {"role": "user", "content": f"{}"}    
        ]
        
        for description_shot, classes_shot, associations_shot in zip(description_shots, classes_shots,
                                                                     associations_shots):
            # ignore classes title since it's already in the input
            # shot = f"Description: {description_shot}\n" \
            #        f"\n{classes_shot}\n" \
            #        f"Relationships:\n{associations_shot}\n" \
            #        f"{SEP}"
            #  {"role": "assistant", "content": "Who won the world series in 2020?"},
            shot = {"role": "user", "content": f"Description: {description_shot}\n"}   
            shot_answer = {"role": "assistant", "content": f"{classes_shot} \n\n  Relationships:\n{associations_shot}\n\n"}
            # print("shot_answer:" type(shot_answer))
            message.append(shot)
            message.append(shot_answer)
            
        # prompt_shots = '\n'.join(prompt_shots)
        # header = PROBLEM_STATEMENT + '\n' + prompt_shots
        
    else:
        # header = PROBLEM_STATEMENT + '\n' + TASK_DESCRIPTION
        message = [
            {"role": "system", "content": f"{PROBLEM_STATEMENT}"},
            {"role": "user", "content": f"{TASK_DESCRIPTION}"}    
        ]
        

    prompt_list = []
    for i, d in zip(names, descriptions):
        
        task_todo =  {"role": "user", "content": f"{d}"}  
        
        prompt  = []
        prompt = prompt + message   
        
        prompt.append(task_todo)
                           
        prompt_list.append({"description": d,
                            "model": "llama3.2",
                            "prompt": prompt,
                            "system": "",
                            "stream": False,
                            "name": i})

    return prompt_list



def generate_prompts_chatgpt_COT(dataset, shots):
    descriptions = list(dataset[~dataset.Name.isin(shots)]["Description"])
    names = list(dataset[~dataset.Name.isin(shots)]["Name"])
    
    if shots:
        description_shots = list(dataset[dataset.Name.isin(shots)]["Description"])
        classes_shots = list(dataset[dataset.Name.isin(shots)]["Classes"])
        associations_shots = list(dataset[dataset.Name.isin(shots)]["Associations"])

        # prompt_shots = []
        message = [
            {"role": "system", "content": f"{PROBLEM_STATEMENT}"},
            # {"role": "user", "content": f"{}"}    
        ]
        
        for description_shot, classes_shot, associations_shot in zip(description_shots, classes_shots,
                                                                     associations_shots):
            # ignore classes title since it's already in the input
            # shot = f"Description: {description_shot}\n" \
            #        f"\n{classes_shot}\n" \
            #        f"Relationships:\n{associations_shot}\n" \
            #        f"{SEP}"
            
            shot = {"role": "user", "content": f"Description: {description_shot}\n"}    # COT only need description, no need to solution
            # shot_answer = {"role": "assistant", "content": f"{classes_shot} \n\n  Relationships:\n{associations_shot}\n\n"},
                   
            message.append(shot)  # only contain H2S COT
            # message.append(shot_answer)
        
    else:
        # header = PROBLEM_STATEMENT + '\n' + TASK_DESCRIPTION
        message = [
            {"role": "system", "content": f"{PROBLEM_STATEMENT}"},
            {"role": "user", "content": f"{TASK_DESCRIPTION}"}    
        ]
        

    prompt_list = []
    for i, d in zip(names, descriptions):
        task_todo =  {"role": "user", "content": f"{d}"}  
        prompt  = []
        prompt = prompt + message    
        prompt.append(task_todo)
                           
        prompt_list.append({"description": d,
                            "prompt": prompt,
                            "name": i})

    return prompt_list


if __name__ == "__main__":
    pass
