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

## Parts 2 et 3

- Part 2 : la branche `variafantin` teste une autre propriété, la distributivité (`x*(y+z) == x*y + x*z`).
- Part 3 : nos essais des différents mécanismes sont dans `Lab3_fantin/` (paramètres dans le programme, ligne de commande, template).

## Parts 4 à 8

### Ce qu'il y a dans le dépôt

```
fm/experiment.uvl            le feature model avec tous nos facteurs (192 configurations)
configs/*.csvconf            nos 4 programmes des labs 1 et 2, écrits comme des configurations
configs/sample.csv           l'échantillon : nos 4 programmes + 60 configurations tirées au hasard
sample.py                    le script d'échantillonnage fourni
templates/                   un template par langage (Python, JavaScript, C)
run.py                       génère chaque programme de l'échantillon, le lance 5 fois, écrit les résultats
causal.py                    deux petites expériences pour vérifier nos explications (Part 8)
results/                     les CSV de résultats, un par machine
analyse.ipynb                le notebook d'analyse (Part 8)
.github/workflows/           docker.yaml (labs 1 et 2) et experiments.yml (lab 3)
```

Les fichiers de `results/` et `configs/sample.csv` sont produits par GitHub Actions, pas par nous. Le workflow tourne sur 3 machines : Ubuntu x86, Ubuntu ARM et macOS.

### Les facteurs

| Facteur | Valeurs | Comment on le fait varier |
| ------- | ------- | ------------------------- |
| Répétitions | 10 000, 100 000, 1 000 000 | trou dans le template |
| Langage | C, Python, JavaScript | un template par langage |
| Propriété | associativité, distributivité | trou dans le template |
| Librairie | random, numpy (Python seulement) | trou dans le template |
| Précision | double, float (C ou numpy seulement) | trou dans le template |
| Intervalle | nombres entre 0 et 1, ou entre 0 et 100 | trou dans le template |
| Compilateur | gcc, clang (C seulement) | commande de compilation |
| Système | Ubuntu, macOS | matrice de jobs GitHub Actions |

### Reproduire

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python sample.py fm/experiment.uvl --size 60 --seed 1 --include configs/*.csvconf -o configs/sample.csv
python run.py
python causal.py
```

En local, les résultats vont dans `results_local/` (pas commité), pour ne pas se mélanger avec ceux de GitHub Actions. `run.py` lance seulement les lignes qui correspondent à l'OS de la machine.

Pour le notebook : `pip install -r requirements-notebook.txt`, puis ouvrir `analyse.ipynb` et tout relancer.

### Nos choix

- **Taille de l'échantillon : 60 sur 192**, soit environ un tiers, plus nos 4 programmes. Chaque valeur de chaque facteur apparaît au moins 13 fois, sauf JavaScript (5 fois) qui a peu de variantes dans le modèle. Le tout tourne en quelques minutes dans GitHub Actions.
- **Même commande, même échantillon** : on a lancé deux fois `sample.py` avec `--seed 1` et comparé les deux fichiers avec `diff`, ils sont identiques.
- **5 exécutions par configuration**, parce que le résultat est aléatoire. Ça suffit pour voir de combien il bouge.
- Chaque ligne de résultat garde les facteurs, le résultat, et où ça a tourné (OS, processeur, versions de Python, Node et du compilateur, commit).

### Ce qu'on a trouvé (détails dans le notebook)

- La propriété testée change beaucoup le résultat.
- L'écart entre nos résultats des labs 1 et 2 (75 % et 83 %) ne vient pas du langage. Il vient de la façon de tirer les nombres : générateur, intervalle, float ou double.
- La machine ne change rien, sauf pour la distributivité en C : le résultat est différent sur ARM, à cause de l'instruction FMA.
- Le nombre de répétitions ne change pas la valeur, seulement sa précision.

### Limites

- La graine de chaque exécution n'est pas enregistrée : on peut relancer une configuration, mais pas retrouver exactement les mêmes tirages.
- Sur macOS, la commande `gcc` lance en fait clang.
- On n'a testé que deux propriétés.

### Utilisation de l'IA

- **ChatGPT** : programme JavaScript du lab 2 (`TP1/egal.js`).
- **Gemini** : programme Python avec numpy (lab 3, part 1).
- **Claude Code** (Anthropic, modèles Claude Opus 5.5 puis Claude Fable 5.2) : explications sur git, Docker et GitHub Actions ; écriture des workflows, de `run.py`, de `causal.py`, des templates JavaScript et C ; ajout des facteurs précision, intervalle et compilateur au modèle ; première version du notebook et de ce README.

Ce qu'on a vérifié : on a relancé les scripts en local, regardé les programmes générés, comparé les résultats avec ceux des labs 1 et 2, et vérifié que les 3 jobs GitHub Actions passent.

