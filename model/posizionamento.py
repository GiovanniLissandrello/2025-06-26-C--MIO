from dataclasses import dataclass
import datetime

@dataclass
class Posizione:
    driverId : int
    posizione: int

    def __str__(self):
        return f"{self.driverId} ({self.posizione})"