pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = "2023bcd0056niketh"
        DOCKERHUB_PASSWORD = "dckr_pat_kI906L7-NHbe-rA1SoSn_l-NFvM"
        EC2_PUBLIC_IP      = '13.61.175.33'

        REGISTER_NUMBER    = "na"
        ROLL_NUMBER        = "2023bcd0056"

        FRONTEND_IMAGE     = "${DOCKERHUB_USERNAME}/${REGISTER_NUMBER}_${ROLL_NUMBER}_frontend"
        BACKEND_IMAGE      = "${DOCKERHUB_USERNAME}/${REGISTER_NUMBER}_${ROLL_NUMBER}_backend"
    }

    stages {

        stage('Checkout') {
            steps {
                echo '--- Checking out source code from GitHub ---'
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                echo '--- Building Docker images ---'
                sh "docker build -t ${FRONTEND_IMAGE}:latest ./frontend"
                sh "docker build -t ${BACKEND_IMAGE}:latest  ./backend"
            }
        }

        stage('Tag Images') {
            steps {
                echo '--- Tagging images with build number ---'
                sh "docker tag ${FRONTEND_IMAGE}:latest ${FRONTEND_IMAGE}:${BUILD_NUMBER}"
                sh "docker tag ${BACKEND_IMAGE}:latest  ${BACKEND_IMAGE}:${BUILD_NUMBER}"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo '--- Pushing images to Docker Hub ---'
                sh "echo ${DOCKERHUB_PASSWORD} | docker login -u ${DOCKERHUB_USERNAME} --password-stdin"
                sh "docker push ${FRONTEND_IMAGE}:latest"
                sh "docker push ${FRONTEND_IMAGE}:${BUILD_NUMBER}"
                sh "docker push ${BACKEND_IMAGE}:latest"
                sh "docker push ${BACKEND_IMAGE}:${BUILD_NUMBER}"
            }
        }

        stage('Deploy on EC2') {
            steps {
                echo '--- Deploying on AWS EC2 via SSH ---'
                sshagent(['ec2-ssh-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@${EC2_PUBLIC_IP} '
                            export DOCKERHUB_USERNAME=${DOCKERHUB_CREDS_USR}
                            cd ~/student-app
                            docker-compose pull
                            docker-compose down
                            docker-compose up -d
                        '
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline succeeded! App live at http://${EC2_PUBLIC_IP}"
        }
        failure {
            echo "❌ Pipeline failed. Check logs above."
        }
        always {
            sh "docker logout"
        }
    }
}