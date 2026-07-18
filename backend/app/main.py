from fastapi import FastAPI

app = FastAPI(
    title="Digital Twin Predictive Cyber Risk Audit System",
    description="Continuous cyber-risk assessment using a synchronized digital twin",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "system": "Digital Twin Predictive Cyber Risk Audit System",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }