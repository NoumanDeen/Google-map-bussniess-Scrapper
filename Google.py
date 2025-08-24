from urllib.parse import quote_plus
from scrapy import Selector
import concurrent.futures
from Utils import *
import requests
import json
import os
import time
import datetime
from credit_tracker import CorrectedCreditTracker
import threading
import random
from time import monotonic


UA_POOL = [
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
]

GEOCODE_CACHE_PATH = "geocode_cache.json"
_cache_lock = threading.Lock()
try:
	with open(GEOCODE_CACHE_PATH, "r", encoding="utf-8") as f:
		GEOCODE_CACHE = json.load(f)
except Exception:
	GEOCODE_CACHE = {}

_last_geocode_ts = 0.0

def geocode_with_cache(address):
	global _last_geocode_ts
	with _cache_lock:
		cached = GEOCODE_CACHE.get(address)
		if cached is not None:
			return cached

	# simple rate limit
	now = monotonic()
	wait = _last_geocode_ts + GEOCODE_MIN_INTERVAL - now
	if wait > 0:
		time.sleep(wait)

	# retry with backoff + jitter
	for attempt in range(MAX_ATTEMPTS):
		try:
			r = requests.get(G_URL.format(address), headers=headers, proxies=proxyDict, timeout=30)
			data = r.json()
			comps = data.get("results", [{}])[0].get("address_components", [])
			
			# Track Google Maps API usage (FREE, just quota)
			# Note: We need to access the credit_tracker from the Scraper instance
			# This will be handled in the get_data method
			
			with _cache_lock:
				GEOCODE_CACHE[address] = comps
				try:
					with open(GEOCODE_CACHE_PATH, "w", encoding="utf-8") as f:
						json.dump(GEOCODE_CACHE, f, indent=2, ensure_ascii=False, sort_keys=True)
						f.write("\n")
				except Exception:
					pass
			return comps
		except Exception:
			time.sleep((BACKOFF_BASE ** (attempt + 1)) + random.uniform(*JITTER_RANGE))
	return []


class Scraper:

    def __init__(self, keyword, filenm, latitude=None, longitude=None, credit_tracker=None):
        self.search_terms = keyword
        self.search_loc = keyword.split(" in ")[-1].strip()
        self.filenm = filenm
        self.cmp = []
        self.check_dup = []
        # Store coordinates for location-based searches
        self.latitude = latitude or 40.4173  # Default to Ohio center if not provided
        self.longitude = longitude or -82.9071  # Default to Ohio center if not provided
        self.credit_tracker = credit_tracker  # Add credit tracker reference

    def save_data(self):
        """Save data to Excel file - now optional"""
        if not os.path.exists("Output"):
            os.mkdir("Output")
        df = pd.DataFrame(self.cmp)
        df.to_excel(f"Output/{self.filenm}.xlsx", index=False)
        print(f"[SAVE] Data saved to: Output/{self.filenm}.xlsx")

    def get_data_only(self):
        """Return data without saving to file - for state-level collection"""
        return self.cmp.copy()

    def start(self):
        """Original start method - saves individual city files"""
        print(f"[SEARCH] Search Term --------> {self.search_terms}")
        print(f"[LOCATION] Location Coordinates -> Lat: {self.latitude}, Lng: {self.longitude}")
        
        start_time = time.time()
        page_start_time = start_time
        
        # Use location-based search URL with coordinates
        search_url = self.get_location_based_search_url()
        response = self.get_response(search_url)
        
        pg = 1
        while True:
            page_start_time = time.time()
            print(f"\n[PAGE] Scraping Page # {pg} at {datetime.datetime.now().strftime('%H:%M:%S')}")
            
            try:
                links = self.get_listings(self.search_terms, response)
                print(f"[SUCCESS] Found {len(links)} business links on page {pg}")
                
                if not links:
                    print("[WARNING] No links found - page might be empty or blocked")
                    break
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    executor.map(self.get_data, links)
                
                # Save individual city file (original behavior)
                self.save_data()
                print(f"[SUCCESS] Data saved - Total businesses so far: {len(self.cmp)}")
                
                pg += 1
                nxt_page = response.xpath("//a[contains(@id, 'pnnext')]/@href").get()
                
                if nxt_page:
                    print(f"[NEXT] Moving to next page...")
                    response = self.get_response("https://www.google.com"+nxt_page)
                    
                    # Add delay between pages
                    delay = 2
                    print(f"[WAIT] Waiting {delay} seconds before next page...")
                    time.sleep(delay)
                else:
                    print("[COMPLETE] No more pages found - search complete")
                    break
                    
            except Exception as e:
                print(f"[ERROR] Error on page {pg}: {e}")
                print(f"[TIME] Error time: {datetime.datetime.now().strftime('%H:%M:%S')}")
                break
        
        total_time = time.time() - start_time
        print(f"\n[FINISH] COMPLETED: {len(self.cmp)} businesses in {total_time:.1f} seconds")

    def start_and_return_data(self):
        """NEW METHOD: Start scraping and return data without saving files"""
        print(f"[SEARCH] Search Term --------> {self.search_terms}")
        print(f"[LOCATION] Location Coordinates -> Lat: {self.latitude}, Lng: {self.longitude}")
        
        start_time = time.time()
        page_start_time = start_time
        
        # Use location-based search URL with coordinates
        search_url = self.get_location_based_search_url()
        response = self.get_response(search_url)
        
        pg = 1
        while True:
            page_start_time = time.time()
            print(f"\n[PAGE] Scraping Page # {pg} at {datetime.datetime.now().strftime('%H:%M:%S')}")
            
            try:
                links = self.get_listings(self.search_terms, response)
                print(f"[SUCCESS] Found {len(links)} business links on page {pg}")
                
                if not links:
                    print("[WARNING] No links found - page might be empty or blocked")
                    break
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    executor.map(self.get_data, links, chunksize=1)
                
                print(f"[SUCCESS] Data collected - Total businesses so far: {len(self.cmp)}")
                
                pg += 1
                time.sleep(random.uniform(*PAGE_DELAY_RANGE))
                if pg % LONG_PAUSE_EVERY_PAGES == 0:
                    pause = random.uniform(*LONG_PAUSE_RANGE)
                    print(f"[PAUSE] Cooling down for {pause:.1f}s")
                    time.sleep(pause)
                nxt_page = response.xpath("//a[contains(@id, 'pnnext')]/@href").get()
                
                if nxt_page:
                    print(f"[NEXT] Moving to next page...")
                    response = self.get_response("https://www.google.com"+nxt_page)
                    
                    # Add delay between pages
                    delay = 2
                    print(f"[WAIT] Waiting {delay} seconds before next page...")
                    time.sleep(delay)
                else:
                    print("[COMPLETE] No more pages found - search complete")
                    break
                    
            except Exception as e:
                print(f"[ERROR] Error on page {pg}: {e}")
                print(f"[TIME] Error time: {datetime.datetime.now().strftime('%H:%M:%S')}")
                break
        
        total_time = time.time() - start_time
        print(f"\n[FINISH] COMPLETED: {len(self.cmp)} businesses in {total_time:.1f} seconds")
        
        # Return the collected data instead of saving
        return self.get_data_only()

    def get_location_based_search_url(self):
        """Generate a search URL with coordinates for more accurate local results"""
        base_url = 'https://www.google.com/search'
        params = {
            'q': self.search_terms,
            'npsic': '0',
            'rflfq': '1',
            'rlha': '0',
            'rllag': f'{self.latitude},{self.longitude},2415',  # Coordinates with radius
            'tbm': 'lcl',
            'ved': '2ahUKEwiN1fyRwNbnAhUHVBUIHdOxBdIQjGp6BAgLEFk'
        }
        
        # Build query string
        query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        return f"{base_url}?{query_string}"

    def get_response(self, URL: str):
        ua = random.choice(UA_POOL)
        local_headers = dict(headers)
        local_headers["User-Agent"] = ua

        attempts = 0
        while attempts < MAX_ATTEMPTS:
            attempts += 1
            try:
                if proxy == 1:
                    r = requests.get(URL, headers=local_headers, proxies=proxyDict, timeout=30)
                    # Track PacketStream usage (REAL COSTS)
                    if hasattr(self, 'credit_tracker') and self.credit_tracker:
                        response_size = len(r.content)
                        self.credit_tracker.track_packetstream_request(response_size)
                else:
                    r = requests.get(URL, headers=local_headers, timeout=30)

                status = r.status_code
                txt = r.text[:600].lower()

                if status in (429, 503) or "unusual traffic" in txt or "sorry" in txt:
                    wait = (BACKOFF_BASE ** attempts) + random.uniform(*JITTER_RANGE)
                    print(f"[BACKOFF] {status}/block detected. Sleeping {wait:.1f}s (attempt {attempts})")
                    time.sleep(wait)
                    continue

                if status != 200:
                    wait = (BACKOFF_BASE ** attempts) + random.uniform(*JITTER_RANGE)
                    print(f"[RETRY] HTTP {status}. Sleeping {wait:.1f}s (attempt {attempts})")
                    time.sleep(wait)
                    continue

                return Selector(text=r.content)

            except Exception as e:
                wait = (BACKOFF_BASE ** attempts) + random.uniform(*JITTER_RANGE)
                print(f"[ERROR] {e}. Sleeping {wait:.1f}s (attempt {attempts})")
                time.sleep(wait)

        if proxy == 1:
            try:
                r = requests.get(URL, headers=local_headers, timeout=30)
                return Selector(text=r.content)
            except Exception as e:
                print(f"[FATAL] Could not fetch after retries: {e}")
        else:
            print("[FATAL] Could not fetch after retries.")
        return Selector(text="")

    def get_listings(self, search_term, response: Selector):
        cmp = []
        # for listing_selector in response.css('div div[jsname="GZq3Ke"]div div[jsname="jXK9ad"]'):
        for listing_selector in response.css('div div[jsname="jXK9ad"]'):
            listing_id = listing_selector.css('a::attr(data-cid)').get()
            if listing_id not in self.check_dup:
                self.check_dup.append(listing_id)
                details_url = details_url_t.format(q=quote_plus(search_term), id=listing_id)
                cmp.append(details_url)
        return cmp

    def get_data(self, url: str):
        time.sleep(random.uniform(*DETAIL_DELAY_RANGE))
        response = self.get_response(url)
        name = response.css('h2[data-attrid="title"] span::text').get()
        address = response.css('.w8qArf:contains(Address) + .LrzXr::text').get()
        if not address:
            address = response.xpath("//span[contains(*, 'Address')]/following::span[1]/text()").get()
        phone = response.css('span:contains("Phone") + span a span::text').get()
        hours = ', '.join(
            [f"{row.css('td::text').get()}: {row.css('td+td::text').get('').replace('–', '-')}" for row in
             response.css('table.WgFkxc tr')])
        website = response.css('a:contains("Website")::attr(href)').re_first(r'q=(.*)/') or response.css(
            'a:contains("Website")::attr(href)').get()
        rating = response.css('.Aq14fc::text').get('0') + '/5'
        reviews = response.css('.hqzQac [data-sort_by="qualityScore"] span::text').get('')
        cate = " ".join(response.xpath("//span[contains(@class, 'YhemCb')]//text()").getall()).split(" in ")[0].strip()
        
        fnl = {
            "Name": name,
            "Category": cate,
            "Phone Number": phone,
            "Hours": hours,
            "Website": website,
            "Rating": rating,
            "Address": address,
            "City": "",
            "State": "",
            "Zip Code": ""
        }
        
        st_ad, route = "", ""
        if address:
            # Track Google Maps API usage (FREE, just quota)
            if hasattr(self, 'credit_tracker') and self.credit_tracker:
                self.credit_tracker.track_google_api_request()
            
            comps = geocode_with_cache(address)
            for item in comps:
                nm = item.get("types", [""])[0]
                value = item.get("long_name")
                if nm == "street_number": st_ad = value
                if nm == "route": route = value
                nm = address_columns.get(nm)
                if not nm: continue
                fnl[nm] = value
        fnl["Address"] = f"{st_ad} {route}"
        self.cmp.append(fnl)
        print(f"Scraping ------------> {name}")
