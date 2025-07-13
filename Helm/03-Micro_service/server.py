import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
import pytz

# Port selection
if len(sys.argv) > 1:
    try:
        port = int(sys.argv[1])
    except ValueError:
        port = 4000
else:
    port = int(os.getenv("PORT", 4000))

app = FastAPI(
    title="ClickHouse Data API",
    description="API for retrieving ClickHouse data",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.datacon_clickhouse_endpoints import router as datacon_clickhouse_routers

app.include_router(datacon_clickhouse_routers, prefix="/api", tags=["ClickHouse Data"])


@app.get("/")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    local_tz = pytz.timezone("Asia/Bangkok")
    local_time = datetime.now(local_tz)
    print(
        f"API Server running at http://localhost:{port} - {local_time.strftime('%m/%d/%Y, %I:%M:%S %p')}"
    )
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
