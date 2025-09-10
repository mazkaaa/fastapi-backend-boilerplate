from fastapi import FastAPI

from app.routers.items import router as items_router


tags_metadata = [
	{
		"name": "health",
		"description": "Service health and readiness checks.",
	},
	{
		"name": "items",
		"description": "CRUD operations over in-memory Items. This is a DB-free example suitable for boilerplates and demos.",
	},
]

app = FastAPI(
	title="FastAPI Boilerplate",
	version="0.1.0",
	description=(
		"A minimal FastAPI boilerplate featuring an in-memory CRUD for Items. "
		"Use this as a starting point before adding real persistence."
	),
	openapi_tags=tags_metadata,
	docs_url="/docs",
	redoc_url="/redoc",
	openapi_url="/openapi.json",
	contact={
		"name": "Backend Team",
		"url": "https://example.com",
		"email": "backend@example.com",
	},
	license_info={
		"name": "MIT",
		"url": "https://opensource.org/licenses/MIT",
	},
	terms_of_service="https://example.com/terms",
)


@app.get("/health", tags=["health"], summary="Health check", description="Simple health endpoint returning a static status.")
def health_check():
	return {"status": "ok"}


# API Routers
app.include_router(items_router, prefix="/api")


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
