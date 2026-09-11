// Pipeline Jenkins pour SunuSanté

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
                sh '''
                    python -m pip install --upgrade pip
                    pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    python manage.py check
                    python manage.py collectstatic --noinput --dry-run
                '''
            }
        }

        stage('Standard de code (lint)') {
            steps {
                sh 'flake8 .'
            }
        }

        stage('Tests') {
            steps {
                sh 'python manage.py test'
            }
        }

        stage('Sécurité - SAST') {
            steps {
                sh '''
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
                sh 'pip-audit -r requirements.txt'
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