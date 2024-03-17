import gspread
from openai import AsyncOpenAI
from pydantic import BaseModel
import json

from fastapi import FastAPI

app = FastAPI()

open_ai_key = ""

gc = gspread.service_account()

sh = gc.open("grokker-dataset")


class GrokPattern(BaseModel):
    pattern: str
    surity: float


class LogLine(BaseModel):
    text: str


def generate_prompt_v2(log_line: str) -> str:
    return f"""You are an expert software reliability engineer, right now you are writing a grok pattern for the given log line: {log_line}\n. You will first tokenize the log line by spaces and then write a grok pattern for all of the tokens. If you are not 100% sure about the grok pattern of a particular token you will give me choices in the json. The format of output should be this: 
    {{
        [
        {{ 
            "token": "token1",
            "choices": [
            "{{
                "pattern" : "pattern1",
                "confidence": "range from 0 to 1"
            }}
        ]
        }},
        ]
    }}
    """


def generate_prompt(log_line: str) -> str:
    return f"""You are an expert software reliability engineer, right now you are writing a grok pattern for the given log line: {log_line}\n.If you are not 100% sure about the grok pattern you will give me choices in the json. The format of output should be a json, there should not be any extra texts in the output. The output should be in this format, if this output is not being followed, the output will be considered as invalid.
    {{  
       [ 
        {{
                "pattern" : "pattern1",
                "confidence": "range from 0 to 1"
        }},
        {{
                "pattern" : "pattern2",
                "confidence": "range from 0 to 1"
        }},
        ]
    }}
    """


@app.get("/")
def read_root():
    return 'Grokker backend is up and running!'


@app.post("/grok")
async def get_grok_pattern_for_plain_text(log_line: LogLine):
    response_from_gpt = json.loads(await get_gpt_response(log_line.text))
    sh.sheet1.append_row([log_line.text, json.dumps(response_from_gpt)])
    return response_from_gpt


client = AsyncOpenAI(
    api_key=open_ai_key
)


async def get_gpt_response(log_line: str) -> str:
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": generate_prompt(log_line=log_line),
            }
        ],
        model="gpt-4",
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content
