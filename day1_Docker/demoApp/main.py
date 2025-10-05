from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import pathlib

app = FastAPI()

# Mount a static files directory at /static
app.mount("/static", StaticFiles(directory=str(pathlib.Path(__file__).parent / "static")), name="static")


@app.get("/favicon.ico")
def favicon():
    """Serve the SVG favicon from the static directory."""
    return FileResponse(pathlib.Path(__file__).parent / "static" / "favicon.svg", media_type="image/svg+xml")


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}

@app.get("/healthz")
def healthz():
    return JSONResponse(content={"status": "ok"})

@app.get("/readiness")
def readiness():
    return JSONResponse(content={"status": "ready"})
