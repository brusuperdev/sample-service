pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID  = '605893374669'
        AWS_REGION      = 'us-east-1'
        ECR_REPO        = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/bruviti-ai-superdev-central"
        IMAGE_TAG       = "${env.BUILD_NUMBER}"
        EKS_CLUSTER     = 'bruviti-ai-superdev-eks'
        HELM_RELEASE    = 'sample-service'
        HELM_CHART_PATH = 'helm/sample-service'
        NAMESPACE       = 'default'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/brusuperdev/sample-service.git',
                    credentialsId: 'github-brusuperdev',
                    branch: 'main'
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${ECR_REPO}:${IMAGE_TAG} -t ${ECR_REPO}:latest ."
            }
        }

        stage('ECR Push') {
            steps {
                sh """
                    aws ecr get-login-password --region ${AWS_REGION} | \
                        docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                    docker push ${ECR_REPO}:${IMAGE_TAG}
                    docker push ${ECR_REPO}:latest
                """
            }
        }

        stage('Helm Deploy') {
            steps {
                sh """
                    aws eks update-kubeconfig --name ${EKS_CLUSTER} --region ${AWS_REGION}
                    helm upgrade --install ${HELM_RELEASE} ${HELM_CHART_PATH} \
                        --namespace ${NAMESPACE} \
                        --set image.tag=${IMAGE_TAG}
                """
            }
        }

        stage('Verify') {
            steps {
                sh """
                    kubectl rollout status deployment/${HELM_RELEASE} -n ${NAMESPACE} --timeout=120s
                    kubectl get pods -n ${NAMESPACE} -l app=${HELM_RELEASE}
                """
            }
        }
    }

    post {
        success {
            echo "Deployed ${ECR_REPO}:${IMAGE_TAG} to ${EKS_CLUSTER}"
        }
        failure {
            echo "Pipeline failed at stage: ${env.STAGE_NAME}"
        }
    }
}
