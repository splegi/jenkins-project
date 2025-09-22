pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-hello"
        CONTAINER_NAME = "flask-hello-container"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/splegi/jenkins-project'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    // Останавливаем старый контейнер, если он есть
                    sh "docker rm -f ${CONTAINER_NAME} || true"
                    // Запускаем новый
                    sh "docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_NAME}:latest"
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished!"
        }
    }
}
