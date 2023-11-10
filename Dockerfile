FROM python:3.9-slim

RUN mkdir /rss-scrap

WORKDIR /rss-scrap

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["0.0.0.0:8000"]