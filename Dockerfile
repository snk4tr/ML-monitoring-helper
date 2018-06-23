FROM python

WORKDIR /code

ADD . /code

RUN pip install -r requirements.txt

CMD python run.py