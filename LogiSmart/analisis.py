"""Tabla de verdad y resumen de una flota."""

from itertools import product
from typing import Iterable
from decision import evaluar
from vehiculo import Vehiculo


def tabla_verdad() -> list[dict[str, bool]]:
    filas = []
    for p, q, r, s in product((False, True), repeat=4):
        resultado = evaluar(Vehiculo("tabla", p, q, r, s))
        filas.append(dict(P=p, Q=q, R=r, S=s, A=resultado.acceso, I=resultado.inspeccion))
    return filas


def analizar_flota(vehiculos: Iterable[Vehiculo]) -> dict[str, int]:
    """Cuenta accesos e inspecciones; las categorías pueden superponerse."""
    resumen = dict(total=0, con_acceso=0, sin_acceso=0, requieren_inspeccion=0,
                   acceso_e_inspeccion=0)
    for vehiculo in vehiculos:
        resultado = evaluar(vehiculo)
        resumen["total"] += 1
        resumen["con_acceso"] += int(resultado.acceso)
        resumen["sin_acceso"] += int(not resultado.acceso)
        resumen["requieren_inspeccion"] += int(resultado.inspeccion)
        resumen["acceso_e_inspeccion"] += int(resultado.acceso and resultado.inspeccion)
    return resumen
