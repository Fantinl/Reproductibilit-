"""Trois expériences pour vérifier nos explications (Part 8, question causale).

    python causal.py

1. mantisse : en Python, associativité, on change seulement la façon de fabriquer les nombres.
   Idée : ce qui compte, c'est le nombre de bits utiles des nombres tirés, pas le langage.
2. fma : en C, distributivité, on change seulement les options de compilation.
   Idée : l'écart x86 / ARM vient de l'instruction FMA (x * y + z calculé en une seule fois).
3. fma_assoc : pareil pour l'associativité avec des nombres entre 0 et 100 (notre C du lab 1).
   Idée : gcc fusionne le "* 100" du tirage avec l'addition, pas clang.

Résultats : results/causal_<OS>_<arch>.csv (dans GitHub Actions) ou results_local/ (en local).
"""
import csv
import platform
import shutil

from jinja2 import Template

from run import (CURRENT_OS, DRAWS, LANGUAGES, OUT, PROPERTIES, RESULTS, RUNS,
                 compile_c, environment, execute, scaled, version)

REPETITIONS = 100000

# Expérience 1 : même programme Python, quatre façons de tirer un nombre
MANTISSE = {
    "random()":                       "random.random()",
    "random() * 100":                 "random.random() * 100",
    "randrange(2**31) / (2**31 - 1)": "random.randrange(2**31) / (2**31 - 1)",   # comme rand() / RAND_MAX en C
    "randrange(2**31) / 2**31":       "random.randrange(2**31) / 2**31",
}

# Expérience 2 : même programme C, options de compilation différentes
FMA = [["-O2"], ["-O2", "-ffp-contract=off"]]
if platform.machine() == "x86_64":      # sur x86, le FMA n'est utilisé que si on le demande
    FMA += [["-O2", "-mfma"], ["-O2", "-mfma", "-ffp-contract=off"]]


def mantisse():
    """Une ligne par variante et par exécution."""
    template = Template(LANGUAGES["Python"]["template"].read_text())
    lhs, rhs = PROPERTIES["Associativite"]
    for i, (name, draw) in enumerate(MANTISSE.items()):
        path = OUT / f"causal_mantisse_{i}.py"
        path.write_text(template.render(lhs=lhs, rhs=rhs, imp="import random", draw=draw,
                                        repetitions=REPETITIONS))
        for run in range(1, RUNS + 1):
            yield {"experience": "mantisse", "Language": "Python", "Propriete": "Associativite",
                   "variante": name, "compiler_version": "", "run": run,
                   "percentage": execute({"Language": "Python"}, path)}


def fma(experience, propriete, scale):
    """Une ligne par compilateur, par jeu d'options et par exécution."""
    template = Template(LANGUAGES["C"]["template"].read_text())
    lhs, rhs = PROPERTIES[propriete]
    imp, ctype, draw = DRAWS[("C", "random", "double")]
    source = OUT / f"causal_{experience}.c"
    source.write_text(template.render(lhs=lhs, rhs=rhs, imp=imp, type=ctype, draw=scaled(draw, scale),
                                      repetitions=REPETITIONS))
    for compiler in ["gcc", "clang"]:
        if shutil.which(compiler) is None:
            print(f"{experience} : {compiler} n'est pas installé, ignoré")
            continue
        for i, flags in enumerate(FMA):
            binary = compile_c(source, OUT / f"causal_{experience}_{compiler}_{i}", compiler, flags)
            for run in range(1, RUNS + 1):
                yield {"experience": experience, "Language": "C", "Propriete": propriete,
                       "variante": f"{compiler} {' '.join(flags)}",
                       "compiler_version": version(compiler), "run": run,
                       "percentage": execute({"Language": "C"}, binary)}


def main():
    OUT.mkdir(exist_ok=True)
    RESULTS.mkdir(exist_ok=True)
    env = environment()
    out = RESULTS / f"causal_{CURRENT_OS}_{platform.machine()}.csv"
    experiences = [*mantisse(), *fma("fma", "Distributivite", 1), *fma("fma_assoc", "Associativite", 100)]
    rows = [{**row, "Repetitions": REPETITIONS, **env} for row in experiences]
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"{out} : {len(rows)} exécutions")


if __name__ == "__main__":
    main()
