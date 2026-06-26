pipeline {
    agent any

    environment {
        VENV = ".venv"
    }

    stages {
        stage('Install') {
            steps {
                script {
                    runCommand('python -m venv .venv')
                    runCommand(
                        isUnix()
                            ? '. .venv/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt'
                            : 'call .venv\\Scripts\\activate.bat && python -m pip install --upgrade pip && pip install -r requirements.txt'
                    )
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    runCommand(
                        isUnix()
                            ? '. .venv/bin/activate && pytest -q'
                            : 'call .venv\\Scripts\\activate.bat && pytest -q'
                    )
                }
            }
        }

        stage('SonarQube') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    script {
                        runCommand('sonar-scanner')
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    runCommand('docker build -t event-registration:latest .')
                }
            }
        }
    }
}

def runCommand(String command) {
    if (isUnix()) {
        sh command
    } else {
        bat command
    }
}
