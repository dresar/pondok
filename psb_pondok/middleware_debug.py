import json
import time
import os
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

LOG_PATH = r"c:\Users\eka\Downloads\pondok\.cursor\debug.log"
SESSION_ID = "debug-session"


class DebugRequestLogMiddleware(MiddlewareMixin):
    """
    Middleware debug untuk mencatat request masuk dan view resolver.
    Tidak mengeksekusi apa pun selain append log NDJSON ke LOG_PATH.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        # region agent log
        entry = {
            "sessionId": SESSION_ID,
            "runId": "pre-fix",
            "hypothesisId": "H1",  # apakah request admin-panel sampai ke Django
            "location": "middleware_debug.py:process_view",
            "message": "process_view",
            "data": {
                "path": request.path,
                "method": request.method,
                "resolver_match": request.resolver_match.view_name if request.resolver_match else None,
            },
            "timestamp": int(time.time() * 1000),
        }
        try:
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass
        # endregion

        # region agent log
        if request.path.startswith(settings.MEDIA_URL):
            rel_path = request.path[len(settings.MEDIA_URL):].lstrip('/')
            full_path = os.path.join(settings.MEDIA_ROOT, rel_path)
            entry_media = {
                "sessionId": SESSION_ID,
                "runId": "pre-fix",
                "hypothesisId": "H3",  # cek file media ada/tidak
                "location": "middleware_debug.py:process_view",
                "message": "media_check",
                "data": {
                    "path": request.path,
                    "full_path": full_path,
                    "exists": os.path.exists(full_path),
                    "is_file": os.path.isfile(full_path),
                },
                "timestamp": int(time.time() * 1000),
            }
            try:
                with open(LOG_PATH, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry_media) + "\n")
            except Exception:
                pass
        # endregion

        # region agent log
        if request.method == "POST" and request.FILES:
            files_info = []
            for name, file_obj in request.FILES.items():
                files_info.append({
                    "field": name,
                    "filename": getattr(file_obj, 'name', ''),
                    "size": getattr(file_obj, 'size', None),
                    "content_type": getattr(file_obj, 'content_type', ''),
                })
            entry_files = {
                "sessionId": SESSION_ID,
                "runId": "pre-fix",
                "hypothesisId": "H4",  # apakah upload diterima Django
                "location": "middleware_debug.py:process_view",
                "message": "upload_received",
                "data": {
                    "path": request.path,
                    "media_root": str(settings.MEDIA_ROOT),
                    "files": files_info,
                },
                "timestamp": int(time.time() * 1000),
            }
            try:
                with open(LOG_PATH, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry_files) + "\n")
            except Exception:
                pass
        # endregion
        return None

    def process_response(self, request, response):
        # region agent log
        entry = {
            "sessionId": SESSION_ID,
            "runId": "pre-fix",
            "hypothesisId": "H2",  # status_code dari response
            "location": "middleware_debug.py:process_response",
            "message": "process_response",
            "data": {
                "path": getattr(request, "path", None),
                "status_code": getattr(response, "status_code", None),
            },
            "timestamp": int(time.time() * 1000),
        }
        try:
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass
        # endregion
        return response

