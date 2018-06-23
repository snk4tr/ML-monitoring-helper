FROM python

RUN apt-get update && \
     apt-get -y install mc

WORKDIR /code

ADD . /code

RUN pip install -r requirements.txt

CMD python run.py