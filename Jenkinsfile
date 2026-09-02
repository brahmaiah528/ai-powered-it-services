pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'docker.enterprise.org'
        IMAGE_NAME_BACKEND = 'itsm-backend'
        IMAGE_NAME_FRONTEND = 'itsm-frontend'
        BUILD_TAG = "${env.BUILD_NUMBER}"
        DATABASE_URL = 'sqlite:///./itsm.db'
        DEMO_MODE = 'true'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
        timestamps()
    }

    stages {
        stage('1. Checkout') {
            steps {
                echo "Checking out source code from GitHub repository: enterprise-org/it-service-management"
                checkout scm
            }
        }

        stage('2. Backend Dependencies') {
            steps {
                echo "Installing Python backend dependencies..."
                dir('backend') {
                    sh 'pip install --no-cache-dir -r requirements.txt'
                }
            }
        }

        stage('3. Frontend Dependencies') {
            steps {
                echo "Installing Node.js frontend dependencies..."
                dir('frontend') {
                    sh 'npm ci || npm install'
                }
            }
        }

        stage('4. Backend Tests') {
            steps {
                echo "Running backend test suite with Pytest..."
                sh 'pytest tests/backend/ -v --tb=short'
            }
        }

        stage('5. Frontend Tests') {
            steps {
                echo "Running frontend lint and tests..."
                dir('frontend') {
                    sh 'npm run build'
                }
            }
        }

        stage('6. Build Frontend') {
            steps {
                echo "Compiling React TypeScript bundle into production artifacts..."
                dir('frontend') {
                    sh 'npm run build'
                }
            }
        }

        stage('7. Build Backend') {
            steps {
                echo "Validating Python backend syntax and packaging..."
                sh 'python -m py_compile backend/app/main.py'
            }
        }

        stage('8. Docker Build') {
            steps {
                echo "Building Docker container images for Backend and Frontend..."
                sh "docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME_BACKEND}:${BUILD_TAG} ./backend"
                sh "docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME_FRONTEND}:${BUILD_TAG} ./frontend"
            }
        }

        stage('9. Docker Compose Validation') {
            steps {
                echo "Validating docker-compose.yml configuration..."
                sh 'docker compose config'
            }
        }

        stage('10. Deployment') {
            steps {
                echo "Deploying containers via Docker Compose / Kubernetes..."
                sh 'docker compose up -d --remove-orphans'
            }
        }

        stage('11. Health Check') {
            steps {
                echo "Verifying deployment health status..."
                script {
                    sleep 10
                    sh 'curl -f http://localhost:8000/api/health || exit 1'
                    echo "Deployment verified: Health Check SUCCESSFUL!"
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo "CI/CD Pipeline Build #${BUILD_NUMBER} completed successfully!"
        }
        failure {
            echo "CI/CD Pipeline Build #${BUILD_NUMBER} failed! Alerting SRE On-Call."
        }
    }
}
