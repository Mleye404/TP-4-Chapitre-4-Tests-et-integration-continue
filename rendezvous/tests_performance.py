"""
TP4, partie 2 — Test non fonctionnel de performance (chapitre 4).

Ce test mesure le temps de réponse de la page de prise de rendez-vous.
Il s'agit d'un smoke test de performance destiné à détecter une régression
grossière qui rendrait la page anormalement lente.
"""
import time

from django.test import TestCase


class PerformanceFormulaireTest(TestCase):
    def test_formulaire_repond_rapidement(self):
        debut = time.perf_counter()

        response = self.client.get("/rendezvous/")

        duree = time.perf_counter() - debut

        self.assertEqual(response.status_code, 200)
        self.assertLess(
            duree,
            1.0,
            f"Le formulaire a répondu trop lentement : {duree:.3f} seconde(s)",
        )
