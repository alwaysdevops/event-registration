pipeline {
    agent any

    environment {
        WINDOWS_PYTHON = 'C:/Users/Administrator/AppData/Local/Python/pythoncore-3.14-64/python.exe'
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
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    script {
                        runCommand(isUnix() ? 'command -v sonar-scanner' : 'where sonar-scanner')
                        runCommand('sonar-scanner')
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    runCommand('docker --version')
                    runCommand("docker build -t ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER} -t ${env.DOCKER_IMAGE}:latest .")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        if (isUnix()) {
                            sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                            sh "docker push ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                            sh "docker push ${env.DOCKER_IMAGE}:latest"
                            sh 'docker logout'
                        } else {
                            bat '''
                                @echo off
                                set "DOCKER_PASS_FILE=%WORKSPACE%\\docker-password.txt"
                                > "%DOCKER_PASS_FILE%" echo %DOCKER_PASS%
                                docker login -u %DOCKER_USER% --password-stdin < "%DOCKER_PASS_FILE%"
                                del "%DOCKER_PASS_FILE%"
                            '''
                            bat "docker push ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                            bat "docker push ${env.DOCKER_IMAGE}:latest"
                            bat 'docker logout'
                        }
                    }
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
