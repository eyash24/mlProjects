FROM python:3.8-slim-buster
WORKDIR /applicaton
COPY . /application

RUN apt update -y && apt install awscli -y
RUN pip freeze > requirements.txt
RUN pip install -r requirements.txt
CMD ["python3","application.py"]