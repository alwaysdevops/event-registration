pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code downloaded from GitHub'
            }
        }

        stage('Build') {
            steps {
                bat 'dir'
            }
        }

        stage('Test') {
            steps {
                bat 'if exist index.html (echo TEST PASSED) else (exit 1)'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Application deployed successfully'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }

        failure {
            echo 'Pipeline failed'
        }
    }
}
