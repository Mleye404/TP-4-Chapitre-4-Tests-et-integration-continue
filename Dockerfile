FROM jenkins/jenkins:lts-jdk17

USER root

RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean

USER jenkins

RUN jenkins-plugin-cli --plugins "git workflow-aggregator docker-workflow"