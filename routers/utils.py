import json
from threading import local
from fastapi import APIRouter
import socket

router = APIRouter(
    prefix="/utils",
    tags=["utils"],
    responses={404: {"description": "Not found"}}
)

# another implementation
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    localhost = s.getsockname()[0]
    s.close()
    return str(localhost)

    
@router.get("/ipaddress")
async def utils_ipaddress() -> str :
    """Returns the private ipaddress of localhost
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return str(IP)