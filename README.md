# Sakkokassa Webapp

**1. Install Docker & Docker-compose**      

**2. Clone repo**      

**3. Create .env file from template**     

/DJANGO VARIABLES/  
SECRET_KEY= <GIVE_YOUR_SECRET_KEY>  
DEBUG=0  
ALLOWED_HOSTS= localhost 127.0.0.1 <YOUR_DOMAIN> [::1]  

/LETSENCRYPT VARIABLES/  
DEFAULT_EMAIL=<YOUR_EMAIL>  
NGINX_PROXY_CONTAINER=nginx-proxy  
ACME_CA_URI=https://acme-staging-v02.api.letsencrypt.org/directory  <-- *REMOVE THIS FOR PRODUCTION CERTIFICATES*     

/NGINX PROXY VARIABLES/  
VIRTUAL_HOST=<YOUR_DOMAIN>  
VIRTUAL_PORT=8000  
LETSENCRYPT_HOST=<YOUR_DOMAIN>  

**4. Fill credentials for superuser account (username & password)**    
