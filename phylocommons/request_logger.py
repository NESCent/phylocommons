import time
from logging import getLogger

class LoggingMiddleware(object):
    def __init__(self):
        self.logger = getLogger('phylocommons.request')

    def process_request(self, request):
        request.timer = time.time()
        return None

    def process_response(self, request, response):
        self.logger.info(
            '[%s] [%s] %s (%.1fs)',
            time.strftime("%a %m/%d/%y %I:%M:%S %p", time.localtime()),
            response.status_code,
            request.get_full_path(),
            (time.time() - request.timer) if hasattr(request, 'timer') else -1
        )
        return response
