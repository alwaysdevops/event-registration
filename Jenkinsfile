pipeline {
    agent {
        label 'ubuntu-agent'
    }

    environment {
        DOCKER_IMAGE = 'abhiaiops88/event-registration'
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        DOCKER_BUILDKIT = '1'
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
                script {
                    if (sonarScannerAvailable()) {
                        runCommand('sonar-scanner')
                    } else {
                        echo 'sonar-scanner not found. Skipping SonarQube stage.'
                    }
                }
            }
        }

        stage('Verify Docker') {
            steps {
                script {
                    runCommand('docker --version')
                    verifyDockerDaemon()
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    runCommand("docker build -t ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER} -t ${env.DOCKER_IMAGE}:latest .")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                        sh "docker push ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                        sh "docker push ${env.DOCKER_IMAGE}:latest"
                        sh 'docker logout'
                    }
                }
            }
        }
    }
}

def runCommand(String command) {
    sh command
}

def pythonCommand() {
    return 'python3'
}

def sonarScannerAvailable() {
    return sh(script: 'command -v sonar-scanner', returnStatus: true) == 0
}

def verifyDockerDaemon() {
    def status = sh(script: 'docker info', returnStatus: true)

    if (status != 0) {
        error 'Docker CLI is installed, but Jenkins cannot reach the Docker daemon. Start Docker Engine and make sure the Jenkins agent user can run docker, usually by adding it to the docker group.'
    }
}
