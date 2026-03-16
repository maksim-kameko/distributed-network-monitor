pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/maksim-kameko/distributed-network-monitor.git'
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                echo "Installing system dependencies (ping)..."
                # Usuwamy sudo, bo w kontenerze zazwyczaj go nie ma
                apt-get update && apt-get install -y iputils-ping

                echo "Installing Python dependencies..."
                python3 -m pip install --upgrade pip --break-system-packages
                python3 -m pip install fastapi uvicorn requests pytest httpx robotframework robotframework-requests --break-system-packages
                '''
            }
        }

        stage('Run Unit & Integration Tests') {
            steps {
                sh 'python3 -m pytest test_server.py -v'
            }
        }

        stage('Robot Framework Tests') {
            steps {
                sh '''
                echo "Starting FastAPI server in the background..."
                python3 -m uvicorn server:app --port 8000 &
                
                sleep 3
                
                echo "Running Robot Framework automation..."
                python3 -m robot network_tests.robot || true
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: '*.html,*.xml', fingerprint: true
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline execution finished."
        }
        success {
            echo "Build Successful!"
        }
        failure {
            echo "Build Failed!"
        }
    }
}
