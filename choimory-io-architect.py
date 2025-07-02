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
from diagrams.onprem.inmemory import Redis


with Diagram("choimory-io", direction="TB"):
    user = Users("user")

    with Cluster("Front"):
        front = Nextjs("client")
        user >> front

    with Cluster("Member"):
        member_cqrs = Kotlin("member-cqrs") # front <-> api
        member_grpc = Kotlin("member-grpc") # api <-> api (query)
        member_event = Kotlin("member-event") # api <-> api (command)

        member_command = Postgresql("member-command")
        member_query = Elasticsearch("member-query")
        member_redis = Redis("member-redis")
        
        front >> member_cqrs

        member_cqrs >> member_command
        member_cqrs >> member_query
        member_cqrs >> member_redis

        member_grpc >> member_command
        member_grpc >> member_query
        member_grpc >> member_redis

        member_event >> member_command
        member_event >> member_query
        member_event >> member_redis

    with Cluster("Memo"):
        memo_cqrs = Nodejs("memo-cqrs")
        memo_grpc = Nodejs("memo-grpc")
        memo_event = Nodejs("memo-event")

        memo_command = Postgresql("memo-command")
        memo_query = MongoDB("memo-query")
        memo_redis = Redis("memo-redis")

        front >> memo_cqrs

        memo_cqrs >> memo_command
        memo_cqrs >> memo_query
        memo_cqrs >> memo_redis

        memo_grpc >> memo_command
        memo_grpc >> memo_query
        memo_grpc >> memo_redis

        memo_event >> memo_command
        memo_event >> memo_query
        memo_event >> memo_redis

        memo_grpc >> member_grpc >> memo_grpc
    
    with Cluster("Board"):
        board_cqrs = Kotlin("board-cqrs")
        board_grpc = Kotlin("board-grpc")
        board_event = Kotlin("board-event")

        board_command = Postgresql("board-command")
        board_query = Elasticsearch("board-query")
        board_redis = Redis("board-redis")

        front >> board_cqrs

        board_cqrs >> board_command
        board_cqrs >> board_query
        board_cqrs >> board_redis

        board_grpc >> board_command
        board_grpc >> board_query
        board_grpc >> board_redis

        board_event >> board_command
        board_event >> board_query
        board_event >> board_redis

        board_grpc >> member_grpc >> board_grpc
        board_grpc >> memo_grpc >> board_grpc

    with Cluster("Message broker"):
        broker = Rabbitmq("broker")

        member_event >> broker >> member_event
        memo_event >> broker >> memo_event
        board_event >> broker >> board_event

    with Cluster("CI"):
        github = Github("github")

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
        s3 = S3("s3")

        pod >> ec2