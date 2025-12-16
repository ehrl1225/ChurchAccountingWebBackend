from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from domain.member.controller import router as member_router
from domain.organization.organization.controller import router as organization_router
from common.dependency_injector import Container
from domain.organization.organization_invitation.controller import router as organization_invitation_router
from domain.organization.joined_organization.controller import router as joined_organization_router

app = FastAPI(
    docs_url="/docs",
    redoc_url=None
)

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

container = Container()

container.wire(
    modules=container.wiring_config.modules,
    packages=container.wiring_config.packages
)

app.container = container
