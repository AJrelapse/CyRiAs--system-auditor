from fastapi import FastAPI

from app.modules.asset_discovery.router import (
    router as asset_discovery_router,
)
from app.modules.log_collection.router import (
    router as log_collection_router,
)
from app.modules.configuration.router import (
    router as configuration_router,
)

from app.db.database import Base, engine
from app.db import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Digital Twin Predictive Cyber Risk Audit System",
    description=(
        "Continuous cyber-risk assessment using "
        "a synchronized digital twin"
    ),
    version="1.0.0",
)


app.include_router(asset_discovery_router)
app.include_router(asset_discovery_router)
app.include_router(log_collection_router)
app.include_router(asset_discovery_router)
app.include_router(log_collection_router)
app.include_router(configuration_router)

@app.get("/")
def root():
    return {
        "system": "Digital Twin Predictive Cyber Risk Audit System",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }

