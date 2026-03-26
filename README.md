# Wodzone System

Sistema de seguimiento y gestión de entrenamientos con interfaz web moderna. Incluye backend Django con API REST y frontend React con Vite.

## Requisitos previos

Antes de iniciar, asegúrate de tener instalado:

- Python 3.8+
- Node.js 18+
- npm (incluido con Node.js)
- Git

Verifica las versiones:

```bash
python --version
node --version
npm --version
git --version
```

## Instalación rápida

### 1. Clonar el repositorio

```bash
git clone https://github.com/EmilianoRdzV/wodzone-system.git
cd wodzone-system
```

### 2. Configurar variables de entorno

Copia el archivo de ejemplo y edítalo según necesites:

```bash
cp .env.example .env
```

Contenido básico del .env:

```
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
DB_PATH=
MONGODB_API_KEY=your-atlas-api-key-here
MONGODB_APP_ID=your-app-id-here
MONGODB_DATABASE=wodzone
MONGODB_COLLECTION=checkins
```

### 3. Instalar dependencias de backend (Python)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

En Windows:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Aplicar migraciones de base de datos

```bash
python manage.py migrate
```

### 5. Instalar dependencias de frontend (Node.js)

```bash
cd frontend
npm install
cd ..
```

### 6. Crear superusuario (opcional, para administración)

```bash
python manage.py createsuperuser
```

Sigue las instrucciones interactivas para crear un usuario administrador.

## Ejecutar el sistema

### Opción 1: Ejecutar ambos servidores en paralelo (Recomendado)

Terminal 1 - Backend Django:

```bash
source venv/bin/activate
python manage.py runserver
```

El backend estará disponible en: http://localhost:8000

Terminal 2 - Frontend React:

```bash
cd frontend
npm run dev
```

El frontend estará disponible en: http://localhost:5173

### Opción 2: Ejecutar solo el backend

Si solo necesitas trabajar con la API:

```bash
source venv/bin/activate
python manage.py runserver
```

API disponible en: http://localhost:8000/api/

Panel de administración: http://localhost:8000/admin/

### Opción 3: Ejecutar solo el frontend

```bash
cd frontend
npm run dev
```

Frontend disponible en: http://localhost:5173

## Construir para producción

### Frontend

```bash
cd frontend
npm run build
```

Los archivos compilados estarán en `frontend/dist/`

### Backend

Para desplegar en producción, consulta la documentación oficial de Django.

## Estructura del proyecto

```
wodzone-system/
├── manage.py              # Script de gestión de Django
├── requirements.txt       # Dependencias de Python
├── db.sqlite3            # Base de datos SQLite (se crea automáticamente)
├── config/               # Configuración de Django
│   ├── settings.py       # Configuración principal
│   ├── urls.py          # URLs del proyecto
│   └── wsgi.py          # WSGI para producción
├── core/                 # Aplicación principal de Django
│   ├── models.py        # Modelos de datos
│   ├── views.py         # Vistas/APIs
│   └── urls.py          # URLs de la app
├── frontend/            # Aplicación React
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
├── templates/           # Templates HTML
├── static/              # Archivos estáticos (CSS, JS, imágenes)
└── .env                 # Variables de entorno (no compartir)
```

## Comandos útiles

### Django

```bash
python manage.py runserver                    # Ejecutar servidor de desarrollo
python manage.py migrate                      # Aplicar migraciones
python manage.py makemigrations               # Crear nuevas migraciones
python manage.py createsuperuser              # Crear usuario administrador
python manage.py shell                        # Shell interactivo de Django
python manage.py test                         # Ejecutar tests
python manage.py collectstatic                # Recopilar archivos estáticos
```

### React/Frontend

```bash
npm run dev                  # Ejecutar servidor de desarrollo
npm run build              # Compilar para producción
npm run preview            # Previsualizar compilación
npm install                # Instalar dependencias
npm list                   # Listar dependencias instaladas
```

### Git

```bash
git status                 # Ver cambios
git pull origin main       # Obtener cambios remotos
git checkout -b feature/nombre-rama    # Crear rama nueva
git add .
git commit -m "Descripción del cambio"
git push origin nombre-rama
```

## Solución de problemas

### Puerto 8000 o 5173 ya en uso

```bash
# Cambiar puerto en Django
python manage.py runserver 8001

# Cambiar puerto en React (en frontend/, edita vite.config.ts)
npm run dev -- --port 3000
```

### Erro de importación de módulos Python

Asegúrate de que el entorno virtual esté activado:

```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Base de datos dañada o cambios no reflejados

Reinicia con una base de datos limpia:

```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

Advertencia: Esto eliminará todos los datos.

### Node modules corruptos o problemas de dependencias

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Credenciales por defecto

Después de ejecutar las migraciones y crear un superusuario, accede a:

- Panel de administración: http://localhost:8000/admin/
- Usa las credenciales que ingresaste con `createsuperuser`

## Configuración de base de datos

El sistema usa SQLite por defecto, perfecto para desarrollo local. Todos los datos se almacenan en `db.sqlite3`.

Para cambiar a otra base de datos (PostgreSQL, MySQL), edita `config/settings.py` en la sección DATABASES.

## Variables de entorno

Las variables en `.env` son cargadas automáticamente. Las principales son:

- `SECRET_KEY`: Clave secreta de Django (cambiar en producción)
- `DEBUG`: Modo de depuración (debe ser False en producción)
- `MONGODB_API_KEY`: Credencial de MongoDB Atlas (si se usa)
- `MONGODB_APP_ID`: ID de aplicación MongoDB

## Próximos pasos

1. Revisa la documentación de Django: https://docs.djangoproject.com/
2. Revisa la documentación de React: https://react.dev/
3. Explora el código en `core/` para entender la lógica
4. Modifica los modelos en `core/models.py` según necesites
5. Crea nuevas vistas API en `core/views.py`

## Soporte

Para problemas, consulta:

- Logs de Django: disponibles en la terminal donde ejecutas `runserver`
- Console del navegador: abre la consola de desarrollador (F12)
- Archivo de logs (si está configurado) en `logs/`

## Licencia

Proyecto privado. Todos los derechos reservados.
