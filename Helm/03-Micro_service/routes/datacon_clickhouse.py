from typing import List, Dict, Any
from dotenv import load_dotenv
import logging
import requests
import json
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_clickhouse_data(
    limit: int = None, filters: dict = None
) -> List[Dict[str, Any]]:
    """
    Query ClickHouse database with dynamic filters
    """
    try:
        url = os.getenv("CLICKHOUSE_URL")
        auth = (os.getenv("CLICKHOUSE_USER"), os.getenv("CLICKHOUSE_PASSWORD"))

        base_query = "SELECT * FROM dtc_params"

        if filters:
            where_conditions = []
            for column, value in filters.items():
                if value:
                    if "," in value:
                        values = [
                            f"'{v.strip()}'" for v in value.split(",") if v.strip()
                        ]
                        where_conditions.append(f"{column} IN ({','.join(values)})")
                    else:
                        where_conditions.append(f"{column} = '{value}'")

            if where_conditions:
                base_query += f" WHERE {' AND '.join(where_conditions)}"

        query = f"{base_query}"
        if limit is not None:
            query += f" LIMIT {limit}"
        query += " FORMAT JSONEachRow"

        response = requests.post(url, data=query, auth=auth, timeout=30)

        if response.status_code != 200:
            logger.error(
                f"ClickHouse HTTP error {response.status_code}: {response.text}"
            )
            raise Exception(f"HTTP {response.status_code}: {response.text}")

        data_records = []
        for line in response.text.strip().split("\n"):
            if line:
                record = json.loads(line)
                data_records.append(record)

        return data_records

    except Exception as e:
        logger.error(f"ClickHouse query error: {str(e)}")
        raise
