# p2f-portal

Portal layer for the Past to Future projects Portal. Past to Future is an EU Horizon funded project. 

## Running the portal

*As of 2025-11-04 the below command will run the portal as a self contained object*

    sudo docker run --rm --name p2f_portal -p 8082:8082 ghcr.io/past-to-future-eu-horizon/p2f_portal:latest


## Environments

* P2F_API_HOSTNAME
* P2F_API_PORT = 443
* P2F_API_HTTPS = True
* P2F_PORTAL_EMAIL_ADDRESS
* P2F_PORTAL_TOKEN
