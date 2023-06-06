FROM python:3.11
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY *.py /app/
COPY blueprints /app/blueprints
COPY static /app/static
COPY templates /app/templates
EXPOSE 80
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]