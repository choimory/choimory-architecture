from diagrams import Diagram, Cluster
from diagrams.onprem.client import Users
from diagrams.onprem.queue import Rabbitmq
from diagrams.programming.language import Kotlin, Nodejs, Java
from diagrams.programming.framework import Nextjs
from diagrams.onprem.database import Postgresql, MongoDB
from diagrams.onprem.vcs import Github
from diagrams.onprem.container import Docker
from diagrams.onprem.ci import GithubActions
from diagrams.k8s.compute import RS, Pod, Deploy
from diagrams.aws.compute import EC2
from diagrams.aws.storage import S3
from diagrams.elastic.elasticsearch import Elasticsearch


with Diagram("choimory-io", direction="BT"):
    user = Users("user")

    with Cluster("Docker"):
        with Cluster("Web"):
            front = Nextjs("client")
            user >> front

        with Cluster("API"):
            member_api = Kotlin("member-api")
            memo_api = Nodejs("memo-api")
            front >> member_api
            front >> memo_api

        with Cluster("Database"):
            member_command = Postgresql("member-command")
            member_query = Elasticsearch("member-query")
            
            memo_command = Postgresql("memo-command")
            memo_query = MongoDB("memo-query")        

            member_api >> member_command
            member_api >> member_query
            memo_api >> memo_command
            memo_api >> memo_query

        with Cluster("Broker"):
            broker = Rabbitmq("broker")

            member_command >> broker
            member_query >> broker
            memo_command >> broker
            memo_query >> broker 

    with Cluster("CI"):
        github = Github("github")
        #front >> github
        #member_api >> github
        #memo_api >> github  

        github_actions = GithubActions("github-actions")
        github >> github_actions

    with Cluster("CD"):
        docker = Docker("docker")
        github_actions >> docker

        deploy = Deploy("k8s deploy")
        docker >> deploy

        replica = RS("k8s set")
        deploy >> replica

        pod = Pod("k8s pod")
        replica >> pod

    with Cluster("Infra"):
        ec2 = EC2("ec2")
        pod >> ec2
        
        s3 = S3("s3")