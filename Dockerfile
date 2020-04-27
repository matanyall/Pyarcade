# Run once.
FROM python:3.8-buster
ENV PYTHONUNBUFFERED TRUE

WORKDIR /home/root
RUN git clone -q https://github.com/vishnubob/wait-for-it.git
RUN cp wait-for-it/wait-for-it.sh /usr/bin

WORKDIR /var/www/pyarcade
ENV PYTHONPATH "${PYTHONPATH}:$pwd"

# Run sometimes.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run always.
COPY . .
CMD python3 ./pyarcade/start.py
