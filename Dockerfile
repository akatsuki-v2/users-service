FROM python:3.10

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scripts /scripts
RUN chmod u+x /scripts/*

COPY mount /srv/root
WORKDIR /srv/root

EXPOSE 80

CMD ["/scripts/bootstrap.sh"]
