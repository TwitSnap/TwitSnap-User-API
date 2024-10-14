import httpx
from config.settings import logger
from typing import Optional, Dict, Any

class Requester:
    @staticmethod
    async def post(url: str, headers: Optional[Dict[str, str]] = None, json_body: Optional[Dict[str, Any]] = None) -> Any:
        async with httpx.AsyncClient() as client:
            logger.debug(f"Attempting POST request to {url} - request_body:{json_body}")
            response = await client.post(url, headers=headers, json=json_body)
            logger.debug(f"Attempt POST request to {url} - status code {response.status_code}")
            response.raise_for_status()
            return response

