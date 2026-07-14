import os
from dotenv import load_dotenv
from groq import Groq
from app.llm.prompt import build_prompt
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")

)


def ask_llm(repository_report, user_question):
    final_prompt = build_prompt(repository_report, user_question)

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        temperature=0.1,
        messages=[
            {"role": "user", "content": final_prompt}
        ]
    )

    return completion.choices[0].message.content