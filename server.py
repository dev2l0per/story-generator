import requests
import json
from flask import (
  Flask, request, Response, render_template
)
app = Flask(__name__)

API_URL = "https://feature-add-torch-serve-gpt-2-server-gkswjdzz.endpoint.ainize.ai"
API_URL_PARAM = "/infer/gpt2_story"

@app.route("/gen-story", methods=['POST'])
def generate_story():
  try:
    text = request.form['text']
    num_samples = request.form['num_samples']
    length = request.form['length']
  except Exception:
    return Response("Empty Field", status=400)
  
  url = API_URL + API_URL_PARAM
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
  app.run(debug=True, host="0.0.0.0", port="1234")