FROM python:3.10.9-slim AS builder
LABEL author="Deivison Marteleto<ddmarteleto@gmail.com>"

ARG USERNAME=build
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=America/Sao_Paulo

RUN apt-get update -y && apt upgrade -y \
    && apt-get install -y --no-install-recommends  gettext build-essential telnet mariadb-client libsnmp-dev   \
        libxml2-dev gcc python-dev libxslt1-dev libxslt1.1  snmp snmpd telnet sudo openssh-client\
        libmariadb3 libmariadb-dev && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Always set a working directory
WORKDIR /home/build/app

# Install Python deps
COPY requirements.txt .
RUN  pip install --no-cache-dir  -r requirements.txt && \
    chmod -R 755 /home/build/app

USER $USERNAME

EXPOSE 8000
