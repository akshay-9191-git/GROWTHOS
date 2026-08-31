from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.opportunities import router as opportunities_router
from app.routes.agent import router as agent_router
from app.routes.actions import router as actions_router
from app.routes.decision import router as decision_router

from app.database import Base, engine

# Register all SQLAlchemy models
from app.routes.learning import router as learning_router
from app.routes.dashboard import router as dashboard_router
from app.models.action_outcome import ActionOutcome
from app.models.action_log import ActionLog
from app.models.growth_action import GrowthAction
from app.models.user import User
from app.models.product import Product
from app.models.cart import CartItem
from app.models.event import BrowsingEvent
from app.models.order import Order
from app.models.order_item import OrderItem
from app.routes.decision import router as decision_router
from app.routes.auto_growth import router as auto_growth_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="GrowthOS API",
    description="Autonomous AI Growth & Agentic Commerce Platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(opportunities_router)
app.include_router(agent_router)
app.include_router(actions_router)
app.include_router(learning_router)
app.include_router(dashboard_router)
app.include_router(decision_router)
app.include_router(auto_growth_router)


@app.get("/")
def root():
    return {
        "project": "GrowthOS",
        "message": "Autonomous AI Growth Engine is running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "connected"
    }