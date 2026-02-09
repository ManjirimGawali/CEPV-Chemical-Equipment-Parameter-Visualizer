# app/services/api.py
import requests
from app.state import AppState
import os

# Load .env file first (before reading environment variables)
try:
    from dotenv import load_dotenv
    import sys
    
    # Determine the base path (works in both dev and built versions)
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as script
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    # Try to load .env from the base path
    env_path = os.path.join(base_path, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        # Also try in PyInstaller's _MEIPASS if available
        try:
            meipass_path = os.path.join(sys._MEIPASS, '.env')
            if os.path.exists(meipass_path):
                load_dotenv(meipass_path)
        except AttributeError:
            pass
except ImportError:
    # python-dotenv not installed, skip loading .env
    pass
except Exception:
    # If .env loading fails, continue with environment variables or defaults
    pass

# Default API URL - use production URL as default, can be overridden with CEPV_API_URL
# Production URL is the default for built executables
env_url = os.getenv("CEPV_API_URL") or "https://cepv-chemical-equipment-parameter.onrender.com"

# Remove trailing slash if present
env_url = env_url.rstrip('/')

# Add /api if not already present in the URL
if not env_url.endswith('/api'):
    BASE_URL = f"{env_url}/api"
else:
    BASE_URL = env_url

# Validate BASE_URL is set (should always be set now, but check anyway)
if not BASE_URL:
    raise ValueError("CEPV_API_URL environment variable is not set and no default URL provided")

def _headers(json=True):
    headers = {}
    if json:
        headers["Content-Type"] = "application/json"
    if AppState.token:
        headers["Authorization"] = f"Token {AppState.token}"
    return headers


def login(username, password):
    res = requests.post(
        f"{BASE_URL}/auth/login/",
        json={"username": username, "password": password},
        headers=_headers(),
        timeout=60,  # Increased timeout for cold starts
    )
    res.raise_for_status()
    return res.json()


def signup(username, password):
    res = requests.post(
        f"{BASE_URL}/auth/signup/",
        json={"username": username, "password": password},
        headers=_headers(),
        timeout=60,  # Increased timeout for cold starts
    )
    res.raise_for_status()
    return res.json()


def upload_csv(file_path, name):
    with open(file_path, "rb") as f:
        res = requests.post(
            f"{BASE_URL}/upload/",
            headers=_headers(json=False),  # IMPORTANT
            files={"file": f},
            data={"name": name},
            timeout=30,
        )
    res.raise_for_status()
    return res.json()


def get_history():
    res = requests.get(
        f"{BASE_URL}/history/",
        headers=_headers(),
        timeout=60,  # Increased timeout for cold starts
    )
    res.raise_for_status()
    return res.json()


def analyze_dataset(dataset_id):
    res = requests.get(
        f"{BASE_URL}/dataset/{dataset_id}/analyze/",
        headers=_headers(),
        timeout=60,  # Increased timeout for cold starts
    )
    res.raise_for_status()
    return res.json()


def download_pdf(dataset_id, save_path):
    res = requests.get(
        f"{BASE_URL}/report/{dataset_id}/",
        headers=_headers(),
        stream=True,
    )
    res.raise_for_status()

    with open(save_path, "wb") as f:
        for chunk in res.iter_content(1024):
            f.write(chunk)
