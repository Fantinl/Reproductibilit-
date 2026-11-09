"""Dérive, lance et enregistre chaque configuration de configs/sample.csv.

    python run.py

Seules les lignes du langage géré (TEMPLATES) et de l'OS courant sont lancées :
sur Ubuntu les lignes Systeme=Ubuntu, sur macOS les lignes Systeme=MacOS.
Résultats : results/results_<OS>.csv, une ligne par exécution.
"""
import csv
import platform
import subprocess
import sys
from pathlib import Path

from jinja2 import Template

SAMPLE = Path("configs/sample.csv")
OUT = Path("generated")
RESULTS = Path("results")
RUNS = 5

TEMPLATES = {"Python": Path("templates/assoc.py.jinja")}

PROPERTIES = {
    "Associativite":  ("(x + y) + z", "x + (y + z)"),
    "Distributivite": ("x * (y + z)", "x * y + x * z"),
}

LIBRARIES = {
    "random": ("import random",      "random.random()"),
    "numpy":  ("import numpy as np", "np.random.random()"),
}

CURRENT_OS = {"Linux": "Ubuntu", "Darwin": "MacOS"}[platform.system()]


def generate(row):
    """Remplit le template avec les valeurs de la ligne, écrit le programme, renvoie son chemin."""
    template = Template(TEMPLATES[row["Language"]].read_text())
    lhs, rhs = PROPERTIES[row["Propriete"]]
    imp, draw = LIBRARIES[row["Librairie"]]

    code = template.render(lhs=lhs, rhs=rhs, imp=imp, draw=draw,
                           repetitions=int(row["Repetitions"]))

    OUT.mkdir(exist_ok=True)
    path = OUT / f"{row['config_id']}.py"
    path.write_text(code)
    return path


def execute(path):
    """Lance le programme généré et renvoie le pourcentage qu'il affiche."""
    result = subprocess.run([sys.executable, path], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"{path} a planté :\n{result.stderr}")
    return float(result.stdout.strip())


def environment():
    """Où et avec quoi ça a tourné."""
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    return {"os": platform.system(), "os_version": platform.release(),
            "arch": platform.machine(), "python": platform.python_version(),
            "commit": commit}


def main():
    rows = list(csv.DictReader(SAMPLE.open()))
    todo = [row for row in rows
            if row["Language"] in TEMPLATES and row["Systeme"] == CURRENT_OS]
    env = environment()

    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / f"results_{CURRENT_OS}.csv"
    with out.open("w", newline="") as f:
        writer = None
        for row in todo:
            path = generate(row)
            for run in range(1, RUNS + 1):
                result = {**row, "run": run, "percentage": execute(path), **env}
                if writer is None:
                    writer = csv.DictWriter(f, fieldnames=result.keys())
                    writer.writeheader()
                writer.writerow(result)
            print(f"{row['config_id']}: {RUNS} exécutions")

    print(f"{out} : {len(todo)} configurations sur {len(rows)} lancées "
          f"({CURRENT_OS}, langages : {', '.join(TEMPLATES)})")


if __name__ == "__main__":
    main()
