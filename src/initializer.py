class IncludeAPIRouter(object):
    def __new__(cls):
        from routers.health_check import router as router_health_check
        from routers.vehicle_tracking import router as router_vehicle_tracking
        from routers.object_detection import router as router_object_detection
        from routers.streaming import router as router_streaming
        from fastapi.routing import APIRouter

        router = APIRouter()
        router.include_router(router_health_check, prefix='/api/v1', tags=['Health Check'])
        router.include_router(router_vehicle_tracking, prefix='/api/v1', tags=['Vehicle Tracking'])
        router.include_router(router_object_detection, prefix='/api/v1', tags=['Object Detection'])
        router.include_router(router_streaming, prefix='/api/v1', tags=['Streaming'])
        return router
