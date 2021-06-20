FROM python:3-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY dsmr_exporter/dsmr_exporter.py .

CMD [ "python", "./dsmr_exporter.py" ]

