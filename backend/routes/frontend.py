import pathlib
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter
from slowapi.util import get_remote_address
from rich.console import Console

# --- Constants --- #

console = Console()
app = APIRouter(prefix="/frontend", tags=["frontend"])
frontend = pathlib.Path(__file__).parent.parent.parent.joinpath("frontend")
limiter = Limiter(key_func=get_remote_address)
app.mount("/static", StaticFiles(directory=frontend.joinpath("static")), name="static")
templates = Jinja2Templates(directory=frontend.joinpath("templates"))

# --- Routes --- #


@limiter.limit("10/minute")
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ----------------------------------------------------------------------------- #
