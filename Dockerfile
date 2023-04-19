FROM alpine

RUN curl -L "https://github.com/FairwindsOps/nova/releases/download/3.2.0/nova_3.2.0_linux_amd64.tar.gz" > nova.tar.gz && \
  tar -xvf nova.tar.gz && \
  mv nova /usr/local/bin/
