from openai import OpenAI
import openai
import os

def get_LM_response(prompt, model="mistral-7b", json_mode=False, max_tokens=None):
    if model.startswith('gpt'):
        return get_gpt_response(prompt, model)  
    if model == "mistral-7b":
        model_url = "https://mistral-7b.lepton.run/api/v1/"
    if model == "Wizardlm-2-8x22b":
        model_url = "https://wizardlm-2-8x22b.lepton.run/api/v1/"
    client = openai.OpenAI(
        base_url=model_url,
        api_key=os.environ.get('lepton_api_key')
    )

    completion_args = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }

    if json_mode:
        completion_args["response_format"] = {"type": "json_object"}
    if max_tokens:
        completion_args["max_tokens"] = max_tokens

    completion = client.chat.completions.create(**completion_args)

    response = ""
    for chunk in completion:
        if not chunk.choices:
            continue
        content = chunk.choices[0].delta.content
        if content:
            response += content
    return response

def get_gpt_response(prompt, gpt_model="gpt-4", json_mode=False, response_format=""):
    client = OpenAI(
        api_key=os.environ.get("openai_api_key"),
    )
    if response_format == "json": 
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            model=gpt_model,
        )
    else:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=gpt_model,
        )
    if response.choices:
        response_text = response.choices[0].message.content
        return response_text
    else:
        return None
    
if __name__ == "__main__":
    print(get_LM_response("What is the meaning of life?"))
