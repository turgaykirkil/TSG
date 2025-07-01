import asyncio
from fastapi import APIRouter
from starlette.responses import JSONResponse
import subprocess
import os
import sys
import traceback

router = APIRouter()

@router.post("/scraping/open-site")
async def open_site():
    """
    Chromium'da ticaretsicil.gov.tr açılır, session kullanıcıda tutulur.
    Hata durumunda stdout/stderr ve path bilgisi döner.
    """
    print("\n========== API REQUEST: /api/scraping/open-site (POST) ==========")
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "scraping_chromium.py"))
    python_exec = sys.executable or "python"
    logs = {}
    logs['cwd'] = os.getcwd()
    logs['script_path'] = script_path
    logs['python_exec'] = python_exec
    logs['env'] = dict(os.environ)

    if not os.path.exists(script_path):
        logs['error'] = f"Script bulunamadı: {script_path}"
        print("[scraping_api] HATA - Script bulunamadı:", logs)
        print("========== END API REQUEST ==========")
        return JSONResponse({"status": "error", "logs": logs}, status_code=500)
    try:
        process = subprocess.Popen(
            [python_exec, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd(),
            env=os.environ.copy()
        )
        logs['pid'] = process.pid
        print(f"[scraping_api] Chromium açılıyor, PID: {process.pid}")
        print("========== END API REQUEST ==========")
        return JSONResponse({"status": "started", "logs": logs})
    except Exception as e:
        logs['exception'] = str(e)
        logs['traceback'] = traceback.format_exc()
        print(f"[scraping_api] HATA: {logs}")
        print("========== END API REQUEST ==========")
        return JSONResponse({"status": "error", "logs": logs}, status_code=500)
