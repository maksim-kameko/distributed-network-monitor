# Distributed Network Health Monitor

A lightweight, distributed network monitoring system built with Python and FastAPI. It includes a fully automated CI/CD pipeline for continuous testing.

## Architecture
- **Server (Backend)**: Uses FastAPI and `subprocess` to execute system-level ping commands.
- **Tester (Agent)**: An OOP-based client that polls the server for status and logs results with timestamps.

## Tech Stack
- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Libraries**: Requests, Subprocess, Datetime, Time
- **Testing**: Pytest (Unit/Integration), Robot Framework (Acceptance/BDD)
- **Infrastructure**: Docker, Jenkins (Continuous Integration)

## CI/CD Pipeline
This project is continuously tested using a Jenkins pipeline running in a Docker container. On every code push, the pipeline:
1. Installs all necessary dependencies.
2. Runs unit and integration tests using `pytest`.
3. Runs acceptance/BDD tests using `Robot Framework`.
4. Generates and archives HTML/XML test reports.

## How to Run
1. Start the server:
   `uvicorn server:app --reload`
2. Run the monitoring agent (it uses 8.8.8.8 by default, or you can specify your own target):
   `python3 tester.py [TARGET_IP]`
   *Example:* `python3 tester.py 1.1.1.1`
3. View the logs:
   `cat history.log`

## Docker
1. Build the image: 
   `docker build -t monitor-server .`
2. Run the container: 
   `docker run -p 8000:8000 monitor-server`

## Testing
To run the automated test suites manually:
- Unit Tests: `python3 -m pytest test_server.py -v`
- Acceptance Tests: `python3 -m robot network_tests.robot`

## CI/CD Pipeline (Live Infrastructure)
This project is continuously integrated and tested using my own Jenkins CI server hosted in a Docker container and exposed via Cloudflare Tunnels.

🟢 **Live Jenkins Server:** [https://jenkins.maksim-network.me](https://jenkins.maksim-network.me)

The pipeline is configured directly on the Jenkins server and automatically triggers on every commit to the `main` branch. 

**Pipeline Stages:**
1. **Checkout**: Pulls the latest code from this repository.
2. **Environment Setup**: Installs Python dependencies (FastAPI, Pytest, Robot Framework) inside the Jenkins container.
3. **Unit Testing**: Executes `pytest` to verify the backend logic.
4. **Acceptance Testing**: Runs `Robot Framework` tests to validate the API responses.
5. **Artifacts**: Archives `.html` and `.xml` test reports, which are publicly viewable on the Jenkins dashboard.

### Pipeline Configuration
The pipeline is written in Groovy (Declarative Pipeline) and handles the entire build, test, and reporting process. 

<details>
<summary><b>🛠️ Click to expand the Jenkins Pipeline Code</b></summary>

```groovy
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
                echo "Installing dependencies..."
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
    }
}

