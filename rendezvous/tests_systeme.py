"""
TP4, partie 2 — Test système (chapitre 4).

Un test système exerce l'application ENTIÈRE, de bout en bout, comme le
ferait un utilisateur : formulaire -> soumission -> facture.
"""
from django.test import TestCase

from patients.models import Patient

from .models import TypeConsultation


class ParcoursCompletRendezVousTest(TestCase):
    def test_parcours_complet_de_la_prise_de_rendez_vous_a_la_facture(self):
        # 1. Création d'un patient
        patient = Patient.objects.create(
            nom="Diop",
            prenom="Moussa",
            email="moussa.diop@example.com",
        )

        # 2. Affichage du formulaire de prise de rendez-vous
        response = self.client.get("/rendezvous/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, patient.nom)
        self.assertContains(response, patient.prenom)

        # 3. Soumission d'une prise de rendez-vous
        response = self.client.post(
            "/rendezvous/",
            {
                "patient": patient.id,
                "type_consultation": TypeConsultation.GENERALISTE,
                "date": "2026-09-07",
                "notes": "Consultation de contrôle",
            },
        )

        self.assertEqual(response.status_code, 302)

        # 4. Consultation de la facture du patient
        response = self.client.get(f"/rendezvous/facture/{patient.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "5000")
