FROM pytorch/pytorch:1.9.1-cuda11.1-cudnn8-runtime
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]