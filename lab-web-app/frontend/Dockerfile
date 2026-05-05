FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY dbbasicapp.py /app/dbbasicapp.py

EXPOSE 8501

CMD ["streamlit", "run", "dbbasicapp.py", "--server.address=0.0.0.0", "--server.port=8501"]

