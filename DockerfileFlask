FROM python:3-alpine3.15
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENV MONGO_HOST='localhost'
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]
