"""Dérive, lance et enregistre chaque configuration de configs/sample.csv.

    python run.py

Seules les lignes d'un langage géré (LANGUAGES) et de l'OS courant sont lancées :
sur Ubuntu les lignes Systeme=Ubuntu, sur macOS les lignes Systeme=MacOS.
Les lignes C dont le compilateur n'est pas installé sont ignorées.
Résultats : results/results_<OS>_<arch>.csv (dans GitHub Actions) ou results_local/ (en local),
une ligne par exécution.
"""
import csv
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from jinja2 import Template

SAMPLE = Path("configs/sample.csv")
OUT = Path("generated")
# Le dépôt ne contient que les résultats produits par GitHub Actions ;
# en local, ils vont dans un dossier ignoré par git (sinon conflit avec les commits du bot)
RESULTS = Path("results") if os.environ.get("GITHUB_ACTIONS") else Path("results_local")
RUNS = 5
CFLAGS = ["-O2"]

# Pour chaque langage : son template, l'extension du fichier généré, la commande qui le lance
# (rien pour le C : on lance directement le binaire compilé)
LANGUAGES = {
    "Python":     {"template": Path("templates/assoc.py.jinja"), "ext": ".py", "cmd": [sys.executable]},
    "JavaScript": {"template": Path("templates/assoc.js.jinja"), "ext": ".js", "cmd": ["node"]},
    "C":          {"template": Path("templates/assoc.c.jinja"),  "ext": ".c",  "cmd": []},
}

PROPERTIES = {
    "Associativite":  ("(x + y) + z", "x + (y + z)"),
    "Distributivite": ("x * (y + z)", "x * y + x * z"),
}

# (langage, librairie, précision) -> (import, type C, tirage d'un nombre dans [0, 1[)
DRAWS = {
    ("Python", "random", "double"):     ("import random",      "", "random.random()"),
    ("Python", "numpy", "double"):      ("import numpy as np", "", "np.random.random()"),
    ("Python", "numpy", "float"):       ("import numpy as np", "", "np.float32(np.random.random())"),
    ("JavaScript", "random", "double"): ("",                   "", "Math.random()"),
    ("C", "random", "double"):          ("", "double", "(double)rand() / RAND_MAX"),
    ("C", "random", "float"):           ("", "float",  "(float)rand() / (float)RAND_MAX"),
}

# Intervalle des tirages : [0, 1[ ou [0, 100[
SCALES = {"Max1": 1, "Max100": 100}

CURRENT_OS = {"Linux": "Ubuntu", "Darwin": "MacOS"}[platform.system()]


def version(command):
    """Première ligne de `command --version`, ou "" si la commande n'existe pas."""
    if shutil.which(command) is None:
        return ""
    out = subprocess.run([command, "--version"], capture_output=True, text=True).stdout
    return out.splitlines()[0].strip() if out else ""


def scaled(draw, scale):
    """Le tirage, multiplié par l'échelle. En float32 numpy, on multiplie avant de convertir."""
    if scale == 1:
        return draw
    if draw.startswith("np.float32("):
        return f"np.float32({draw[len('np.float32('):-1]} * {scale})"
    return f"{draw} * {scale}"


def compile_c(source, binary, compiler, flags):
    """Compile un fichier C, arrête tout avec l'erreur du compilateur si ça échoue."""
    result = subprocess.run([compiler, *flags, "-o", str(binary), str(source)],
                            capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"{source} ne compile pas :\n{result.stderr}")
    return binary


def generate(row):
    """Remplit le template avec les valeurs de la ligne, écrit le programme (et le compile
    si c'est du C), renvoie le chemin de ce qu'il faut lancer."""
    language = LANGUAGES[row["Language"]]
    template = Template(language["template"].read_text())
    lhs, rhs = PROPERTIES[row["Propriete"]]
    imp, ctype, draw = DRAWS[(row["Language"], row["Librairie"], row["Precision"])]

    code = template.render(lhs=lhs, rhs=rhs, imp=imp, type=ctype,
                           draw=scaled(draw, SCALES[row["Intervalle"]]),
                           repetitions=int(row["Repetitions"]))

    OUT.mkdir(exist_ok=True)
    path = OUT / f"{row['config_id']}{language['ext']}"
    path.write_text(code)

    if row["Language"] == "C":
        return compile_c(path, OUT / row["config_id"], row["Compilateur"], CFLAGS)
    return path


def execute(row, path):
    """Lance le programme généré et renvoie le pourcentage qu'il affiche."""
    command = LANGUAGES[row["Language"]]["cmd"] + [str(path)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"{path} a planté :\n{result.stderr}")
    return float(result.stdout.strip())


def environment():
    """Où et avec quoi ça a tourné."""
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    return {"os": platform.system(), "os_version": platform.release(),
            "arch": platform.machine(), "python": platform.python_version(),
            "node": version("node"), "commit": commit}


def runnable(row):
    """Cette ligne peut-elle tourner ici ?"""
    if row["Language"] not in LANGUAGES or row["Systeme"] != CURRENT_OS:
        return False
    if row["Language"] == "C" and shutil.which(row["Compilateur"]) is None:
        print(f"{row['config_id']}: ignorée, {row['Compilateur']} n'est pas installé")
        return False
    return True


def main():
    rows = list(csv.DictReader(SAMPLE.open()))
    todo = [row for row in rows if runnable(row)]
    env = environment()

    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / f"results_{CURRENT_OS}_{platform.machine()}.csv"
    with out.open("w", newline="") as f:
        writer = None
        for row in todo:
            path = generate(row)
            compiler = {"compiler_version": version(row["Compilateur"]) if row["Language"] == "C" else "",
                        "cflags": " ".join(CFLAGS) if row["Language"] == "C" else ""}
            for run in range(1, RUNS + 1):
                result = {**row, "run": run, "percentage": execute(row, path), **env, **compiler}
                if writer is None:
                    writer = csv.DictWriter(f, fieldnames=result.keys())
                    writer.writeheader()
                writer.writerow(result)
            print(f"{row['config_id']}: {RUNS} exécutions")

    print(f"{out} : {len(todo)} configurations sur {len(rows)} lancées "
          f"({CURRENT_OS}, langages : {', '.join(LANGUAGES)})")


if __name__ == "__main__":
    main()
