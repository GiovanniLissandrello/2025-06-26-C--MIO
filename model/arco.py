from dataclasses import dataclass

from model.costruttore import Costruttore


@dataclass
class Arco:
    u : Costruttore
    v : Costruttore
    peso : int
