FROM python:3.7.3-slim-stretch

WORKDIR /app

RUN apt-get update

## Setup gcc for typed-ast which mypy depends on
RUN apt-get install -y \
        build-essential \
        gcc

## Setup antlr - https://github.com/puckel/docker-airflow/issues/182#issuecomment-444683455
RUN mkdir -p /usr/share/man/man1 \
    && apt-get install curl -y openjdk-8-jre \
    && curl https://www.antlr.org/download/antlr-4.7.2-complete.jar -o /usr/local/lib/antlr-4.7.2-complete.jar \
    && echo "java -Xmx500M -cp \"/usr/local/lib/antlr-4.7.2-complete.jar:$CLASSPATH\" org.antlr.v4.Tool \$@" >> /usr/local/bin/antlr4 \
    && chmod u+x /usr/local/bin/antlr4

## Ensure wabt tools are installed, these are used during the python tests for now to ensure valid wat files are created
RUN curl -s -L https://github.com/WebAssembly/wabt/releases/download/1.0.11/wabt-1.0.11-linux.tar.gz | tar xvz \
    && mv ./wabt-1.0.11/* /usr/local/bin \
    && rm -rf wabt-1.0.11

## Install python dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --dev --ignore-pipfile --system

COPY . .
