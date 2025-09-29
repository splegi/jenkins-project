pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-hello"
        CONTAINER_NAME = "flask-hello-container"
        DOCKER_IMAGE = "splegi/flask-hello" // <-- свой Docker Hub репо
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        CD_REPO = "https://github.com/splegi/cd-deploy-project"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/splegi/jenkins-project', credentialsId: 'github-creds'
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
                bat "python -m pip install --upgrade pip"
                bat "python -m pip install -r requirements.txt"
                bat "set PYTHONPATH=%CD% && pytest tests"
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %DOCKER_IMAGE%:%IMAGE_TAG% ."
            }
        }

        stage('Run Container for Smoke Test') {
            steps {
                bat """
                docker ps -a -q --filter "name=%CONTAINER_NAME%" > nul 2>&1
                IF %ERRORLEVEL%==0 docker rm -f %CONTAINER_NAME%
                docker run -d -p 5000:5000 --name %CONTAINER_NAME% %DOCKER_IMAGE%:%IMAGE_TAG%
                """
            }
        }

        stage('Smoke Test') {
            steps {
                bat '''
                echo === Smoke test ===
                curl -s -o nul -w "HTTP CODE: %%{http_code}\\n" http://localhost:5000/ > result.txt
                findstr "HTTP CODE: 200" result.txt 1>nul
                if errorlevel 1 (
                    echo Smoke test FAILED!
                    exit 1
                ) else (
                    echo Smoke test PASSED!
                )
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    docker push %DOCKER_IMAGE%:%IMAGE_TAG%
                    '''
                }
            }
        }

        stage('Update CD Repo / Helm') {
            steps {
                checkout([$class: 'GitSCM', 
                    branches: [[name: 'main']], 
                    userRemoteConfigs: [[url: CD_REPO, credentialsId: 'github-creds']]
                ])
                bat """
                powershell -Command "(Get-Content charts/flask-hello/values.yaml) -replace 'tag:.*', 'tag: ${IMAGE_TAG}' | Set-Content charts/flask-hello/values.yaml"
                git add charts/flask-hello/values.yaml
                git commit -m "Update image tag to ${IMAGE_TAG}" || echo "Nothing to commit"
                """
                // пуш через Jenkins step
                withCredentials([usernamePassword(credentialsId: 'github-creds', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                    bat 'git push https://%GIT_USER%:%GIT_PASS%@github.com/splegi/cd-deploy-project main'
                }
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
