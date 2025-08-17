from urllib.parse import quote_plus
from scrapy import Selector
import concurrent.futures
from Utils import *
import requests
import json
import os
import time
import datetime
from credit_tracker import CreditTracker


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
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    executor.map(self.get_data, links)
                
                print(f"[SUCCESS] Data collected - Total businesses so far: {len(self.cmp)}")
                
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
        print(f"[REQUEST] Requesting: {URL[:100]}...")
        request_start = time.time()
        
        if proxy == 1:
            attempts = 0
            while True:
                attempts += 1
                try:
                    print(f"[PROXY] Proxy attempt {attempts}")
                    r = requests.get(URL, headers=headers, proxies=proxyDict, timeout=30)
                    if r.status_code == 200:
                        request_time = time.time() - request_start
                        print(f"[SUCCESS] Success in {request_time:.1f}s (attempt {attempts})")
                        break
                    else:
                        print(f"[WARNING] Status {r.status_code} (attempt {attempts})")
                except Exception as e:
                    print(f"[ERROR] Error: {e} (attempt {attempts})")
                    if attempts > 10:
                        print("[WARNING] Too many attempts, trying direct connection")
                        r = requests.get(URL, headers=headers, timeout=30)
                        break
                    continue
        else:
            r = requests.get(URL, headers=headers, timeout=30)
        
        return Selector(text=r.content)

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
            # Track credit usage for geocoding API call
            if self.credit_tracker:
                self.credit_tracker.track_query(
                    query=self.search_terms,
                    state="",  # Will be filled in main.py
                    county="",  # Will be filled in main.py
                    results_count=1
                )
            
            r = requests.get(G_URL.format(address), headers=headers)
            json_resp = json.loads(r.content)
            for item in json_resp.get("results")[0].get("address_components"):
                nm = item.get("types")[0]
                value = item.get("long_name")
                if nm == "street_number":
                    st_ad = value
                if nm == "route":
                    route = value
                nm = address_columns.get(nm)
                if not nm:
                    continue
                fnl[nm] = value
        fnl["Address"] = f"{st_ad} {route}"
        self.cmp.append(fnl)
        print(f"Scraping ------------> {name}")
