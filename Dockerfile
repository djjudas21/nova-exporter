FROM python:3.12-alpine

# Install Nova
RUN apk --no-cache add curl
RUN curl -L "https://github.com/FairwindsOps/nova/releases/download/v3.9.0/nova_3.9.0_linux_amd64.tar.gz" > nova.tar.gz && \
  tar -xvf nova.tar.gz && \
  mv nova /usr/local/bin/

# Install Nova Exporter
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY nova_exporter.py /
WORKDIR /

# Run it!
CMD ["python", "nova_exporter.py"]
EXPOSE 8000/tcp
