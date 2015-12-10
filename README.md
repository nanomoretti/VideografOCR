# VideograffOCR

#### Reconocimiento automático de texto en informativos de TV

### Set-up

#### virtualenv

```bash
$ sudo apt-get python-pip
$ pip install virtualenv
$ pip install virtualenvwrapper
```
Agregar las siguientes líneas al correspondiente archivo de configuración de
shell (`.bashrc`, `.zshrc`, etc.)
```bash
# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```

Crear entorno virtual e instalar paquetes python del proyecto. Puede que
algunos paquetes fallen al compilarse (por ej., numpy). Atender a los errores
(generalmente, faltan librerías o binarios de compilación en el sistema).
Enriquecer este README con los errores encontrados y listar las soluciones como
pasos necesarios.

```
$ mkvirtualenv videograffocr
$ workon videograffocr
$ pip install -r requirements.txt
```

Cuando se incorporan nuevas librerías, actualizar los requerimientos con `pip
freeze > requirements.txt`

#### python set-up
Asumiendo que el proyecto está clonado en `/home/user/videografocr`,
agregar al correspondiente archivo de configuración de shell (`.bashrc`, `.zshrc`, etc.)

`export PYTHONPATH=PYTHONPATH:/home/user/`

#### tesseract

`sudo apt-get install tesseract-ocr tesseract-ocr-spa`

#### opencv

_Lista de pasos tentativa, originalmente publicada
[aquí](http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/),
mezclada con la
[documentación](http://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html)
de opencv_

- update del sistema
```bash
$ sudo apt-get update && sudo apt-get upgrade
```

- instalación de herramientas de compilación
```bash
$ sudo apt-get install build-essential cmake-curses-gui pkg-config
```

- paquetes que permiten la lectura y escritura de imágenes
```bash
$ sudo apt-get install libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev
```

- paquetes que permiten la lectura de video
```bash
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
```

- paquetes optimización de rutinas de opencv
```bash
$ sudo apt-get install libatlas-base-dev gfortran
```

- librerías de desarrollo de python
```bash
$ sudo apt-get install python2.7-dev
```

- TODO: qt, gtk?

- clonar el repositorio de opencv, fuera de este repositorio. _Esto puede
  reemplazarse por *descargar la versión deseada* de opencv_

    ```bash
    $ cd && mkdir opencv_build
    $ cd opencv_build
    $ git clone https://github.com/Itseez/opencv.git
     ```

- configurar el projecto antes de compilar
    ```
    $ cd opencv
    $ mkdir build && cd build  # directorio temporal
    $ ccmake ..                   # para elegir las configuraciones antes de
generar los Makefiles
    ```

- compilar
    ```bash
    $ make -j <número de procesadores>
    ```

Asumiendo que la compilación fue exitosa, podemos instalar opencv en el
sistema:
    ```bash
    $ sudo make install
    ```

Ahora opencv se encuentra instalado en el sistema, pero todavía no es accesible
desde el entorno virtual creado. Es necesario copiar o linkear la librearía de
python *del sistema* en el entorno virtual del proyecto

- Ubicar la librería opencv:
```bash
$ deactivate   # para dejar de usar el virtualenv, volver al python del sistema
$ python
Python 2.7.6 (default, Jun 22 2015, 17:58:13)
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> print cv2.__file__
/usr/lib/python2.7/dist-packages/cv2.so
```

- copiar la librería al directorio donde nuestro entorno virtual busca
  librerías
```bash
$ ln -s /usr/lib/python2.7/dist-packages/cv2.so
~/.virtualenvs/videograffocr/lib/python2.7/site-packages/cv2.so
```
- chequear que opencv está accesible desde el virtualenv
```bash
$ workon videograffocr && python -c "import cv2; print cv2.__file__"
```

Esta línea debería ejecutar sin errores.


