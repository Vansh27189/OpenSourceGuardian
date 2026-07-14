from app.services.repository_service import analyse_repo
from pprint import pprint
from app.llm.prompt import build_prompt
from app.llm.llm_client import ask_llm

url = input("Repository URL: ")

result = analyse_repo(url)

# pprint(result)
question = input("Ask a question about this repo: ")
answer = ask_llm(result["report"], question)
print(answer)

# print(build_prompt(result["report"],"is this repo safe"))