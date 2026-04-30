# pos-backend

Backend base para GalaxyMovil ERP usando FastAPI y SQL Server.

## Requisitos
- Python 3.11+
- SQL Server 2019+
- ODBC Driver 18 for SQL Server

## Arranque local
1. Crear y activar venv.
2. Instalar dependencias:
   `pip install -r requirements.txt`
3. Copiar `.env.example` a `.env` y ajustar credenciales.
4. Ejecutar:
   `uvicorn app.main:app --reload`

## Endpoints iniciales
- `GET /` estado general.
- `GET /api/v1/health` healthcheck.
- `POST /api/v1/auth/login` login inicial (mock).
