import logging
import time

logger = logging.getLogger(__name__)


class RequestTimingMiddleware:
    """
    Log how long each request takes.
    Keeps behavior the same, only adds timing info to logs.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "Request %s %s took %.2f ms",
            request.method,
            request.path,
            duration_ms,
        )
        return response

