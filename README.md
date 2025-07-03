
---

## 🚀 Instalación

1. Clona el repositorio o descarga este backend.

2. Abre una terminal y navega a la carpeta `backend/`:

```bash
cd backend

#(Opcional pero recomendado) Crea un entorno virtual:
python -m venv venv
source venv/bin/activate    # En Linux/macOS
venv\Scripts\activate       # En Windows

#Instala las dependencias:
pip install -r requirements.txt


#Ejecutar el servidor
python app.py

#Verás en consola:
🔧 Iniciando Ferretec Backend...
📁 Los datos se guardan en archivos .txt en la carpeta 'data/'
🌐 API disponible en: http://localhost:5000


#Subir el proyecto a GitHub con:

git init
git remote add origin <url-del-repo-backend>git statu
git add .
git commit -m "Inicio backend"
git push -u origin main


git remote add origin https://github.com/JhojanR13/ferretec-backend

####
git config --global --add safe.directory 'E:/DSI-III/POO/POO PYTHON/ferretec-backend'


git push -u origin main
git branch # ver rama principal

#Hacer un commint
git add .
git commit -m "mensaje del commint"

########
git push origin master


#iniciando rama desarrollo
git checkout desarrollogit add .
git add .
git commit -m "Nueva Rama Desarrollo"


#rama desarrollo para usarla
git checkout desarrollo   # entrar a la rama desarrollo
git pull origin desarrollo  # descargar y fusionar archivos desde Github hacia tu PC


#Jhojan
git checkout desarrollo
git pull origin desarrollo
git checkout -b feature/modificaciones-de-jhojan
#Renso
git checkout desarrollo
git pull origin desarrollo
git checkout -b feature/modificaciones-de-renso
#sham
git checkout desarrollo
git pull origin desarrollo
git checkout -b feature/modificaciones-de-sham

#Trabajar y subir cambios
#Cada uno trabaja en su rama. Cuando quiere guardar avances en GitHub:
git add .
git commit -m "Tu mensaje claro de cambios"
git push origin feature/modificaciones-de-[nombre]
