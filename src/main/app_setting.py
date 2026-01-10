from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from common.database import SessionLocal
from common.redis.redis_client import RedisClient
from domain.member.controller import router as member_router
from domain.organization.organization.controller import router as organization_router
from common.dependency_injector import Container
from domain.organization.organization_invitation.controller import router as organization_invitation_router
from domain.organization.joined_organization.controller import router as joined_organization_router
from domain.file.file.controller import router as file_router
from domain.ledger.category.category.controller import router as category_router
from domain.ledger.category.item.controller import router as category_item_router
from domain.ledger.event.controller import router as event_router
from domain.ledger.receipt.controller import router as receipt_router
from domain.file.word.controller import router as word_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await RedisClient.init()
    try:
        yield
    finally:
        await RedisClient.close()



app = FastAPI(
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan
)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    async with SessionLocal() as session:
        request.state.db = session
        try:
            response = await call_next(request)
            if response.status_code >=400:
                await request.state.db.rollback()
            else:
                await request.state.db.commit()
        except Exception as e:
            await request.state.db.rollback()
            raise e
    return response

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(member_router)
app.include_router(organization_router)
app.include_router(organization_invitation_router)
app.include_router(joined_organization_router)
app.include_router(file_router)
app.include_router(category_router)
app.include_router(category_item_router)
app.include_router(event_router)
app.include_router(receipt_router)
app.include_router(word_router)

app.mount("/static", StaticFiles(directory="./static"))

container = Container()

container.wire(
    modules=container.wiring_config.modules,
    packages=container.wiring_config.packages
)
app.container = container