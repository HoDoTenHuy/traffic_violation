class IncludeAPIRouter(object):
    def __new__(cls):
        from routers.health_check import router as router_health_check
        from fastapi.routing import APIRouter

        router = APIRouter()
        router.include_router(router_health_check, prefix='/api/v1', tags=['Health Check'])
        return router
