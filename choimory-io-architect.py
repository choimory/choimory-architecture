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


with Diagram("choimory-io", show=False, direction="TB"):
    user = Users("user")

    with Cluster("Web"):
        front = Nextjs("client")
        user >> front

    with Cluster("Docker"):
        with Cluster("API Gateway"):
            gateway = Java("api-gateway")
            front >> gateway

        with Cluster("Message broker"):
            broker = Rabbitmq("broker")
            gateway >> broker

        with Cluster("API"):
            member_api = Kotlin("member-api")
            memo_api = Nodejs("memo-api")
            broker >> member_api
            broker >> memo_api
        
        with Cluster("Database"):
            member_db = Postgresql("member-db")
            memo_db = MongoDB("memo-db")
            member_api >> member_db
            memo_api >> memo_db

    with Cluster("CI"):
        github = Github("github")
        front >> github
        gateway >> github
        member_api >> github
        memo_api >> github  

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