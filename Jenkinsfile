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
                apt-get update && apt-get install -y iputils-ping python3 python3-pip
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
                echo "Cleaning up old server processes..."
                pkill -f uvicorn || true
                
                echo "Starting FastAPI server in the background..."
                # Uruchomienie z przekierowaniem logów do pliku
                python3 -m uvicorn server:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
                
                sleep 5
                
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
            echo "Cleaning up before finishing..."
            sh 'pkill -f uvicorn || true'
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
