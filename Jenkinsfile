pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/maksim-kameko/distributed-network-monitor.git'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    docker run --rm \
                        -v $(pwd):/app \
                        -w /app \
                        python:3.10-slim \
                        sh -c "pip install fastapi uvicorn requests pytest httpx --quiet && pytest /app/test_server.py -v"
                '''
            }
        }

        stage('Robot Framework Tests') {
            steps {
                sh '''
                    docker run --rm \
                        -v $(pwd):/app \
                        -w /app \
                        python:3.10-slim \
                        sh -c "pip install robotframework robotframework-requests --quiet && python -m robot network_tests.robot"
                '''
            }
        }

        stage('Docker Build & Deploy') {
            steps {
                sh '''
                    docker stop fastapi-monitor || true
                    docker rm fastapi-monitor || true
                    docker build -t monitor-server .
                    docker run -d \
                        --name fastapi-monitor \
                        -p 8000:8000 \
                        --env-file /home/tucamaks/distributed-network-monitor/.env \
                        monitor-server
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        failure {
            echo 'Build Failed!'
        }
    }
}
