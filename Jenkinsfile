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

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Set up Python') {
      steps {
        bat """
          python -m venv %PYENV%
          call %PYENV%\\Scripts\\activate
          python -m pip install --upgrade pip
          pip install -r requirements.txt
        """
      }
    }

    stage('Train Model') {
      steps {
        bat """
          call %PYENV%\\Scripts\\activate
          python scripts/train_model.py --data data/Salary_dataset.csv --target Salary --model-out models/model.pkl
        """
      }
    }

    stage('Build & Push Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          bat """
            docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% .
            docker tag %DOCKER_IMAGE%:%DOCKER_TAG% %DOCKER_IMAGE%:latest
            echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
            docker push %DOCKER_IMAGE%:%DOCKER_TAG%
            docker push %DOCKER_IMAGE%:latest
          """
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
Good news! 🎉

✅ Build succeeded!

Job: ${env.JOB_NAME}
Build: ${env.BUILD_NUMBER}
Git Commit: ${env.GIT_COMMIT}

Docker Image: ${DOCKER_IMAGE}:${DOCKER_TAG}
Also tagged as: ${DOCKER_IMAGE}:latest

Check console output: ${env.BUILD_URL}
"""
      )
    }
    failure {
      emailext(
        subject: "❌ FAILURE: Jenkins build #${env.BUILD_NUMBER} for ${env.JOB_NAME}",
        to: 'abdulhananch404@gmail.com',
        body: """\
Build failed. Please check logs here:
${env.BUILD_URL}
"""
      )
    }
  }
}
