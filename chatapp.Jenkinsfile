pipeline{
  agent any

  environment {
    REPO = 'gcr.io/ido-chatapp/chatapp'
    RETRIES = 20
    ADDR = 'localhost'
    PORT = 9000
  }
  options { 
    disableConcurrentBuilds() 
  } 
  post{
    success{
      echo "========pipeline executed successfully ========"
    }
    failure{
      echo "========pipeline execution failed========"
    }
  }
  stages{
    stage('Version'){
      steps{
        sh "echo ${BRANCH_NAME}"
        sh "sed -i 's/build_number/${BUILD_NUMBER}/g' web/routes.py"
        sh 'grep ${BUILD_NUMBER} web/routes.py'
      }
    }
    stage('Build') {
      steps {
        script {
          img = docker.build (env.REPO, "-f chat.Dockerfile .")
        }
      }
    }
    stage('E2E') {
      options {
        timeout(time: 3, unit: "MINUTES")
      }
      parallel {
        stage('Runtime') {
          steps {
            sh 'docker-compose up'
          }
        }
        stage('E2E') {
          steps {
            sh './tests.sh ${RETRIES} ${ADDR} ${PORT}'
          }
          post {
            always{
              echo "========always========"
              sh 'docker-compose down'
            }
          }
        }
      }
    }
    stage ('Publish') {
      steps {
        script {          
            docker.withRegistry('https://gcr.io', 'gcr:ido-chatapp') {
              if ("${env.BRANCH_NAME}" =~ 'dev') {
                img.push("dev-${GIT_COMMIT}") 
              }
              else if ("${env.BRANCH_NAME}" =~ 'staging') {
                img.push("staging-${GIT_COMMIT}") 
              }
              else if ("${env.BRANCH_NAME}" =~ 'main') {
                img.push("1.0.${BUILD_NUMBER}") 
              }           
            }
          }
        }
      }
    }
  }