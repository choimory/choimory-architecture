from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.custom import Custom

with Diagram("Keycloak Authorization Code Flow", show=False, direction="TB"):
    user = User("User")
    browser = Custom("Browser", "./logo/browser-logo.png")
    app = Server("Application (Client)")
    keycloak = Custom("Keycloak", "./logo/keycloak-logo.png")
    resource = Server("Protected Resource (API)")

    with Cluster("User's Device"):
        user >> Edge(label="1. Access Application") >> browser

    browser >> Edge(label="2. Request Login") >> app
    app >> Edge(label="3. Redirect to Keycloak") >> browser
    browser >> Edge(label="4. User Logs In") >> keycloak
    keycloak >> Edge(label="5. Return Authorization Code") >> browser
    browser >> Edge(label="6. Send Authorization Code") >> app
    app >> Edge(label="7. Exchange Code for Token") >> keycloak
    keycloak >> Edge(label="8. Return Access Token (and ID Token)") >> app
    app >> Edge(label="9. Access Protected Resource with Token") >> resource
    resource >> Edge(label="10. Return Data") >> app