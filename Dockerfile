FROM python:3.6-jessie

WORKDIR /app/

RUN apt-get update && \
    apt-get install -y gcc apt-transport-https

COPY ./requirements.txt /app/requirements.txt

RUN pip install -U 'pip>=8' && \
    pip install --no-cache-dir -r requirements.txt

# Install the app
COPY . /app/

# Set Python-related environment variables to reduce annoying-ness
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

CMD /bin/bash
