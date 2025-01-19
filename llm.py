from crewai import LLM
from time import sleep
from typing import Any, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RateLimitedLLM(LLM):
    def __init__(self, model: str, api_key: str, retry_delay: int = 1, max_retries: int = 3):
        super().__init__(model=model, api_key=api_key)
        self.retry_delay = retry_delay
        self.max_retries = max_retries
    
    async def generate(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        for attempt in range(self.max_retries):
            try:
                return await super().generate(*args, **kwargs)
            except Exception as e:
                if "rate_limit_exceeded" in str(e):
                    wait_time = self.retry_delay * (attempt + 1)
                    logger.warning(f"Rate limit hit. Waiting {wait_time}s before retry...")
                    sleep(wait_time)
                    continue
                raise e
        raise Exception(f"Failed after {self.max_retries} attempts")