FROM python:3.7

EXPOSE 80

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
WORKDIR /
CMD python -m app
