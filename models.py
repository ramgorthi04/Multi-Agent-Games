from openai import OpenAI
import openai
import json
import time 
import os

def get_lepton_response(prompt, model="mistral-7b", json_mode = False, max_tokens=None):
    """Gets response from mistral-7b through lepton
    
    Model selection can be modified within the function. Currently uses Mistral-7B.
    
    Parameters
    ----------
    prompt
    model : str, defaults to "mistral-7b"
        Can also input "Wizardlm-2-8x22b"
    json_mode : boolean, defaults false
    
    Returns
    -------
    response as string
    """
    if (model == "mistral-7b"):
        model_url = "https://mistral-7b.lepton.run/api/v1/"
    if (model == "Wizardlm-2-8x22b"):
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

    if __debug__:
        print(f"Getting response from {model} with prompt: {prompt}")
    completion = client.chat.completions.create(**completion_args)


    response = ""
    for chunk in completion:
        if not chunk.choices:
            continue
        content = chunk.choices[0].delta.content
        if content:
            response = response + content
    return response


def get_gpt_response(prompt, gpt_model="gpt-4", json_mode=False, response_format=""):
    """Encapsulates GPT prompting
    User provides prompt and gets only the text of GPT response

    Parameters
    ----------
    prompt : str
    gpt_model : str, optional (default is "gpt-4")
        Can also input "gpt-3.5-turbo"
    response_format : str, optional
        Input "json" for json format
    Returns
    -------
    str
        text response returned by chat completion agent
    None
        if no response received by GPT
    """

    client = OpenAI(
        api_key=os.environ.get("openai_api_key"),
    )
    if response_format == "json": 
        response = client.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": prompt,
        }
        ],
        response_format={ "type": "json_object" },
        model=gpt_model,
        )
    else:
        response = client.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": prompt,
        }
        ],
        model=gpt_model,
        )
    if response.choices:
        response_text = response.choices[0].message.content
        return response_text
    else:
        return None
