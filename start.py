from __init__ import *
from api import *

if __name__ == "__main__":
    logger.info("启动API应用")
    import uvicorn
    from fastapi.openapi.utils import get_openapi

    # Configure Swagger UI
    api.title = "Furina API"
    api.description = "我的爬虫API接口"
    api.version = "1.0.0"
    
    # Generate API docs
    def custom_openapi():
        if api.openapi_schema:
            return api.openapi_schema
        openapi_schema = get_openapi(
            title=api.title,
            version=api.version,
            description=api.description,
            routes=api.routes,
        )
        api.openapi_schema = openapi_schema
        return api.openapi_schema

    api.openapi = custom_openapi

    # Run the app
    uvicorn.run(api, host="127.0.0.1", port=8000)
    logger.info("关闭了API应用")