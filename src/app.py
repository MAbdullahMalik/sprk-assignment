import uvicorn
from fastapi import FastAPI, Depends
from fastapi.requests import Request
import logging

from routes.v1.api import router
from schemas import HealthResponse

app = FastAPI()
logging.basicConfig(filename='sprk.log', level=logging.DEBUG)


async def log_request(request: Request):
    logging.info(f"{request.method} {request.url}")
    logging.info(await request.body())


app.include_router(router=router, prefix="/v1", dependencies=[Depends(log_request)])


@app.get("/", response_model=HealthResponse)
async def health():
    return HealthResponse(status="Healthy")


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000)
