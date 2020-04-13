FROM python:3.8-buster
ENV PYTHONUNBUFFERED TRUE
WORKDIR /var/www/pyarcade
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python3 ./pyarcade/start.py
