import zipfile
import os
import logging
from pathlib import Path
import argparse
import glob
import getpass
from tqdm import tqdm
from pyfiglet import Figlet

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ZipFileProcessor:
    """
    Clase para procesar archivos ZIP.
    """

    def __init__(self, file_pattern: str):
        """
        Inicializa una instancia de ZipFileProcessor con el patrón de nombre de archivo.

        :param file_pattern: Patrón de nombre de los archivos a procesar.
        """
        self.file_pattern = file_pattern

    def list_files(self):
        """
        Lista los archivos dentro de los archivos ZIP que coinciden con el patrón de nombre.
        """
        zip_files = glob.glob(self.file_pattern)

        if not zip_files:
            logging.error(f"No se encontraron ficheros ZIP que coincidan con el patrón {self.file_pattern}.")
            return

        for zip_file in zip_files:
            if not zipfile.is_zipfile(zip_file):
                logging.error(f"El fichero {zip_file} no es un archivo ZIP válido.")
                continue

            try:
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    file_list = zip_ref.namelist()
                    logging.info(f"Ficheros dentro de {zip_file}:")
                    for file in file_list:
                        logging.info(file)
            except Exception as e:
                logging.error(f"Se produjo un error al listar los ficheros de {zip_file}: {str(e)}")

    def extract(self, extract_path: str = None, password: str = None) -> None:
        """
        Extrae los archivos de los archivos ZIP que coinciden con el patrón de nombre.

        :param extract_path: Ruta de destino para extraer los archivos (opcional).
        :param password: Contraseña para extraer archivos protegidos (opcional).
        """
        zip_files = glob.glob(self.file_pattern)

        if not zip_files:
            logging.error(f"No se encontraron ficheros ZIP que coincidan con el patrón {self.file_pattern}.")
            return

        extract_path = extract_path or os.getcwd()

        if not os.path.exists(extract_path):
            logging.error(f"La ruta de descompresión {extract_path} no existe.")
            return

        for zip_file in zip_files:
            if not zipfile.is_zipfile(zip_file):
                logging.error(f"El fichero {zip_file} no es un archivo ZIP válido.")
                continue

            try:
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    total_files = len(zip_ref.namelist())
                    extracted_files = 0

                    for file_info in tqdm(zip_ref.infolist(), desc=f"Descomprimiendo {zip_file}", total=total_files, unit="file"):
                        try:
                            zip_ref.extract(file_info, path=extract_path, pwd=password.encode() if password else None)
                            extracted_files += 1
                        except Exception as e:
                            logging.error(f"Error al descomprimir {file_info.filename}: {str(e)}")

                    logging.info(f"Se han descomprimido {extracted_files} de {total_files} ficheros de {zip_file}.")
            except Exception as e:
                logging.error(f"Se produjo un error al descomprimir el fichero {zip_file}: {str(e)}")

    def compress(self, output_path: str, output_name: str = "compressed_files.zip", password: str = None) -> None:
        """
        Comprime los archivos que coinciden con el patrón de nombre en un archivo ZIP.

        :param output_path: Ruta de destino para guardar el archivo ZIP.
        :param output_name: Nombre del archivo ZIP de salida (opcional).
        :param password: Contraseña para proteger el archivo ZIP (opcional).
        """
        file_list = glob.glob(self.file_pattern, recursive=True)

        if not file_list:
            logging.error(f"No se encontraron ficheros que coincidan con el patrón {self.file_pattern}.")
            return

        if not output_name.endswith(".zip"):
            output_name += ".zip"

        if os.path.isdir(output_path):
            output_file = os.path.join(output_path, output_name)
        else:
            output_file = output_path

        try:
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                for file in tqdm(file_list, desc="Comprimiendo ficheros", unit="file"):
                    if os.path.isfile(file):
                        arcname = os.path.basename(file)
                        zip_ref.write(file, arcname)

                if password:
                    zip_ref.setpassword(password.encode())

                logging.info(f"Se han comprimido {len(file_list)} ficheros en {output_file}.")
        except Exception as e:
            logging.error(f"Se produjo un error al comprimir los ficheros: {str(e)}")


def main():
    """
    Procesa los argumentos de la línea de comandos y ejecuta la acción correspondiente sobre
    los archivos que coinciden con el patrón de nombre.

    Acciones disponibles:
        -l o --list: Muestra el listado de ficheros dentro del archivo ZIP.
        -c o --compress: Comprime los archivos en un archivo ZIP.
        Sin opciones: Descomprime los archivos en la ruta especificada.

    Opciones:
        -o o --output: Ruta de descompresión o fichero de salida (opcional).
        -p o --password: Contraseña para descomprimir o comprimir ficheros protegidos (opcional).
        -n o --name: Nombre del archivo ZIP de salida (opcional).
    """


parser = argparse.ArgumentParser(description="Procesador de ficheros ZIP")
parser.add_argument("file_pattern", help="Patrón del nombre de los ficheros a procesar")
parser.add_argument("-o", "--output", help="Ruta de descompresión o fichero de salida (opcional)", default=os.getcwd())
parser.add_argument("-p", "--password", help="Contraseña para descomprimir o comprimir ficheros protegidos (opcional)", action="store_true")
parser.add_argument("-l", "--list", help="Mostrar el listado de ficheros dentro del ZIP", action="store_true")
parser.add_argument("-c", "--compress", help="Comprimir ficheros en un archivo ZIP", action="store_true")
parser.add_argument("-n", "--name", help="Nombre del archivo ZIP de salida (opcional)", default="compressed_files.zip")

args = parser.parse_args()

file_pattern = args.file_pattern
output_path = args.output
output_name = args.name
password = getpass.getpass("Introduce la contraseña: ") if args.password else None
list_files = args.list
compress_files = args.compress

zip_processor = ZipFileProcessor(file_pattern)

if list_files:
    zip_processor.list_files()
elif compress_files:
    zip_processor.compress(output_path, output_name, password)
else:
    zip_processor.extract(output_path, password)


if __name__ == "__main__":
    f = Figlet(font='slant')
    print(f.renderText('Unzip Google Drive Files'))
    main()
