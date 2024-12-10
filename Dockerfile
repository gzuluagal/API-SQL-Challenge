FROM python:3.10

WORKDIR /API-SQL-Challenge


COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "src/main.py"]