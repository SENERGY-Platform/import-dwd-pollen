FROM python:3.9

ADD . /opt/app
WORKDIR /opt/app
RUN pip install --no-cache-dir -r pip-requirements.txt
LABEL org.opencontainers.image.source https://github.com/SENERGY-Platform/import-dwd-pollen
CMD [ "python", "./main.py" ]
