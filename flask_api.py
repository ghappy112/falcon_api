from transformers import AutoTokenizer
import transformers
import torch
from langchain import HuggingFacePipeline, PromptTemplate,  LLMChain
from flask import Flask, request
from pyngrok import ngrok

# falcon 7B repo
model = "tiiuae/falcon-7b-instruct"

# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model, device_map="auto")

# Create a text generation pipeline
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    #torch_dtype=torch.float32,
    torch_dtype=torch.float16, # requires GPU
    max_length=2048,
    device_map="auto"
)

# write prompt template for llm
template = """
Respond to the following question with a helpful answer.
Question: {question}
Answer:"""

# create langchain llm
llm = HuggingFacePipeline(pipeline = pipeline, model_kwargs = {'temperature':0})

# create prompt template for llm
prompt = PromptTemplate(template=template, input_variables=["question"])

# create a lang chain
llm_chain = LLMChain(prompt=prompt, llm=llm)

# initialize flask app
app = Flask(__name__)

# API Request Function
@app.route("/", methods=["GET"])
def answer_question():
    return llm_chain.invoke(request.args.get("question"))["text"].strip()

# main method to create and run API
if __name__ == "__main__":

  ngrok.set_auth_token("NGROK Token")

  port = 80

  public_url = ngrok.connect(port)
  print(' * ngrok tunnel "{}" -> "http://127.0.0.1:{}/"'.format(public_url, port))

  app.config['BASE_URL'] = public_url

  app.run(port=port)
