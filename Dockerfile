FROM python:3.6

RUN apt-get update && \
    apt-get -y install mc && \
    apt-get update && \
    apt-get install -y curl && \
    cd /usr/local/bin && curl https://getmic.ro | bash && \
    apt-get install tk-dev -y && \
    apt-get install python3-tk -y

WORKDIR /code

ADD . /code

RUN pip install -r requirements.txt

CMD python run.py