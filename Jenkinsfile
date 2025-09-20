pipeline {
  agent any

  environment {
    PYENV = '.venv'
    DOCKER_IMAGE = 'i221515/mlops_a1'
    DOCKER_TAG = "build-${env.BUILD_NUMBER}"
  }

  options {
    timestamps()
  }

  triggers {
    githubPush()   // Auto-trigger on GitHub push
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Set up Python') {
      steps {
        ansiColor('xterm') {
          sh '''
            python3 -m venv ${PYENV}
            . ${PYENV}/bin/activate
            pip install --upgrade pip
            pip install -r requirements.txt
          '''
        }
      }
    }

    stage('Train Model') {
      steps {
        ansiColor('xterm') {
          sh '''
            . ${PYENV}/bin/activate
            python scripts/train_model.py --data data/Salary_dataset.csv --target Salary --model-out models/model.pkl
          '''
        }
      }
    }

    stage('Build & Push Docker Image') {
      steps {
        script {
          docker.withRegistry('https://registry-1.docker.io/', 'docker-hub-cred') {
            def img = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
            img.push()
            img.push('latest')
          }
        }
      }
    }
  }

  post {
    success {
      emailext(
        subject: "✅ SUCCESS: Jenkins build #${env.BUILD_NUMBER} for ${env.JOB_NAME}",
        to: 'abdulhananch404@gmail.com',
        body: """\
✅ Build succeeded!

Job: ${env.JOB_NAME}
Build: ${env.BUILD_NUMBER}
Git Commit: ${env.GIT_COMMIT}

Docker Image: ${DOCKER_IMAGE}:${DOCKER_TAG}
Also tagged as: ${DOCKER_IMAGE}:latest
"""
      )
    }
    failure {
      emailext(
        subject: "❌ FAILURE: Jenkins build #${env.BUILD_NUMBER} for ${env.JOB_NAME}",
        to: 'abdulhananch404@gmail.com',
        body: "❌ Build failed. See logs: ${env.BUILD_URL}"
      )
    }
  }
}
