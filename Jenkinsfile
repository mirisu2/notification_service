pipeline {
   agent {label 'io'}

   options {
      disableConcurrentBuilds()
      buildDiscarder(logRotator(numToKeepStr: '5'))
   }
    
   environment {
      TELEGRAM_ID      = credentials('TELEGRAM_ID')
      X_NOTIFY_API_Key = credentials('X_NOTIFY_API_Key')
   }
    
   stages {
       
      stage('Clone repository') {
         steps {
            git url: 'https://github.com/mirisu2/notification_service.git', branch: 'master'
         }
         post {
            success {
                sh 'ls -lha'
                sh 'pwd'
                echo '---------- Clone repository successfully'
            }
         }
      }

      stage('Copy cfg file into app folder') {
         steps {
            echo "---------- Copy cfg file into app folder"
            sh 'cp /home/arty/configs/notify_service.cfg ./instance/production.cfg'
         }
      }
      
      stage('Build & tag & push image') {
         steps {
             echo "---------- Build image notify"
             sh "docker build -t notify ."
         }
      }
      
      stage('Stop running container and remove it') {
         steps {
            sh 'docker ps -f name=notify -q | xargs --no-run-if-empty docker container stop'
            sh 'docker container ls -a -fname=notify -q | xargs -r docker container rm'
         }
      }

      stage('Run container') {
         steps {
            echo "Run container notify"
            sh "docker run --env-file /home/arty/configs/notify_service_env.list -d --restart=always --security-opt apparmor=docker-default --cpus=1 --memory=1g --oom-kill-disable --log-driver syslog --log-opt syslog-address=udp://192.168.198.253:514 --log-opt tag=notify_service --name notify -p 5005:80 notify"
         }
      }
      stage('Test app') {
          steps {
              script{
                 result = sh( script: "curl -X GET http://notify.h744.host/ping", returnStdout: true)
              }
              echo "curl: ${result}"
          }
      }    
      
   }
   
   post { 
        success { 
            sleep 15
            sh "curl --location --request POST 'http://notify.h744.host/api/v2/telegram' \
                --header 'Content-Type: application/json' \
                --header 'X-NOTIFY-API-Key: ${env.X_NOTIFY_API_Key}' \
                --data-raw '{\"id\": \"${env.TELEGRAM_ID}\",\"text\":\"New container **notify** was built and started\"}'"
        }
        failure {
            mail to: "${env.ADMIN_EMAIL}",
            subject: "Pipeline ${currentBuild.fullDisplayName} is failed",
            body: "Your build ${BUILD_ID} was not completed, please check: ${env.BUILD_URL}"            
        }
    }     
}
