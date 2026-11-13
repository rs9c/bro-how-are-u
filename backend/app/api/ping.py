from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter(tags=["debug"])

class PingReq(BaseModel):
    req: str
    repeat: int | None = None

@router.post("/ping")
async def post_ping(req: PingReq):
    '''
    想和后端打乒乓吗？多来几个！
    '''
    if req.req != "Ping":
        return JSONResponse(status_code=400, content={"msg": "req请求格式错误"})
    resp = "POST Pong!"
    if req.repeat is not None and req.repeat > 1 and req.repeat < 101:
        for _ in range(req.repeat - 1):
            resp += "Pong!"
    return {"msg": resp}

@router.get("/ping")
async def get_ping():
    '''
    想和后端打乒乓吗？
    '''
    return {"msg": "GET Pong!"}