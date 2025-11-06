from fastapi import FastAPI
from pydantic import BaseModel
from database import engine, Base
from api.router import router
from fastapi.middleware.cors import CORSMiddleware
from logger_config import get_logger

tags_metadata = [
    {
        "name": "system",
        "description": "Operational endpoints covering service status and platform metadata.",
    },
    {
        "name": "recipes",
        "description": "Create, update, and manage beer recipes with detailed ingredient breakdowns.",
    },
    {
        "name": "batches",
        "description": "Track brewery batches, their states, and production metrics.",
    },
    {
        "name": "hops",
        "description": "Manage hop inventory, varieties, and usage characteristics.",
    },
    {
        "name": "miscs",
        "description": "Maintain miscellaneous adjuncts such as spices, finings, and additives.",
    },
    {
        "name": "yeasts",
        "description": "Store yeast strains, fermentation profiles, and attenuation data.",
    },
    {
        "name": "fermentables",
        "description": "Catalog fermentable ingredients including grains, sugars, and extracts.",
    },
    {
        "name": "health",
        "description": "Health monitoring endpoints for infrastructure integrations.",
    },
    {
        "name": "logs",
        "description": "Access brewing logs for audit trails and troubleshooting.",
    },
    {
        "name": "questions",
        "description": "Manage knowledge-base questions and decision-tree prompts.",
    },
    {
        "name": "style_guidelines",
        "description": "Reference style guidelines to benchmark recipe characteristics.",
    },
    {
        "name": "styles",
        "description": "Interact with BJCP style entries and metadata.",
    },
    {
        "name": "references",
        "description": "Link external brewing references and educational resources.",
    },
    {
        "name": "mash_profiles",
        "description": "Configure mash profiles and temperature schedules.",
    },
    {
        "name": "water_profiles",
        "description": "Manage brewing water chemistry and target mineral profiles.",
    },
    {
        "name": "equipment_profiles",
        "description": "Capture equipment configurations, efficiencies, and boil-off rates.",
    },
    {
        "name": "user",
        "description": "User account endpoints for authentication and profile management.",
    },
    {
        "name": "refresh-beer-styles",
        "description": "Utility endpoints to refresh beer style datasets and cached content.",
    },
]

# Get logger instance

logger = get_logger("Main")

# Connect to the database (bind the engine)
# Create the tables in the database (create_all)
logger.info("Connecting to the database and creating tables")
Base.metadata.create_all(bind=engine, checkfirst=True)

# Create the FastAPI app and include the router from the endpoints folder

logger.info("Creating FastAPI app and including the router")
app = FastAPI(
    title="HoppyBrew API",
    description=(
        "Programmatic interface for managing brewing data within the HoppyBrew platform. "
        "The API exposes functionality for recipes, ingredient inventories, production batches, "
        "and system configuration, enabling integrations with taproom dashboards, IoT sensors, "
        "and administrative tooling."
    ),
    version="1.0.0",
    contact={
        "name": "HoppyBrew Team",
        "url": "https://github.com/asbor/HoppyBrew",
        "email": "support@hoppybrew.io",
    },
    terms_of_service="https://github.com/asbor/HoppyBrew/blob/main/README.md",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=tags_metadata,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": 0,
        "docExpansion": "list",
        "displayRequestDuration": True,
    },
)
app.include_router(router)

# Add CORS middleware to allow requests from the frontend

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ServiceStatus(BaseModel):
    message: str
    status: str

    class Config:
        schema_extra = {
            "example": {
                "message": "Welcome to the HoppyBrew API",
                "status": "online",
            }
        }


@app.get(
    "/",
    tags=["system"],
    summary="Service heartbeat",
    response_description="A short status message confirming the API is operational.",
    response_model=ServiceStatus,
)
async def read_main():
    """
    Lightweight heartbeat check that confirms the API is reachable.
    """
    return ServiceStatus(message="Welcome to the HoppyBrew API", status="online")


@app.get(
    "/health",
    tags=["system"],
    summary="Health check endpoint",
    response_description="Health status of the service and its dependencies.",
    response_model=ServiceStatus,
)
async def health_check():
    """
    Health check endpoint for container orchestration and monitoring systems.
    Returns 200 OK if the service is healthy and able to process requests.
    """
    return ServiceStatus(message="Service is healthy", status="ok")
