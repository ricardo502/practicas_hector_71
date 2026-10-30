"""Reglas proposicionales del caso de estudio."""

from dataclasses import dataclass
from vehiculo import Vehiculo


@dataclass(frozen=True)
class Decision:
    acceso: bool
    inspeccion: bool


def evaluar(vehiculo: Vehiculo) -> Decision:
    """Calcula A = P ∧ S ∧ ¬Q e I = P ∧ (R ∨ Q), independientemente."""
    p = vehiculo.autorizado
    q = vehiculo.excede_peso
    r = vehiculo.material_peligroso
    s = vehiculo.certificacion_vigente
    return Decision(acceso=p and s and not q, inspeccion=p and (r or q))
