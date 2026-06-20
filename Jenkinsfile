pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Python') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m venv .venv'
                        sh '. .venv/bin/activate && pip install --upgrade pip'
                        sh '. .venv/bin/activate && pip install -r requirements.txt'
                    } else {
                        bat 'python -m venv .venv'
                        bat '.venv\\Scripts\\python.exe -m pip install --upgrade pip'
                        bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt'
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    if (isUnix()) {
                        sh '. .venv/bin/activate && pytest -q'
                    } else {
                        bat '.venv\\Scripts\\python.exe -m pytest -q'
                    }
                }
            }
        }

        stage('Build Artifact') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'tar -czf event-registration.tar.gz app.py requirements.txt Jenkinsfile README.md'
                    } else {
                        bat 'powershell -Command "Compress-Archive -Path app.py,requirements.txt,Jenkinsfile,README.md -DestinationPath event-registration.zip -Force"'
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'event-registration.zip, event-registration.tar.gz', allowEmptyArchive: true
            junit allowEmptyResults: true, testResults: '**/test-*.xml'
        }
    }
}
