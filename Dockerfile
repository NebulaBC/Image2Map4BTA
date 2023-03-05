FROM python:latest
COPY backend ./backend
WORKDIR backend
RUN pip install -r requirements.txt

CMD gunicorn -w 2 -b 0.0.0.0:8000 app:app
