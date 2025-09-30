FROM python:3

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt Django-question/
RUN pip install -r Django-question/requirements.txt

# copy project
COPY ./mysite Django-question/mysite

WORKDIR Django-question/mysite/