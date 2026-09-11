# Pipeline CI - SunuSanté

**Nom / Groupe : Groupe 3**

- **Mouhamadou Leye**
- **Seydina Mouhamed Lybass Pouye**

---

## 1. Le workflow d'intégration continue (chapitre 4, partie 1)

Le workflow présenté dans le cours suit le processus allant du commit du
développeur jusqu'au feedback fourni par le serveur d'intégration continue.

| Étape du cours | Stage Jenkins correspondant |
|---|---|
| 1. Commit & push | Git / GitHub : envoi du code sur le dépôt distant |
| 2. Notification (Jenkins est prévenu) | Déclenchement du job Jenkins `sunusante-ci` |
| 3. Build | `Build` |
| 4. Feedback build | Résultat du stage `Build` dans Jenkins |
| 5. Tests automatiques | `Tests` |
| 6. Feedback tests | Résultat du stage `Tests` dans Jenkins |

En complément de ces étapes principales, notre pipeline comporte également
les stages suivants :

- `Récupération du code`
- `Installation des dépendances`
- `Standard de code (lint)`
- `Sécurité - SAST`
- `Sécurité - SCA`

### Comment Jenkins est-il informé qu'un nouveau commit existe ?

Dans notre configuration actuelle, le pipeline a été exécuté par
**déclenchement manuel avec le bouton "Build Now" dans Jenkins**.

Le code source est récupéré depuis le dépôt GitHub lors de chaque exécution
du pipeline. Jenkins utilise le `Jenkinsfile` présent dans le dépôt Git.

Un déclenchement automatique à chaque push pourrait être ajouté
ultérieurement avec un **webhook GitHub** ou avec le **polling SCM**.

---

## 2. Les prérequis d'une bonne CI (chapitre 4, partie 3)

| Prérequis | Statut sur SunuSanté | Détail |
|---|---|---|
| Dépôt avec versioning | OK | Le projet utilise Git pour le versioning. Le dépôt distant est hébergé sur GitHub : `Mleye404/TP-4-Chapitre-4-Tests-et-integration-continue`. |
| Standard de code vérifié | OK | Le standard de code Python est vérifié avec **Flake8** dans le stage `Standard de code (lint)`. L'exécution de `flake8 .` est intégrée au pipeline. |
| Serveur d'intégration continue | OK | **Jenkins** est utilisé comme serveur CI. Il est exécuté dans un conteneur Docker et le pipeline utilise un agent Docker basé sur l'image `python:3.11-slim`. |

### Dépôt avec versioning

Le projet SunuSanté est versionné avec **Git**. Le dépôt local permet aux
développeurs de suivre l'historique des modifications et le dépôt distant
GitHub permet le partage et la centralisation du code.

Chaque version importante du projet peut être identifiée par un commit.
Jenkins récupère automatiquement la version du code présente dans le dépôt
lors de l'exécution du pipeline.

### Standard de code

Le projet utilise **Flake8** pour vérifier automatiquement la qualité et le
style du code Python.

Le stage suivant est présent dans notre Jenkinsfile :

```text
Standard de code (lint)
````

La commande exécutée est :

```bash
flake8 .
```

Au début du TP, une erreur de style était volontairement présente dans
`rendezvous/views.py`. Cette erreur a été corrigée et la commande
`flake8 .` s'exécute maintenant sans erreur.

Cette vérification automatique permet de détecter les problèmes de style
avant la validation du code et de rendre le code plus homogène entre les
différents développeurs.

### Serveur d'intégration continue

Nous utilisons **Jenkins** comme serveur d'intégration continue.

Jenkins est installé et exécuté dans un conteneur Docker. Le pipeline utilise
également Docker pour exécuter les différentes étapes dans un environnement
Python basé sur :

```text
python:3.11-slim
```

Le serveur Jenkins réalise les principales tâches suivantes :

1. récupérer le code depuis GitHub ;
2. installer les dépendances ;
3. vérifier le projet avec le stage `Build` ;
4. vérifier le standard de code avec Flake8 ;
5. exécuter les tests automatisés ;
6. exécuter les contrôles de sécurité ;
7. afficher le résultat final du pipeline.

---

## 3. Pourquoi Jenkins, ici (chapitre 4, partie 4)

| Outil          | Avantage principal                                                                                                       | Inconvénient principal                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| GitLab CI/CD   | Intégration directe avec GitLab et configuration des pipelines dans un fichier `.gitlab-ci.yml`.                         | Moins naturel pour un projet hébergé sur GitHub et dépend davantage de l'environnement GitLab.         |
| Jenkins        | Open source, très extensible grâce aux nombreux plugins et adapté aux besoins spécifiques ainsi qu'à l'auto-hébergement. | Nécessite plus de configuration, de maintenance et d'administration.                                   |
| GitHub Actions | Intégration native avec GitHub et déclenchement simple sur les événements comme les `push` et les `pull requests`.       | Peut être moins flexible que Jenkins pour certains environnements très personnalisés ou auto-hébergés. |

### Justification du choix pour SunuSanté

Jenkins convient bien à notre projet car il permet de construire un pipeline
personnalisé et d'exécuter automatiquement toutes les étapes importantes de
contrôle du projet : installation des dépendances, build, lint, tests et
sécurité.

Il permet également d'utiliser Docker afin d'exécuter le pipeline dans un
environnement Python isolé et reproductible. Même si GitHub Actions serait
également un choix naturel puisque le projet est hébergé sur GitHub, Jenkins
a été choisi dans le cadre de ce TP pour mettre en pratique le fonctionnement
d'un serveur d'intégration continue.

---

## 4. CI, Continuous Delivery, déploiement continu

### Périmètre couvert

Notre Jenkinsfile couvre principalement l'**intégration continue (CI)**.

Le pipeline réalise les opérations suivantes :

1. récupération du code source ;
2. installation des dépendances ;
3. vérification du projet avec le stage `Build` ;
4. contrôle du standard de code avec Flake8 ;
5. exécution des tests automatisés ;
6. analyse de sécurité SAST avec Semgrep ;
7. analyse des dépendances SCA avec pip-audit.

Le pipeline fournit donc un feedback automatique sur la qualité du code et
sur son bon fonctionnement.

Notre dernière exécution Jenkins est entièrement verte. Les résultats
obtenus sont notamment :

* build réussi ;
* lint réussi ;
* **18 tests exécutés avec succès** ;
* analyse SAST Semgrep réussie avec **0 vulnérabilité détectée** ;
* contrôle SCA validé après la correction de la vulnérabilité Django.

### Ce qui manquerait pour aller plus loin

Pour atteindre le niveau du **Continuous Delivery**, il faudrait ajouter des
étapes supplémentaires permettant de préparer une version toujours prête à
être livrée.

Par exemple, il faudrait :

* produire un artefact ou une image Docker versionnée ;
* préparer un environnement de préproduction ;
* ajouter une étape de release ;
* permettre un déploiement manuel vers un environnement cible après
  validation du pipeline.

Pour atteindre le **déploiement continu**, il faudrait ensuite automatiser
également le déploiement en production.

Le processus deviendrait alors :

```text
Commit
   ↓
Tests et contrôles automatiques
   ↓
Validation du pipeline
   ↓
Création de l'artefact / image Docker
   ↓
Déploiement automatique
```

La différence principale est donc la suivante :

* **CI** : le code est automatiquement intégré, buildé et testé ;
* **Continuous Delivery** : le code reste toujours prêt à être livré, mais
  une action manuelle peut être nécessaire pour déclencher la livraison ;
* **Déploiement continu** : toutes les étapes, y compris le déploiement,
  sont automatisées.

---

## 5. Tests non fonctionnels hors scope

Le chapitre 4 présente plusieurs catégories de tests non fonctionnels,
notamment :

* les tests de performance ;
* les tests de sécurité ;
* les tests capacitaires ;
* les tests de compatibilité.

Dans notre TP, les tests de performance et de sécurité sont déjà pris en
compte :

* un test de performance de type smoke test a été ajouté dans
  `rendezvous/tests_performance.py` ;
* les contrôles de sécurité sont réalisés par Semgrep pour le SAST et
  pip-audit pour le SCA.

En revanche, les tests capacitaires et de compatibilité ne sont pas
implémentés dans ce TP.

Ce choix est raisonnable car l'objectif du TP est de mettre en place les
principales bases de l'intégration continue sans ajouter des fonctionnalités
ou des tests qui ne répondent pas encore à un besoin concret du projet.

Cela correspond au principe **YAGNI ("You Aren't Gonna Need It")** : il ne
faut pas développer ou ajouter des éléments qui ne sont pas nécessaires
immédiatement.

Pour un projet pédagogique de taille limitée comme SunuSanté, mettre en
place dès maintenant des tests de charge importants ou une infrastructure
complète de compatibilité multi-navigateurs serait disproportionné par
rapport aux besoins actuels.

### Si SunuSanté grandissait réellement

Si l'application devenait un véritable système utilisé par de nombreux
patients et professionnels de santé, il serait nécessaire d'ajouter
progressivement :

#### Tests capacitaires

Des outils comme JMeter, Locust ou k6 pourraient être utilisés pour simuler
un grand nombre d'utilisateurs simultanés.

Ces tests permettraient notamment de vérifier :

* le nombre maximal d'utilisateurs supportés ;
* le comportement de l'application sous forte charge ;
* les performances de la base de données ;
* les éventuels problèmes de saturation.

#### Tests de compatibilité

Des tests supplémentaires pourraient vérifier le fonctionnement de
l'application sur :

* différents navigateurs ;
* différentes versions de navigateurs ;
* ordinateurs et appareils mobiles ;
* différents systèmes d'exploitation.

Des outils comme Selenium ou une solution de test multi-navigateurs
pourraient être intégrés au pipeline.

Ainsi, l'absence actuelle de ces tests n'est pas un oubli. Il s'agit d'un
choix adapté à la taille et aux objectifs du TP. Ces contrôles pourraient
être ajoutés progressivement si les besoins du projet évoluaient.

---

## Conclusion

Le projet SunuSanté dispose maintenant d'un pipeline d'intégration continue
fonctionnel avec Jenkins.

Le pipeline automatise les principales vérifications du projet :

```text
Récupération du code
        ↓
Installation des dépendances
        ↓
Build
        ↓
Standard de code (Flake8)
        ↓
Tests automatisés
        ↓
Sécurité SAST (Semgrep)
        ↓
Sécurité SCA (pip-audit)
        ↓
Feedback Jenkins
```

Les résultats obtenus lors de la dernière exécution sont positifs :

* Pipeline Jenkins entièrement vert ;
* 18 tests exécutés avec succès ;
* aucun test ignoré ;
* Flake8 sans erreur ;
* Semgrep sans vulnérabilité détectée ;
* pip-audit validé après correction de la vulnérabilité détectée ;
* code récupéré depuis le dépôt GitHub ;
* exécution du pipeline dans un environnement Docker avec Python 3.11.