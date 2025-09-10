from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.items import router as items_router
from app.core.settings import get_settings


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

_settings = get_settings()

app = FastAPI(
	title=_settings.app_name,
	version=_settings.version,
	description=(
		"A minimal FastAPI boilerplate featuring an in-memory CRUD for Items. "
		"Use this as a starting point before adding real persistence."
	),
	openapi_tags=tags_metadata,
	docs_url=_settings.docs_url,
	redoc_url=_settings.redoc_url,
	openapi_url=_settings.openapi_url,
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
# CORS (allow all by default; configure via env)
app.add_middleware(
	CORSMiddleware,
	allow_origins=[str(o) for o in _settings.cors_allow_origins],
	allow_credentials=_settings.cors_allow_credentials,
	allow_methods=_settings.cors_allow_methods,
	allow_headers=_settings.cors_allow_headers,
)


@app.get("/health", tags=["health"], summary="Health check", description="Simple health endpoint returning a static status.")
def health_check():
	return {"status": "ok"}


# API Routers
app.include_router(items_router, prefix="/api")


if __name__ == "__main__":
	import uvicorn

	uvicorn.run(
		"app.main:app",
		host=_settings.host,
		port=_settings.port,
		reload=_settings.debug,
	)
