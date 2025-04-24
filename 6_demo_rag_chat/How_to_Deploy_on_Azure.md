## INSTRUCTIONS FOR DEPLOYING ON AZURE

### 0. Install and open Docker Desktop

### 1. Build the Docker image:
`docker build -t rag_chat .`

### 2. Test the image locally:
`docker run -p 8501:8501 rag_chat`

### 3. Create an Azure Container Registry resource:
- Go to the Azure portal and create a new Container Registry (ACR) resource.
- The ACR name is `<your-registry-name>`

### 4. Log in to Azure Container Registry:
`az acr login --name <your-registry-name>`

### 5. Tag the Docker image:
`docker tag rag_chat <your-registry-name>.azurecr.io/rag_chat:v1`

### 6. Push the image to Azure Container Registry:
`docker push <your-registry-name>.azurecr.io/rag_chat:v1`

### 7. Enable admin user in ACR:
`az acr update -n <your-registry-name> --admin-enabled true`

### 8. Create an Azure Container Instance resource:
- Go to the Azure portal and create a new Azure Container Instances (ACI) resource.
- Configure the ACI to use the image you pushed to Azure Container Registry.
- Networking:
   + DNS name label: Enter the `<your-registry-name>` as the domain name
   + Port: remove 80 and enter 8501 / TCP, which is the port where Streamlit runs the application.

`az container create --resource-group <tu_grupo_de_recursos> --name <your-registry-name> --image <your-registry-name>.azurecr.io/rag_chat:v1 --cpu 1 --memory 1.5 --registry-login-server <your-registry-name>.azurecr.io --registry-username <your-registry-name> --registry-password <acr-password> --ports 8501 --dns-name-label <your-registry-name> --query instanceView.state`

### 9. Configure environment variables (if necessary):
- In the Azure portal, go to the container settings and add the necessary environment variables.

### 10. Start the container:
- Once configured, start the container and your Streamlit application should be accessible at the URL provided by Azure.
   `http://<your-registry-name>.<region>.azurecontainer.io:8501/`

# ------------------------------------------------------------------------

## INSTRUCCIONES PARA DESPLEGAR EN AZURE

### 0. Instalar y abrir docker desktop

### 1. Construir la imagen Docker:
`docker build -t rag_chat .`

### 2. Probar la imagen localmente:
`docker run -p 8501:8501 rag_chat`

### 3. Crear un recurso de Azure Container Registry:
- Ve al portal de Azure y crea un nuevo recurso de Container Registry (ACR).
- El nombre de ACR es `<nombre-de-tu-registro>`

### 4. Iniciar sesi�n en Azure Container Registry:
`az acr login --name <nombre-de-tu-registro>`

### 5. Etiquetar la imagen Docker:
`docker tag rag_chat <nombre-de-tu-registro>.azurecr.io/rag_chat:v1`

### 6. Subir la imagen a Azure Container Registry:
`docker push <nombre-de-tu-registro>.azurecr.io/rag_chat:v1`

### 7. Habilitad usuario admin en el ACR
`az acr update -n <nombre-de-tu-registro> --admin-enabled true`

### 8. Crear un recurso de Azure Container Instance:
- Ve al portal de Azure y crea un nuevo recurso de Azure Container Instances (ACI).
- Configura el ACI para usar la imagen que subiste a Azure Container Registry.
- Networking:
   + DNS name label: Introduce `<nombre-de-tu-registro>` para el dominio
   + Networking: Puerto: elimina el puerto 80 e introduce 8501 / TCP, que es el puerto en el que Streamlit ejecuta la aplicaci�n.

`az container create --resource-group <tu_grupo_de_recursos> --name <nombre-de-tu-registro> --image <nombre-de-tu-registro>.azurecr.io/rag_chat:v1 --cpu 1 --memory 1.5 --registry-login-server <nombre-de-tu-registro>.azurecr.io --registry-username <nombre-de-tu-registro> --registry-password <acr-password> --ports 8501 --dns-name-label <nombre-de-tu-registro> --query instanceView.state`

### 9. Configurar las variables de entorno (si es necesario):
- En el portal de Azure, ve a la configuraci�n del contenedor y a�ade las variables de entorno necesarias.

### 10. Iniciar el contenedor:
- Una vez configurado, inicia el contenedor y tu aplicaci�n Streamlit deber�a estar accesible en la URL proporcionada por Azure.
   `http://<nombre-de-tu-registro>.<region>.azurecontainer.io:8501/`
