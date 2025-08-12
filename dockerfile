FROM nvidia/cuda:12.1-runtime

RUN apt-get update && apt-get install -y python3-pip git
RUN pip install torch --index-url https://download.pytorch.org/whl/cu121
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
