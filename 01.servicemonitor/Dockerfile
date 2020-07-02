FROM python:3.8-slim-buster
ENV TZ=Asia/Shanghai
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]