from fastapi import FastAPI

app = FastAPI(
    title="GrowthOS API",
    description="Autonomous AI Growth & Agentic Commerce Platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "project": "GrowthOS",
        "message": "Autonomous AI Growth Engine is running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }