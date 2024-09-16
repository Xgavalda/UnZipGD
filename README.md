# Unzip Google Drive Files

Un script en Python para descomprimir y comprimir archivos ZIP desde Google Drive.

## Características

- Descomprime archivos ZIP que coincidan con un patrón de nombre específico.
- Comprime archivos que coincidan con un patrón de nombre en un archivo ZIP.
- Muestra el progreso de descompresión y compresión utilizando barras de progreso.
- Permite especificar una contraseña para descomprimir o comprimir archivos protegidos.
- Lista los archivos contenidos dentro de los archivos ZIP.

## Requisitos

- Python 3.6 o superior
- Módulo `tqdm` para mostrar el progreso (instalar con `pip install tqdm`)
- Módulo `getpass` para ingresar contraseñas de forma segura

## Instalación

1. Clona el repositorio:

        git clone https://github.com/Xgavalda/UnZipGD.git

2. Ingresa al directorio del proyecto:

        cd UnZipGD

3. Instala los requisitos:

        pip install -r requirements.txt




## Uso

El script acepta los siguientes argumentos:

- `file_pattern`: Patrón del nombre de los archivos a procesar (obligatorio).
- `-o`, `--output`: Ruta de descompresión o fichero de salida (opcional, por defecto es el directorio actual).
- `-p`, `--password`: Indica que se debe solicitar una contraseña para descomprimir o comprimir archivos protegidos (opcional).
- `-l`, `--list`: Muestra el listado de archivos dentro del ZIP (opcional).
- `-c`, `--compress`: Comprime archivos en un archivo ZIP (opcional).
- `-n`, `--name`: Nombre del archivo ZIP de salida (opcional, por defecto es "compressed_files.zip").

### Ejemplos

Descomprimir archivos ZIP que coincidan con un patrón:

        python unzipgd.py "path/to/files/*.zip"


Descomprimir archivos ZIP en una ruta específica:

        python unzipgd.py "path/to/files/*.zip" -o "path/to/output"


Descomprimir archivos ZIP protegidos con contraseña:

        python unzipgd.py "path/to/files/*.zip" -p


Mostrar el listado de archivos dentro del ZIP:

        python unzipgd.py "path/to/files/*.zip" -l




Comprimir archivos en un archivo ZIP:

        python unzipgd.py "path/to/files/*" -c -n "output.zip"




Comprimir archivos en un archivo ZIP protegido con contraseña:

        python unzipgd.py "path/to/files/*" -c -p -n "output.zip"




## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).

## Contribución

Las contribuciones son bienvenidas! Por favor, sigue las [guías de contribución](CONTRIBUTING.md) para suministrar cambios.

## Autor

- [Xgavalda](https://github.com/Xgavalda)