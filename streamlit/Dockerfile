FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install connexion[swagger-ui]

COPY config.ini .

COPY ./app/ ./

#CMD [ "python3", "./server.py" ]

CMD [ "streamlit", "run", "server.py" ]
