pipeline {
    agent any

    environment {
        VENV = ".venv"
    }

    stages {
        stage('Install') {
            steps {
                sh 'python -m venv $VENV'
                sh '. $VENV/bin/activate && pip install --upgrade pip && pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh '. $VENV/bin/activate && pytest -q'
            }
        }

        stage('SonarQube') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t event-registration:latest .'
            }
        }
    }
}
