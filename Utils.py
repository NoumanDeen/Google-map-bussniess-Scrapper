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
else:
    # Default values if settings.ini is not found
    proxy = 0
    proxyDict = {}
    print("⚠️  Warning: settings.ini not found, running without proxy")


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()*100
