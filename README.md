# Lab 1
## C 
Nombre décimaux aléatoires, générés entre 0 et 100. 10000 itérations, sous VSC, sur un Ubuntu 
=> Vrai envrion 75% du temps 
### Python
Nombre décimaux aléatoires 10000 itérations sous VSC sur MAC
==> vrai à 82,54%


# Lab 2
## Dockerfile pour le C 
Build le docker file:
```
docker build -t tp1-c .
```
Le lancer, pour récupérer les fichiers dans TP1: 
```
docker run --rm -v "$(pwd)":/out tp1-c
```
