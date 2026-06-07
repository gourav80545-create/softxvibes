import asyncio
import requests
from urllib.parse import urlsplit

try:
    from config import COOKIE_URL
except ImportError:
    COOKIE_URL = ""

# Global variable to store cookies in memory
COOKIES_CACHE = None


def _extract_paste_id(url: str) -> str:
    path = urlsplit(url).path.rstrip("/")
    parts = [p for p in path.split("/") if p]
    return parts[-1] if parts else ""


def resolve_raw_cookie_url(url: str) -> str:
    url = (url or "").strip()
    low = url.lower()

    if "pastebin.com/" in low and "/raw/" not in low:
        paste_id = _extract_paste_id(url)
        return f"https://pastebin.com/raw/{paste_id}" if paste_id else url

    if "batbin.me/" in low and "/raw/" not in low:
        paste_id = _extract_paste_id(url)
        return f"https://batbin.me/raw/{paste_id}" if paste_id else url

    return url


async def fetch_cookies():
    """Fetch cookies from URL and store in memory"""
    global COOKIES_CACHE
    
    if not COOKIE_URL:
        print("⚠️ COOKIE_URL not set in environment.")
        return None

    raw_url = resolve_raw_cookie_url(COOKIE_URL)

    try:
        response = await asyncio.to_thread(
            requests.get,
            raw_url,
            timeout=15,
            headers={"User-Agent": "softxvibes-cookie-fetcher/1.0"},
        )
        response.raise_for_status()
    except Exception as e:
        print(f"⚠️ Can't fetch cookies: {e}")
        return None

    cookies = (response.text or "").strip()

    if not cookies.startswith("# Netscape"):
        print("⚠️ Invalid cookie format. Needs Netscape format.")
        return None

    if len(cookies) < 100:
        print("⚠️ Cookie content too short. Possibly invalid.")
        return None

    COOKIES_CACHE = cookies
    print(f"✅ Cookies fetched and stored in memory")
    return cookies


def get_cookies():
    """Get cookies from cache"""
    return COOKIES_CACHE
