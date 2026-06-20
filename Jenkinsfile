pipeline {

    
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Python') {
            steps {
                bat 'C:/Users/Administrator/AppData/Local/Python/pythoncore-3.14-64/python.exe --version'
                bat 'C:/Users/Administrator/AppData/Local/Python/pythoncore-3.14-64/Scripts/pip.exe --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'C:/Users/Administrator/AppData/Local/Python/pythoncore-3.14-64/Scripts/pip.exe install -r requirements.txt'
            }
        }

        stage('Application Check') {
            steps {
                bat 'C:/Users/Administrator/AppData/Local/Python/pythoncore-3.14-64/python.exe -m py_compile app.py'
            }
        }

        stage('Verify Docker') {
            steps {
                bat 'docker --version'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t event-registration:v1 .'
            }
        }

        stage('Show Docker Images') {
            steps {
                bat 'docker images'
            }
        }

        stage('Run Container') {
            steps {

                bat '''
                docker rm -f event-registration-container
                '''

                bat '''
                docker run -d --name event-registration-container -p 5000:5000 event-registration:v1
                '''
            }
        }

        stage('Verify Container') {
            steps {
                bat 'docker ps'
            }
        }

    }

    post {

        success {
            echo 'Application Built and Running Successfully'
        }

        failure {
            echo 'Pipeline Failed'
        }

    }

}
