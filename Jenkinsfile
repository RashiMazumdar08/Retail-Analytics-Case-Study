// ============================================
// Jenkinsfile - CI/CD Pipeline
// Stages: Checkout -> Test -> Build Image -> Push -> Deploy
// ============================================
pipeline {
    agent any

    environment {
        IMAGE_NAME = "your-dockerhub-username/retail-analytics"
    }

    stages {

        stage('Checkout Code') {
            steps {
                // Pull latest code from GitHub
                git branch: 'main', url: 'https://github.com/your-username/spark-retail-analytics.git'
            }
        }

        stage('Test') {
            steps {
                // Simple check: does the Python file compile?
                sh 'python3 -m py_compile app.py'
                echo 'Tests passed'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                 usernameVariable: 'DOCKER_USER',
                                 passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $IMAGE_NAME:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s-deployment.yaml'
                sh 'kubectl get pods'
            }
        }
    }

    post {
        success { echo 'Pipeline completed successfully!' }
        failure { echo 'Pipeline failed. Check logs.' }
    }
}
