import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.utils.dbUtil import database
from api.auth import router as auth_router
from api.otps import router as otp_router
from api.users import router as user_router
from api.books import router as book_router
from api.exceptions.business import BusinessException

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="FastAPI (python)",
    description="FastAPI framework, high performance, <br>"
                "easy to learn, fast to code, ready for production",
    version="1.0",
    openapi_url="/openapi.json",
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request.state.connection = database
    response = await call_next(request)
    start_time = time.time()
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)

    return response


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, e: BusinessException):
    return JSONResponse(
        status_code=418,
        content={"code": e.status_code, "message": e.detail},
    )


app.include_router(auth_router.router, tags=["Auth"])
app.include_router(otp_router.router, tags=["OTP"])
app.include_router(user_router.router, tags=["User"])
app.include_router(book_router.router, tags=["Reservation"])
