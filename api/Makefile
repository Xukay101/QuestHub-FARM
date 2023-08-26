# Definición de variables
IMAGE_NAME = questhub-api
CONTAINER_NAME = questhub
PORT = 8000

# Comandos para construir la imagen del contenedor
build:
	docker build -t $(IMAGE_NAME) .

# Comandos para ejecutar el contenedor
run:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):$(PORT) $(IMAGE_NAME)

# Comandos para detener y eliminar el contenedor
stop:
	docker stop $(CONTAINER_NAME)
    
remove:
	docker rm $(CONTAINER_NAME)

# Comando para limpiar imágenes no utilizadas
clean:
	docker image prune -f
