FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY dbfakeapp.py /app/dbfakeapp.py

EXPOSE 8000

CMD ["uvicorn", "dbfakeapp:app", "--host", "0.0.0.0", "--port", "8000"]