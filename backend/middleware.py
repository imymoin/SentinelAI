import time
import uuid

from fastapi import Request

from backend.logging_config import get_logger
from backend.observability import metrics


logger = get_logger(__name__)


async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    start_time = time.perf_counter()

    logger.info(
        "Request started | request_id=%s | method=%s | path=%s",
        request_id,
        request.method,
        request.url.path,
    )

    try:
        response = await call_next(request)

        duration = time.perf_counter() - start_time

        metrics.record_request(
            duration=duration,
            success=response.status_code < 500,
        )

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "Request completed | request_id=%s | status=%s | duration_ms=%.2f",
            request_id,
            response.status_code,
            duration * 1000,
        )

        return response

    except Exception:
        duration = time.perf_counter() - start_time

        metrics.record_request(
            duration=duration,
            success=False,
        )

        logger.exception(
            "Request failed | request_id=%s | duration_ms=%.2f",
            request_id,
            duration * 1000,
        )

        raise