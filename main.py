from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import api_dependency

app = FastAPI(
    title="Pharmaceutical Supply Security Platform",
    description="A comprehensive platform for analyzing and managing pharmaceutical supply chain security",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Pharmaceutical Supply Security Platform",
        "status": "operational"
    }

# Import and include routers
# from app.api.v1.endpoints import supply_chain, risk_assessment, economic_modeling
# app.include_router(supply_chain.router, prefix="/api/v1/supply-chain", tags=["Supply Chain"])
# app.include_router(risk_assessment.router, prefix="/api/v1/risk-assessment", tags=["Risk Assessment"])
# app.include_router(economic_modeling.router, prefix="/api/v1/economic-modeling", tags=["Economic Modeling"])

# Include routers
app.include_router(api_dependency.router, prefix="/api/v1/api-dependencies", tags=["API Dependencies"]) 