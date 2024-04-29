from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router


def get_app() -> FastAPI:
    fast_app = FastAPI(
        title="test",
        version="0",
    )
    fast_app.include_router(router)
    return fast_app


app = get_app()

# Middleware function to add CORS headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (replace with specific origins as needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

