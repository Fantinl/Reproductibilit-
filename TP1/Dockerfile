FROM ubuntu:24.04
RUN apt-get update && apt-get install -y gcc
WORKDIR /TP1
COPY  banquier.c /TP1
COPY egal.c /TP1
RUN gcc -o egal egal.c 
RUN gcc -o banquier banquier.c
WORKDIR /out
CMD ["sh","-c", "/TP1/egal && /TP1/banquier" ]