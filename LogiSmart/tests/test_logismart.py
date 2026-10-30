import unittest
from itertools import product

from analisis import analizar_flota, tabla_verdad
from decision import evaluar
from vehiculo import Vehiculo


class PruebasLogiSmart(unittest.TestCase):
    def test_las_16_combinaciones(self):
        # Resultados esperados escritos explícitamente en orden P,Q,R,S.
        esperados = [(False, False)] * 8 + [
            (False, False), (True, False), (False, True), (True, True),
            (False, True), (False, True), (False, True), (False, True)]
        for valores, esperado in zip(product((False, True), repeat=4), esperados):
            with self.subTest(valores=valores):
                resultado = evaluar(Vehiculo("prueba", *valores))
                self.assertEqual((resultado.acceso, resultado.inspeccion), esperado)

    def test_tabla_completa(self):
        filas = tabla_verdad()
        self.assertEqual(len(filas), 16)
        self.assertEqual(len({tuple(f[k] for k in "PQRS") for f in filas}), 16)
        self.assertEqual(sum(f["A"] for f in filas), 2)
        self.assertEqual(sum(f["I"] for f in filas), 6)

    def test_resumen_flota_completa(self):
        flota = (Vehiculo(str(i), *valores) for i, valores in
                 enumerate(product((False, True), repeat=4)))
        self.assertEqual(analizar_flota(flota), dict(total=16, con_acceso=2,
                         sin_acceso=14, requieren_inspeccion=6, acceso_e_inspeccion=1))

    def test_flota_vacia(self):
        self.assertEqual(analizar_flota([]), dict(total=0, con_acceso=0,
                         sin_acceso=0, requieren_inspeccion=0, acceso_e_inspeccion=0))

    def test_identificador_invalido(self):
        for identificador in ("", "   ", None, 12):
            with self.subTest(identificador=identificador), self.assertRaises(ValueError):
                Vehiculo(identificador, True, False, False, True)

    def test_rechaza_valores_no_booleanos(self):
        for posicion in range(4):
            for invalido in (0, 1, "False", None):
                valores = [True, False, False, True]
                valores[posicion] = invalido
                with self.subTest(posicion=posicion, invalido=invalido):
                    with self.assertRaises(TypeError):
                        Vehiculo("prueba", *valores)


if __name__ == "__main__":
    unittest.main()
