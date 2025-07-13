from typing import Optional, Dict, Any
import logging
from fastapi import APIRouter, HTTPException, Query, Body, Request
from pydantic import BaseModel
from routes.datacon_clickhouse import get_clickhouse_data

logger = logging.getLogger(__name__)
router = APIRouter()


class ClickHouseRequest(BaseModel):
    filters: Optional[Dict[str, str]] = None
    limit: Optional[int] = 50


@router.get("/datacon_clickhouse")
def get_clickhouse_table_data(
    request: Request,
    limit: Optional[int] = Query(
        None, description="Maximum number of records to return"
    ),
):
    try:
        # Extract all query parameters except 'limit' as filters
        filters = {}
        for key, value in request.query_params.items():
            if key != "limit":
                filters[key] = value

        # Use limit=None to remove LIMIT clause
        actual_limit = limit if limit is not None else None
        results = get_clickhouse_data(actual_limit, filters if filters else None)
        return results
    except Exception as error:
        logger.error(f"Error querying ClickHouse: {error}")
        raise HTTPException(
            status_code=500, detail=f"Failed to query ClickHouse table: {str(error)}"
        )


@router.post("/datacon_clickhouse")
def post_clickhouse_table_data(request: Dict[str, Any] = Body(...)):
    try:
        # Extract limit
        limit = request.pop("limit", None)

        # Everything else becomes filters
        filters = {k: v for k, v in request.items() if v is not None}

        results = get_clickhouse_data(limit, filters if filters else None)
        return results
    except Exception as error:
        logger.error(f"Error querying ClickHouse: {error}")
        raise HTTPException(
            status_code=500, detail=f"Failed to query ClickHouse table: {str(error)}"
        )