from transformers import AutoTokenizer, AutoModelWithLMHead, pipeline
import torch
import requests
import json
from flask import (
  Flask, request, Response, render_template
)

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("ceostroff/harry-potter-gpt2-fanfiction")
model = AutoModelWithLMHead.from_pretrained("ceostroff/harry-potter-gpt2-fanfiction", pad_token_id=tokenizer.eos_token_id)
text_generation = pipeline("text-generation", model=model, tokenizer=tokenizer)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

AINIZE_STORY_GEN_URL = "https://feature-add-torch-serve-gpt-2-server-gkswjdzz.endpoint.ainize.ai"
AINIZE_STORY_GEN_URL_PARAM = "/infer/gpt2_story"

def generate(text, num_samples, length):
  try:
    text = text.strip()
    result = dict()
    result_list = text_generation(text, max_length=length, do_sample=True, num_return_sequences = num_samples)
    for idx, item in enumerate(result_list):
      result[idx] = item['generated_text']
    
    return result
  except Exception as e:
    raise Exception("Error")

@app.route("/gen-potter-fanfic", methods=['POST'])
def generate_porter_fanfiction():
  try:
    print(request.form)
    text = request.form['text']
    num_samples = request.form['num_samples']
    length = request.form['length']
  except Exception:
    return Response("Empty Field", status=400)
  
  try:
    result = generate(text, int(num_samples), int(length))

    return result
  except Exception:
    return Response("API Server Error", status = 500)

@app.route("/gen-story", methods=['POST'])
def generate_story():
  try:
    print(request.form)
    text = request.form['text']
    num_samples = request.form['num_samples']
    length = request.form['length']
  except Exception:
    return Response("Empty Field", status=400)
  
  url = AINIZE_STORY_GEN_URL + AINIZE_STORY_GEN_URL_PARAM
  headers = {
    "accept": "*/*",
    "Content-Type": "application/json",
  }
  data = {
    "text": text,
    "num_samples": int(num_samples),
    "length": len(text) + int(length),
  }

  response = requests.post(url, headers=headers, data=json.dumps(data))
  if response.status_code == 200:
    return response.json()
  elif response.status_code == 404:
    return Response("Model not Found", status=404)
  elif response.status_code == 500:
    return Response("Model Internal Server Error", status=500)
  elif response.status_code == 503:
    return Response("Not available to serve Request from Model Server", status=503)
  else:
    return Response("API Server Error", status=500)

@app.route("/")
def main():
  return render_template("index.html")

if __name__ == "__main__":  
  app.run(host="0.0.0.0", port="5000")