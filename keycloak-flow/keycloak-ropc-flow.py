from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.custom import Custom
from diagrams.onprem.compute import Server

with Diagram("Keycloak ROPC Flow", show=False, direction="TB"):
    user = User("User")
    app = Server("Application (Client)")
    keycloak = Custom("Keycloak", "./logo/keycloak-logo.png")
    resource = Server("Protected Resource (API)")

    user >> Edge(label="1. Provides Credentials (username/password)") >> app
    app >> Edge(label="2. Sends Credentials for Token") >> keycloak
    keycloak >> Edge(label="3. Returns Access Token") >> app
    app >> Edge(label="4. Access Protected Resource with Token") >> resource
    resource >> Edge(label="5. Return Data") >> app