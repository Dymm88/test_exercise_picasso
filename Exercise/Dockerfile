FROM python:3.11
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
ENV DJANGO_SETTINGS_MODULE=Exercise.settings
EXPOSE 8000
CMD ["--bind", ":8000", "Exercise.wsgi:application"]