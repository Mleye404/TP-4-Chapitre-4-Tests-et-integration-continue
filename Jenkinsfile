// Pipeline Jenkins pour SunuSanté (chapitre 4).
//
// Chaque stage correspond à une étape du workflow vu en cours :
// Récupération du code -> Build -> Standard de code -> Tests -> Sécurité.

def runCmd(String commande) {
    if (isUnix()) {
        sh commande
    } else {
        bat commande
    }
}

pipeline {

    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root'
        }
    }

    stages {

        stage('Récupération du code') {
            steps {
                checkout scm
            }
        }

        stage('Installation des dépendances') {
            steps {

                runCmd '''
                    python -m pip install --upgrade pip
                '''

                runCmd '''
                    pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Build') {
            steps {

                runCmd '''
                    python manage.py check
                '''

                runCmd '''
                    python manage.py collectstatic --noinput --dry-run
                '''
            }
        }

        stage('Standard de code (lint)') {
            steps {

                runCmd '''
                    flake8 .
                '''
            }
        }

        stage('Tests') {
            steps {

                runCmd '''
                    python manage.py test
                '''
            }
        }

        stage('Sécurité - SAST') {
            steps {

                runCmd '''
                    semgrep \
                        --config p/security-audit \
                        --config p/django \
                        --config p/python \
                        --error .
                '''
            }
        }

        stage('Sécurité - SCA') {
            steps {

                runCmd '''
                    pip-audit -r requirements.txt
                '''
            }
        }
    }

    post {

        success {
            echo 'Pipeline vert : build, lint, tests et sécurité tous OK.'
        }

        failure {
            echo 'Pipeline rouge : consultez le premier stage en échec ci-dessus.'
        }
    }
}