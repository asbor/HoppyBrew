import os
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict
from database import engine, Base
from api.router import router
from fastapi.middleware.cors import CORSMiddleware
from logger_config import get_logger
from config import settings

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
        "name": "fermentation",
        "description": "Track fermentation progress with gravity, temperature, and pH readings over time.",
    },
    {
        "name": "user",
        "description": "User account endpoints for authentication and profile management.",
    },
    {
        "name": "refresh-beer-styles",
        "description": "Utility endpoints to refresh beer style datasets and cached content.",
    },
    {
        "name": "homeassistant",
        "description": "HomeAssistant integration endpoints for monitoring brewing batches.",
    },
    {
        "name": "calculators",
        "description": "Brewing calculation utilities for strike water, ABV, priming sugar, yeast starters, and more.",
    },
    {
        "name": "analytics",
        "description": "Comprehensive analytics for batch performance, cost analysis, and brewing trends.",
    },
]

# Get logger instance

logger = get_logger("Main")

# Connect to the database (bind the engine)
# Create the tables in the database (create_all)
# Only create tables if not in testing mode
if os.getenv("TESTING", "0") != "1":
    logger.info("Connecting to the database and creating tables")
    Base.metadata.create_all(bind=engine, checkfirst=True)
else:
    logger.info("Testing mode detected - skipping automatic table creation")

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# Add exception handler for all unhandled exceptions to ensure CORS headers are present
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler that ensures CORS headers are included in error responses.
    This prevents CORS errors from masking the actual backend errors.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    # Create a JSON response with CORS headers
    response = JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )

    # Add CORS headers manually to ensure they're present
    origin = request.headers.get("origin", "").lower()
    # Normalize origins list for case-insensitive comparison
    normalized_origins = [o.lower() for o in settings.cors_origins_list]
    if origin and origin in normalized_origins:
        # Use the original case from the request
        response.headers["Access-Control-Allow-Origin"] = request.headers.get(
            "origin", ""
        )
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"

    return response


class ServiceStatus(BaseModel):
    message: str
    status: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Welcome to the HoppyBrew API",
                "status": "online",
            }
        }
    )


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
