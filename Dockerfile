# use Python 3.8 as base image
FROM python:3.8

# set working directory
WORKDIR /app

# copy requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy app files
COPY app app

# set environment variables
ENV FLASK_APP=app/__init__.py
ENV FLASK_ENV=production
ENV SECRET_KEY=my-secret-key

# expose port 5000
EXPOSE 5000

# run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]