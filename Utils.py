from difflib import SequenceMatcher
import pandas as pd
import configparser
import os


# Update this to use your main.py coordinates
listings_url_t = 'https://www.google.com/search?sxsrf=ACYBGNS1OuAlrwXrWvHCe01W6jx80oL9jA:1581870852554&' \
                     'q={q}&npsic=0&rflfq=1&rlha=0&rllag=40.4173,-82.9071,2415&tbm=lcl&' \
                     'ved=2ahUKEwiN1fyRwNbnAhUHVBUIHdOxBdIQjGp6BAgLEFk'

details_url_t = 'https://www.google.com/async/lcl_akp?ei=N5dMXuOUC82ckgXKz634Ag&' \
                'tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u16!2m2!16m1!1e1!1m4!1u16!2m2!16m1!1e2' \
                '!2m1!1e2!2m1!1e16!2m1!1e3!3sIAE,lf:1,lf_ui:9&yv=3&lqi=Chd2ZWdhbiByZXN0YXVyYW50IHN5ZG5le' \
                'UjDmMXr9pWAgAhaNQoQdmVnYW4gcmVzdGF1cmFudBAAEAEYABgBGAIiF3ZlZ2FuIHJlc3RhdXJhbnQgc3lkbmV5&' \
                'phdesc=Z0sOfSPV1mY&vet=10ahUKEwijjPfywtznAhVNjqQKHcpnCy8Q8UEI7AI..i&' \
                'lei=N5dMXuOUC82ckgXKz634Ag&tbm=lcl&q={q}&' \
                'async=ludocids:{id},f:rlni,lqe:false,_id:akp_tsuid14,_pms:s,_fmt:pc'
G_URL = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyDD8LALkNo36hN295bcI3Wim-LUvlm5G3s"

address_columns = {
    "locality": "City",
    "administrative_area_level_1": "State",
    "postal_code": "Zip Code"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
}

config = configparser.ConfigParser()
# Try to read settings.ini from the same directory as this script
script_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(script_dir, "settings.ini")

if os.path.exists(settings_path):
    config.read(settings_path)
    proxy = int(config.get("PROXIES", "useproxy"))
    if proxy == 1:
        if config.get("PROXIES", "proxyuser") == "":
            raise Exception("Proxy Username Missing")
        if config.get("PROXIES", "proxypass") == "":
            raise Exception("Proxy Password Missing")

    proxy_user = config.get("PROXIES", "proxyuser")
    proxy_pass = config.get("PROXIES", "proxypass")

    http_proxy = f"http://{proxy_user}:{proxy_pass}@proxy.packetstream.io:31112"
    https_proxy = f"http://{proxy_user}:{proxy_pass}@proxy.packetstream.io:31112"

    proxyDict = {
        "http": http_proxy,
        "https": https_proxy,
    }

    # Crawl controls (with defaults)
    def _getf(section, key, default):
        try: return float(config.get(section, key))
        except: return float(default)
    def _geti(section, key, default):
        try: return int(config.get(section, key))
        except: return int(default)
    def _getb(section, key, default):
        try: return 1 if int(config.get(section, key)) else 0
        except: return int(default)

    if 'CRAWL' in config:
        MAX_WORKERS = _geti("CRAWL", "max_workers", 5)
        PAGE_DELAY_RANGE = (_getf("CRAWL", "page_delay_min", 2.5), _getf("CRAWL", "page_delay_max", 5.0))
        DETAIL_DELAY_RANGE = (_getf("CRAWL", "detail_delay_min", 0.4), _getf("CRAWL", "detail_delay_max", 1.0))
        LONG_PAUSE_EVERY_PAGES = _geti("CRAWL", "long_pause_every_pages", 10)
        LONG_PAUSE_RANGE = (_getf("CRAWL", "long_pause_min", 15), _getf("CRAWL", "long_pause_max", 35))
        MAX_ATTEMPTS = _geti("CRAWL", "max_attempts", 3)
        BACKOFF_BASE = _getf("CRAWL", "backoff_base", 2)
        JITTER_RANGE = (_getf("CRAWL", "jitter_min", 0.3), _getf("CRAWL", "jitter_max", 1.2))
        GEOCODE_MIN_INTERVAL = _getf("CRAWL", "geocode_min_interval", 0.2)
        AUTOSAVE_EVERY_COUNTIES = _geti("CRAWL", "autosave_every_counties", 1)
        SHUFFLE_COUNTIES = _getb("CRAWL", "shuffle_counties", 1)
        RESUME = _getb("CRAWL", "resume", 1)
    else:
        MAX_WORKERS = 5
        PAGE_DELAY_RANGE = (2.5, 5.0)
        DETAIL_DELAY_RANGE = (0.4, 1.0)
        LONG_PAUSE_EVERY_PAGES = 10
        LONG_PAUSE_RANGE = (15, 35)
        MAX_ATTEMPTS = 3
        BACKOFF_BASE = 2
        JITTER_RANGE = (0.3, 1.2)
        GEOCODE_MIN_INTERVAL = 0.2
        AUTOSAVE_EVERY_COUNTIES = 1
        SHUFFLE_COUNTIES = 1
        RESUME = 1
else:
    # Default values if settings.ini is not found
    proxy = 0
    proxyDict = {}
    print("⚠️  Warning: settings.ini not found, running without proxy")
    # Defaults for crawl controls
    MAX_WORKERS = 5
    PAGE_DELAY_RANGE = (2.5, 5.0)
    DETAIL_DELAY_RANGE = (0.4, 1.0)
    LONG_PAUSE_EVERY_PAGES = 10
    LONG_PAUSE_RANGE = (15, 35)
    MAX_ATTEMPTS = 3
    BACKOFF_BASE = 2
    JITTER_RANGE = (0.3, 1.2)
    GEOCODE_MIN_INTERVAL = 0.2
    AUTOSAVE_EVERY_COUNTIES = 1
    SHUFFLE_COUNTIES = 1
    RESUME = 1
