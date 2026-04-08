FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD bash -c "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8080 --server.address 0.0.0.0"