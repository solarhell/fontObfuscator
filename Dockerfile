FROM python:latest

ENV TZ=Asia/Shanghai

WORKDIR /mycode

ADD . /mycode

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

EXPOSE 1323

CMD [ "python", "./src/web.py" ]
