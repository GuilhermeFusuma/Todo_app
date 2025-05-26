from transformers import pipeline

from huggingface_hub import InferenceClient


# Cria um pipeline de geração de texto com um modelo leve
gerador = pipeline(
    "text2text-generation",
    model="EleutherAI/gpt-neo-1.3B"
)

def gerar_input_tarefa(descricao):
    prompt = f"""
You are a help bot for a Todo app, your job is to analyze the prompt of the user and based on that generate a response and generate a response based on that user's input.
analyze the following prompt and based on that check if the user wants you to create a task or not.
"{descricao}"
""" + """
answer in this format: 
response: "the answer that's going to be shown to the user",
create_task": True or False based on the user's prompt,
title: "Titulo",
deadline: "DD/MM/AAAA"
"""
    
    resposta = gerador(prompt, max_new_tokens=100)[0]['generated_text']
    return resposta

teste = input('teste: ')
result = gerar_input_tarefa(teste)

print("resultado: ", result)