# API de contactos y tareas

API REST construida con FastAPI. Para ejecutarla localmente, necesitas [uv](https://docs.astral.sh/uv/) y Python 3.14 o superior.

## Iniciar el proyecto

1. Clona el repositorio y entra en la carpeta del proyecto:

	```bash
	git clone <URL_DEL_REPOSITORIO>
	cd deimianvasquez-api-fast
	```

2. (Opcional) Crea el archivo local de variables de entorno a partir de la plantilla:

	```bash
	cp .env.example .env
	```

3. Instala las dependencias:

	```bash
	uv sync
	```

4. Inicia el servidor de desarrollo:

	```bash
	uv run fastapi dev app/main.py
	```

También puedes ejecutarlo desde la raíz del proyecto con el comando abreviado:

	```bash
	uv run fastapi dev
	```

La API estará disponible en <http://127.0.0.1:8000>. La documentación interactiva de los endpoints está en <http://127.0.0.1:8000/docs> y la ruta de salud en <http://127.0.0.1:8000/health>.

Para detener el servidor, usa `Ctrl+C`.
