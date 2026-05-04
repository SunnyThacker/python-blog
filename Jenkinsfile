pipeline {
    agent any

    // Define environment variables
    environment {
        IMAGE_NAME = "my-blog"
        IMAGE_TAG = "13"
        CONTAINER_NAME = "my-blog-container"
    }
    stages {

            stage('Build Docker Image') {
                steps {
                    script {
                        echo "========== Building Docker Image =========="
                        sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                        sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
                    }
                }
            }

            stage('Scan Docker Image') {
                steps {
                    script {
                        echo "========== Scanning Docker Image =========="
                        sh "docker images ${IMAGE_NAME}:${IMAGE_TAG}"
                        echo "Image scan completed (Add Trivy/Grype here)"
                    }
                }
            }

            stage('Test Docker Image') {
                steps {
                    script {
                        echo "========== Testing Docker Image =========="

                        sh """
                        docker run -d --name test-container -p 3000:3000 ${IMAGE_NAME}:${IMAGE_TAG}
                        sleep 5
                        curl -f http://localhost:3000/
                        """

                        echo "Basic container test passed!"

                        // Cleanup test container
                        sh """
                        docker stop test-container
                        docker rm test-container
                        """
                    }
                }
            }

            stage('Health Check') {
                steps {
                    script {
                        echo "========== Performing Health Checks =========="

                        sh """
                        docker run -d --name health-container -p 3000:3000 ${IMAGE_NAME}:${IMAGE_TAG}
                        sleep 5

                        echo "Checking Home Page..."
                        curl -s http://localhost:3000/ | grep -q "My Blog" || exit 1

                        echo "Checking API..."
                        curl -s http://localhost:3000/api/posts | grep -q "Welcome" || exit 1

                        echo "Checking About Page..."
                        curl -s http://localhost:3000/about | grep -q "About" || exit 1

                        echo "All health checks passed!"
                        """

                        // Cleanup health container
                        sh """
                        docker stop health-container
                        docker rm health-container
                        """
                    }
                }
            }

            stage('Push to Registry') {
                when {
                    branch 'main'
                }
                steps {
                    script {
                        echo "========== Pushing Image =========="
                        // Example:
                        // sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} your-dockerhub/${IMAGE_NAME}:${IMAGE_TAG}"
                        // sh "docker push your-dockerhub/${IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }

            stage('Deploy') {
                when {
                    branch 'main'
                }
                steps {
                    script {
                        echo "========== Deploying Application =========="

                        sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true

                        docker run -d --name ${CONTAINER_NAME} -p 3000:3000 ${IMAGE_NAME}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }

        post {
            always {
                echo "========== Pipeline execution completed =========="
                cleanWs()
            }

            success {
                echo "========== Build SUCCESSFUL =========="
            }

            failure {
                echo "========== Build FAILED =========="
            }
        }
    }