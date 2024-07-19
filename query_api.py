import requests

api_url = "https://NGROK_API_URL.ngrok-free.app/"

def query_llm(question):
    return requests.get(api_url, params={"question": question}).content.decode("utf-8")

# example
print(query_llm("How did discoveries in Discrete Mathematics contribute to Computer Science?"))
# -> 'Discrete Mathematics has made significant contributions to Computer Science.
#     It has been used to develop algorithms for sorting and searching algorithms, designing databases, and developing programming languages.
#     Discrete Mathematics has also been used to develop mathematical models for software engineering, software testing, and software verification.
#     Additionally, it has been used to develop mathematical tools for designing and analyzing computer networks.'
