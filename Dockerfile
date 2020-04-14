# Run once.
FROM python:3.8-buster
ENV PYTHONUNBUFFERED TRUE
WORKDIR /var/www/pyarcade
ENV PYTHONPATH "${PYTHONPATH}:$pwd"

# Run sometimes.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run always.
COPY . .
CMD python3 ./pyarcade/start.py
