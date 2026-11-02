"""veghe – agregator OSINT de avertizare timpurie pentru drone (Iași, Nivelul A).

Citește surse publice (Ucraina, R. Moldova, România, trafic aerian civil), le arhivează
cu ora de primire, aplică reguli simple de vigilență și trimite mesaje INTERNE.
Mesajele publice sunt doar retransmiteri ale mesajelor oficiale, aprobate de un operator.

Nu face: bruiaj, interceptare, urmărirea aeronavelor militare, alerte publice proprii.
"""

import sys

if sys.version_info < (3, 11):  # tomllib și altele există doar de la 3.11
    sys.exit(f"veghe necesită Python ≥ 3.11 (acesta e {sys.version.split()[0]}). "
             "Ubuntu 22.04: sudo add-apt-repository -y ppa:deadsnakes/ppa && sudo apt install -y python3.11, "
             "apoi rulați cu python3.11 -m veghe … (vedeți docs/13).")

__version__ = "0.1.0"
