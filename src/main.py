"""
Module main
"""
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from dynaconf import settings

from src.app.facilities.vendors import resource as vendors
from src.app.facilities.locations import resource as locations
from src.app.ipam.devices import resource as devices
from src.app.ipam.interfaces.single import resource as interfaces_single
from src.app.ipam.interfaces.lag import resource as interfaces_lag
from src.app.ipam.circuits import resource as circuits
from src.app.ipam.tunnel import resource as tunnel
from src.app.ipam.paths import resource as paths
from src.app.ipam.tunnel_traffic_policies import resource as tunnel_traffic_policies


from src.app.ipam.vlans import resource as vlans
from src.app.ipam.l2domains import resource as l2domains


from src.infrastructure.odm.database import init_db
from src.logging import get_logger

logger = get_logger(__name__)

APP_NAME = os.environ.get("APP_NAME", "app")


app = FastAPI(
    title="Gestão de Malha MPLS",
    description=settings.DESCRIPTION,
    version="0.0.1",
    contact={
        "name": "Deivison Marteleto" ,
        "email": "dmarteleto@gmail.com",
    },
    openapi_url="/v1/openapi.json",
    docs_url="/documentation",
    redoc_url=None
)

origins = [
    "http://0.0.0.0:8000",
    "http://localhost:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """
    Events that will be executed when the application starts
    """
    logger.info("Starting app and database.... %s", APP_NAME)
    await init_db(
        db_host=settings.DB_HOST,
        db_name=settings.DB_NAME
    )

    #ipam
    app.include_router(vlans.router)
    app.include_router(l2domains.router)
    #facilities
    app.include_router(vendors.router)
    app.include_router(locations.router)
    app.include_router(devices.router)
    app.include_router(interfaces_single.router)
    app.include_router(interfaces_lag.router)
    app.include_router(circuits.router)
    app.include_router(tunnel.router)
    app.include_router(paths.router)
    app.include_router(tunnel_traffic_policies.router)



@app.exception_handler(Exception)
def global_exception_handler(exc: Exception):
    """
    log your exception here
    you can also request details by using request object
    """
    logger.error("Erro interno: %s",exc )

    return JSONResponse(content={"message":"Um erro interno ocorreu!"},
    status_code=500)

