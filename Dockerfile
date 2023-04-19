from python:slim
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y gdal-bin
RUN python manage.py shell < mqtt/aysinc_functions/functions.py
CMD ["python", "manage.py", "runserver"]