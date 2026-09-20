from contextlib import asynccontextmanager

from fastapi import FastAPI

from db import get_database_structure
from logger import get_logger
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(settings)
    logger = get_logger()
    logger.info("Starting app")
    structure = await get_database_structure()
    bases_datos = list(structure.keys())
    logger.info(f"Bases de datos disponibles: {bases_datos}")
    base = structure.get(bases_datos[0])
    logger.info(f"Base de datos seleccionada: {bases_datos[0]}")
    tablas = list(base.keys())
    logger.info(f"Tablas disponibles: {tablas}")
    tabla = base.get(tablas[0])
    logger.info(f"Tabla seleccionada: {tabla.keys()}")

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}
