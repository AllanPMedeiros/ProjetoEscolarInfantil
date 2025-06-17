FROM python:3.9

WORKDIR /App

COPY App/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV PYTHONPATH=/App
ENV FLASK_ENV=development
ENV FLASK_APP=app:App

CMD ["python", "app.py"]