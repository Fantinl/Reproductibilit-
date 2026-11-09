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

# Lab 3
## Part 1

| Program  | Répétitions   | Système exploitation | Librairie | Propriété | Résultat |
| ------- | ------------- | ---------- |---------- | ---------- |---------- |
| Python   | 10000 | MacOS 26 | random | Associativité |82,54 | 
| JavaScript (ChatGpt)  |10000  | MacOS 27 | random |Associativité| 74.82|
| Python (Gemini, Pro.1)   | 100000    | Ubuntu | NumpyPy |Associativité| 82,75 |
| Python | 10000 | Ubuntu | random | Distributivité | 64,9 | 

## Parts 4 à 7 : modèle, échantillonnage, expériences

### Organisation

```
fm/experiment.uvl          feature model des facteurs de variabilité (48 configurations)
configs/*.csvconf          nos programmes (Labs 1 et 2) exprimés comme configurations
configs/sample.csv         échantillon : 4 programmes + 30 configurations tirées (seed 1)
sample.py                  script d'échantillonnage fourni (flamapy)
templates/assoc.py.jinja   template Python : propriété, librairie et répétitions sont des trous
run.py                     dérive, lance (5 fois) et enregistre chaque configuration
results/results_<OS>.csv   résultats : une ligne par exécution, facteurs + pourcentage + environnement
```

### Reproduire

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python sample.py fm/experiment.uvl --size 30 --seed 1 --include configs/*.csvconf -o configs/sample.csv
python run.py
```

Même commande, même échantillon : relancer `sample.py` avec `--seed 1` redonne exactement le même `configs/sample.csv`.

`run.py` ne lance que les lignes de l'OS où il tourne (colonne `Systeme`) et les langages qui ont un template (Python pour l'instant). Les fichiers `configs/sample.csv` et `results/` du dépôt sont produits par GitHub Actions (`.github/workflows/experiments.yml`), sur un runner Ubuntu et un runner macOS.
