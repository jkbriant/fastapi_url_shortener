from fastapi import FastAPI, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from schemas import URLCreate, URLResponse

import string
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

url_mapping: dict[str, str] = {}
url_reverse_mapping: dict[str, str] = {}

def get_unique_short_url(length: int = 6):
    while True:
        chars = string.ascii_letters + string.digits
        short_url = "".join(random.choice(chars) for _ in range(length))
        if short_url not in url_mapping:
            return short_url

for i in range(0, 100):
    short_url = get_unique_short_url()
    url_mapping[short_url] = "https://www.test.com"
    url_reverse_mapping["https://www.test.com"] = short_url

## ROUTES

@app.get("/")
def home(request: Request):
    posts = [
        {"title": short_url, "content": long_url}
        for short_url, long_url in url_mapping.items()
    ]
    return templates.TemplateResponse(
        request, "home.html", {"posts": posts[:10]}
    )

@app.post(
    "/api/shorten", 
    response_model=URLResponse, 
    status_code=status.HTTP_201_CREATED
)
def shorten_url(url: URLCreate):
    # Normalize URL by adding https:// if not present
    long_url = url.url
    if not long_url.startswith(("http://", "https://")):
        long_url = "https://" + long_url
    
    if long_url in url_reverse_mapping:
        return {"short_url": url_reverse_mapping[long_url], "long_url": long_url}

    short_url = get_unique_short_url()
    url_mapping[short_url] = long_url
    url_reverse_mapping[long_url] = short_url
    return {"short_url": short_url, "long_url": long_url}

@app.get("/api/get_url/{short_url}", response_model=URLResponse)
def get_long_url(short_url: str):
    if short_url not in url_mapping:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")            

    long_url = url_mapping[short_url]
    return {"short_url": short_url, "long_url": long_url}

@app.get("/r/{short_url}")
def redirect_to_long_url(short_url: str, request: Request):
    if short_url not in url_mapping:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")

    long_url = url_mapping[short_url]
    return RedirectResponse(long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@app.get("/api/list_urls", response_model=list[URLResponse])
def list_urls():
    """List all shortened URLs and their corresponding long URLs"""
    result = []
    for short, original in url_mapping.items():
        result.append({"short_url": short, "long_url": original})
    return result

## ERROR HANDLING

@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )