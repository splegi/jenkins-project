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

        stage('Lint & Auto-fix') {
            steps {
                bat '''
                pip install flake8 black isort

                echo === flake8 check ===
                flake8 .

                echo === black auto-format ===
                black .

                echo === isort auto-format ===
                isort .
                '''
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
        
        stage('Smoke test'){
            steps {
                 bat """
                echo === Запускаем smoke-тест ===
                curl -s -o nul -w "HTTP CODE: %{http_code}\n" http://localhost:5000/ > result.txt
                findstr "HTTP CODE: 200" result.txt > nul
                if errorlevel 1 (
                    echo Smoke test FAILED!
                    exit 1
                ) else (
                    echo Smoke test PASSED!
                )
                """
            }
        }
    }

    post{
        success {
            echo "✅ Pipeline успешно завершён!"
        }

        failure {
            echo "❌ Pipeline упал. Проверь логи!"
        }

        unstable {
            echo "⚠️ Pipeline завершился, но есть предупреждения."
        }
        
        always {
            echo "📌 Pipeline закончил выполнение (успех/провал)."
            cleanWs()
        }
    }
}