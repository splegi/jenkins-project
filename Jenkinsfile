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
        
        stage('Run Tests') {
            steps {
                // Устанавливаем зависимости
                bat "python -m pip install --upgrade pip"
                bat "python -m pip install -r requirements.txt"
                
                // Добавляем текущую директорию в PYTHONPATH и запускаем pytest
                bat "set PYTHONPATH=%CD% && pytest tests"
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME%:latest ."
            }
        }

        stage('Run Container') {
            steps {
                bat """
                REM Останавливаем старый контейнер, если он существует
                docker ps -a -q --filter "name=%CONTAINER_NAME%" > nul 2>&1
                IF %ERRORLEVEL%==0 docker rm -f %CONTAINER_NAME%
                
                REM Запускаем новый контейнер
                docker run -d -p 5000:5000 --name %CONTAINER_NAME% %IMAGE_NAME%:latest
                """
            }
        }
    }

    post {
        always {
            echo "Pipeline finished!"
        }
    }
}

