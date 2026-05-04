pipeline {
    agent any

    environment {
        IMAGE_NAME = "my-blog"
        IMAGE_TAG = "13"
        CONTAINER_NAME = "my-blog-container"
        PORT = "3000"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                script {
                    echo "========== Building Docker Image =========="
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Test Image (Ephemeral)') {
            steps {
                script {
                    echo "========== Testing Image =========="

                    sh """
                    docker rm -f test-container || true

                    docker run -d --name test-container -p 3001:3000 ${IMAGE_NAME}:${IMAGE_TAG}
                    sleep 5

                    curl -f http://localhost:3001/

                    docker rm -f test-container
                    """
                }
            }
        }

        stage('Health Check (Ephemeral)') {
            steps {
                script {
                    echo "========== Health Check =========="

                    sh """
                    docker rm -f health-container || true

                    docker run -d --name health-container -p 3002:3000 ${IMAGE_NAME}:${IMAGE_TAG}
                    sleep 5

                    curl -s http://localhost:3002/ | grep -q "My Blog" || exit 1
                    curl -s http://localhost:3002/api/posts | grep -q "Welcome" || exit 1
                    curl -s http://localhost:3002/about | grep -q "About" || exit 1

                    docker rm -f health-container
                    """
                }
            }
        }

        stage('Deploy (Replace Old Container)') {
            steps {
                script {
                    echo "========== Deploying Application =========="

                    sh """
                    # Stop and remove old container if it exists
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true

                    # Run new version
                    docker run -d --name ${CONTAINER_NAME} -p ${PORT}:3000 ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }
    }

    post {
        always {
            echo "========== Pipeline completed =========="
        }

        success {
            echo "========== Deployment SUCCESSFUL =========="
        }

        failure {
            echo "========== Deployment FAILED =========="
        }
    }
}