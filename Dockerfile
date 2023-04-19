FROM python:3.11-alpine

# Install Nova
RUN apk --no-cache add curl
RUN curl -L "https://github.com/FairwindsOps/nova/releases/download/3.2.0/nova_3.2.0_linux_amd64.tar.gz" > nova.tar.gz && \
  tar -xvf nova.tar.gz && \
  mv nova /usr/local/bin/

# Install Nova Exporter
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY nova-exporter.py /
WORKDIR /

# Run it!
CMD ["python", "nova-exporter.py"]
EXPOSE 8000/tcp
