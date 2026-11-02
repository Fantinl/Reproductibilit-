import subprocess
import sys
from pathlib import Path
from jinja2 import Template

template = Template(Path("assoc.py.jinja").read_text())
properties = {"assoc_add": ("(x + y) + z", "x + (y + z)"),
              "assoc_mul": ("(x * y) * z", "x * (y * z)")}
Path("generated").mkdir(exist_ok=True)
for name, (lhs, rhs) in properties.items():
    path = Path(f"generated/{name}.py")
    path.write_text(template.render(lhs=lhs, rhs=rhs, repetitions=10000))
    result = subprocess.run([sys.executable, path], capture_output=True, text=True)
    print(name, result.stdout.strip())