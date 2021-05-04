# conversor
Tarea Corta 1 - IC7602 Redes - I Semestre, 2021

Por,
- Michelle Molina
- Miguel Rivas

Este proyecto tiene como fin, utilizar sockets a bajo nivel en tareas cotidianas de transporte de red.

## ¿Cómo utilizar?
El proyecto se divide en dos aplicaciones: cliente y servidor.

### Servidor
Idealmente, el servidor se debe desplegar un servicio de nube pública (AWS, Azure, Google Cloud, etc.).

1. En una instancia de Ubuntu, con Docker instalado, ejecutar,
```bash
docker-compose up --build -d
```
2. Abrir el puerto 7000
```bash
sudo ufw allow 7000/tcp
```

### Cliente
El cliente puede usarse con Docker o desde Python directamente.
#### Comandos admitidos
- `convert --input [input-file] --format [target-format] --output [out-file]` -- Conversión de archivos
- `tasks` -- Tareas de conversión
- `formats` -- Formatos admitidos
- `help` -- Ayuda

#### Usando Docker
1. En la carpeta `client` compilar la imagen
```bash
docker build -t conversor .
```
2. Ejecutar el comando deseado
```bash
docker run --rm conversor [command]
```
Por ejemplo, para convertir un video (se debe agregar un volumen)
```bash
docker run --rm -v $HOME/videos:/videos conversor convert --input "/videos/sample1.mp4" --format avi --output "/videos/desde-docker.avi"
```

#### Usando Python
1. Instalar las dependencias de `requirements.txt`.
2. En la carpeta `client`, ejecutar el comando deseado,
```bash
python app.py [command]
```

Por ejemplo, para convertir un video,
```bash
python app.py --input /sample1.mp4 --format avi --output video-de-salida.avi
```