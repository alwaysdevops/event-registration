pipeline {
    agent any

    environment {
        WINDOWS_PYTHON = 'C:/Users/Administrator/AppData/Local/Python/pythoncore-3.14-64/python.exe'
    }

    stages {
        stage('Verify Python') {
            steps {
                script {
                    runCommand("${pythonCommand()} --version")
                    runCommand("${pythonCommand()} -m pip --version")
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    runCommand("${pythonCommand()} -m pip install -r requirements.txt")
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    runCommand("${pythonCommand()} -m pytest -q")
                }
            }
        }

        stage('Application Check') {
            steps {
                script {
                    runCommand("${pythonCommand()} -m py_compile app.py")
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

def pythonCommand() {
    return isUnix() ? 'python3' : "\"${env.WINDOWS_PYTHON}\""
}
