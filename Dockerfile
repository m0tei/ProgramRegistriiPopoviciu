FROM python:3-alpine3.15
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
RUN Pip3 install gunicorn
EXPOSE 5000
ENV MONGO_HOST='localhost'
ENV FLASK_APP=app.py
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000","app:app"]
