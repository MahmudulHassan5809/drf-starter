import json
import logging
from json import JSONDecodeError
from urllib.parse import parse_qs

logger = logging.getLogger(__name__)


class RequestResponseLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        data = {
            'method': request.method,
            'headers': dict(request.headers),
            'query_params': dict(request.GET),
        }
        path = str(request.get_full_path()).replace(
            '/api/v1.0/', '').replace('/', '-').upper()
        data['requested_endpoint'] = path
        if hasattr(request, 'body') and request.body:
            try:
                data['request_body'] = json.loads(request.body.decode('utf-8'))
            except JSONDecodeError:
                data['request_body'] = parse_qs(request.body.decode('utf-8'))
            except UnicodeDecodeError:
                pass
        response = self.get_response(request)
        if hasattr(response, 'data'):
            data['response_body'] = response.data
        data['status'] = response.status_code
        if data['status'] // 100 == 5:
            logger.error(json.dumps(data))
        else:
            logger.info(json.dumps(data))
        return response
