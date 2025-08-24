#!/usr/bin/env python3
"""
Corrected Credit Tracker - Integrated Version
Tracks real PacketStream costs and Google Maps API usage during scraping
"""

import json
import os
import time
from datetime import datetime
import requests

class CorrectedCreditTracker:
    def __init__(self, api_key=None, proxy_user=None, proxy_pass=None):
        self.api_key = api_key
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        self.start_time = time.time()
        
        # PacketStream tracking (REAL COSTS)
        self.packetstream_data_used_mb = 0
        self.packetstream_data_used_gb = 0
        self.packetstream_cost = 0
        self.packetstream_requests_made = 0
        self.packetstream_requests_failed = 0
        self.packetstream_cost_per_gb = 0.48  # $0.48 per GB
        
        # Google Maps API tracking (QUOTA, NOT COSTS)
        self.google_api_requests_made = 0
        self.google_api_quota_status = "Unknown"
        self.google_api_free_tier_limit = 1000  # Free tier: 1000 requests/month
        
        # Session tracking
        self.query_stats = {}
        self.state_stats = {}
        self.last_proxy_check = None
        
        # Load existing stats if available
        self.load_stats()
        
        # Check initial status
        if self.api_key:
            self.check_google_api_status()
        self.check_packetstream_status()
    
    def load_stats(self):
        """Load existing statistics from file"""
        try:
            if os.path.exists("corrected_credit_stats.json"):
                with open("corrected_credit_stats.json", "r") as f:
                    data = json.load(f)
                    
                    # Load PacketStream stats
                    self.packetstream_data_used_mb = data.get("packetstream_data_used_mb", 0)
                    self.packetstream_data_used_gb = data.get("packetstream_data_used_gb", 0)
                    self.packetstream_cost = data.get("packetstream_cost", 0)
                    self.packetstream_requests_made = data.get("packetstream_requests_made", 0)
                    
                    # Load Google API stats
                    self.google_api_requests_made = data.get("google_api_requests_made", 0)
                    
                    # Load other stats (convert lists back to sets)
                    self.query_stats = {}
                    for query, stats in data.get("query_stats", {}).items():
                        self.query_stats[query] = {
                            "total_businesses": stats.get("total_businesses", 0),
                            "states": set(stats.get("states", [])),  # Convert list to set
                            "counties": set(stats.get("counties", [])),  # Convert list to set
                            "last_used": stats.get("last_used")
                        }
                    
                    self.state_stats = {}
                    for state, stats in data.get("state_stats", {}).items():
                        self.state_stats[state] = {
                            "total_businesses": stats.get("total_businesses", 0),
                            "counties": set(stats.get("counties", [])),  # Convert list to set
                            "queries": set(stats.get("queries", [])),    # Convert list to set
                            "last_used": stats.get("last_used")
                        }
                    
                    print(f"📊 Loaded existing stats:")
                    print(f"   PacketStream: {self.packetstream_data_used_gb:.2f} GB used, ${self.packetstream_cost:.2f}")
                    print(f"   Google API: {self.google_api_requests_made} requests made")
                    
        except Exception as e:
            print(f"⚠️  Could not load existing stats: {e}")
    
    def save_stats(self):
        """Save current statistics to file"""
        try:
            # Convert sets to lists for JSON serialization
            query_stats_json = {}
            for query, stats in self.query_stats.items():
                query_stats_json[query] = {
                    "total_businesses": stats["total_businesses"],
                    "states": list(stats["states"]),  # Convert set to list
                    "counties": list(stats["counties"]),  # Convert set to list
                    "last_used": stats["last_used"]
                }
            
            state_stats_json = {}
            for state, stats in self.state_stats.items():
                state_stats_json[state] = {
                    "total_businesses": stats["total_businesses"],
                    "counties": list(stats["counties"]),  # Convert set to list
                    "queries": list(stats["queries"]),    # Convert set to list
                    "last_used": stats["last_used"]
                }
            
            data = {
                "last_updated": datetime.now().isoformat(),
                
                # PacketStream stats
                "packetstream_data_used_mb": self.packetstream_data_used_mb,
                "packetstream_data_used_gb": self.packetstream_data_used_gb,
                "packetstream_cost": self.packetstream_cost,
                "packetstream_requests_made": self.packetstream_requests_made,
                "packetstream_requests_failed": self.packetstream_requests_failed,
                "packetstream_cost_per_gb": self.packetstream_cost_per_gb,
                
                # Google API stats
                "google_api_requests_made": self.google_api_requests_made,
                "google_api_quota_status": self.google_api_quota_status,
                "google_api_free_tier_limit": self.google_api_free_tier_limit,
                
                # Other stats (converted to JSON-serializable format)
                "query_stats": query_stats_json,
                "state_stats": state_stats_json,
                "session_duration": time.time() - self.start_time
            }
            
            with open("corrected_credit_stats.json", "w") as f:
                json.dump(data, f, indent=2)
            
        except Exception as e:
            print(f"❌ Error saving stats: {e}")
    
    def check_google_api_status(self):
        """Check Google Maps API quota status (FREE)"""
        if not self.api_key:
            return
        
        try:
            test_url = f"https://maps.googleapis.com/maps/api/geocode/json?address=test&key={self.api_key}"
            response = requests.get(test_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "UNKNOWN")
                
                if status == "OK" or status == "ZERO_RESULTS":
                    remaining = max(0, self.google_api_free_tier_limit - self.google_api_requests_made)
                    self.google_api_quota_status = f"Available ({remaining} requests remaining)"
                elif status == "OVER_QUERY_LIMIT":
                    self.google_api_quota_status = "Quota Exceeded"
                elif status == "REQUEST_DENIED":
                    self.google_api_quota_status = "Invalid Key"
                else:
                    self.google_api_quota_status = f"Status: {status}"
                    
        except Exception as e:
            print(f"❌ Error checking Google Maps API: {e}")
    
    def check_packetstream_status(self):
        """Check PacketStream proxy status"""
        if not self.proxy_user or not self.proxy_pass:
            return
        
        try:
            test_url = "http://httpbin.org/ip"
            proxy_url = f"http://{self.proxy_user}:{self.proxy_pass}@proxy.packetstream.io:31112"
            
            proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
            
            response = requests.get(test_url, proxies=proxies, timeout=15)
            
            if response.status_code == 200:
                self.last_proxy_check = datetime.now().isoformat()
                
        except Exception as e:
            print(f"❌ PacketStream test error: {e}")
    
    def track_packetstream_request(self, response_size_bytes=0):
        """Track PacketStream bandwidth usage (REAL COSTS)"""
        # Convert bytes to MB/GB
        size_mb = response_size_bytes / (1024 * 1024)
        size_gb = size_mb / 1024
        
        # Update totals
        self.packetstream_data_used_mb += size_mb
        self.packetstream_data_used_gb += size_gb
        self.packetstream_requests_made += 1
        
        # Calculate cost
        self.packetstream_cost = self.packetstream_data_used_gb * self.packetstream_cost_per_gb
        
        # Save after each request
        self.save_stats()
    
    def track_google_api_request(self):
        """Track Google Maps API usage (FREE, just quota)"""
        self.google_api_requests_made += 1
        
        # Check if approaching free tier limit
        if self.google_api_requests_made >= self.google_api_free_tier_limit * 0.9:
            print(f"⚠️  Google Maps API: {self.google_api_requests_made}/{self.google_api_free_tier_limit} requests used")
        
        # Save after each request
        self.save_stats()
    
    def track_query(self, query, state, county=None, businesses_found=0):
        """Track query statistics (no costs, just usage)"""
        if query not in self.query_stats:
            self.query_stats[query] = {
                "total_businesses": 0,
                "states": set(),  # Keep as set for operations
                "counties": set(),  # Keep as set for operations
                "last_used": None
            }
        
        # Update query stats
        self.query_stats[query]["total_businesses"] += businesses_found
        self.query_stats[query]["states"].add(state)
        if county:
            self.query_stats[query]["counties"].add(county)
        self.query_stats[query]["last_used"] = datetime.now().isoformat()
        
        # Update state stats
        if state not in self.state_stats:
            self.state_stats[state] = {
                "total_businesses": 0,
                "counties": set(),  # Keep as set for operations
                "queries": set(),   # Keep as set for operations
                "last_used": None
            }
        
        self.state_stats[state]["total_businesses"] += businesses_found
        if county:
            self.state_stats[state]["counties"].add(county)
        self.state_stats[state]["queries"].add(query)
        self.state_stats[state]["last_used"] = datetime.now().isoformat()
        
        # Save stats
        self.save_stats()
    
    def get_final_report(self):
        """Generate comprehensive usage report"""
        total_time = time.time() - self.start_time
        
        # Refresh status
        self.check_google_api_status()
        self.check_packetstream_status()
        
        print("\n" + "="*80)
        print(" CORRECTED USAGE REPORT")
        print("="*80)
        
        print(f"⏰ Session Duration: {total_time:.1f} seconds")
        
        # PacketStream Costs (REAL COSTS)
        print(f"\n PACKETSTREAM PROXY (REAL COSTS):")
        print(f"   Data Used: {self.packetstream_data_used_mb:.2f} MB")
        print(f"   Cost: ${self.packetstream_cost:.6f}")
        print(f"   Requests Made: {self.packetstream_requests_made}")
        print(f"   Requests Failed: {self.packetstream_requests_failed}")
        print(f"   Cost per GB: ${self.packetstream_cost_per_gb}")
        
        # Google Maps API (FREE)
        print(f"\n🗺️  GOOGLE MAPS API (FREE):")
        print(f"   Requests Made: {self.google_api_requests_made}")
        print(f"   Free Tier Limit: {self.google_api_free_tier_limit}")
        print(f"   Remaining: {max(0, self.google_api_free_tier_limit - self.google_api_requests_made)}")
        print(f"   Status: {self.google_api_quota_status}")
        
        # Query Statistics
        print(f"\n📊 QUERY STATISTICS:")
        for query, stats in self.query_stats.items():
            print(f"   {query}: {stats['total_businesses']} businesses")
            print(f"     States: {len(stats['states'])}")
            print(f"     Counties: {len(stats['counties'])}")
        
        # State Statistics
        print(f"\n🌍 STATE STATISTICS:")
        for state, stats in self.state_stats.items():
            print(f"   {state}: {stats['total_businesses']} businesses")
            print(f"     Counties: {len(stats['counties'])}")
            print(f"     Queries: {len(stats['queries'])}")
        
        print("="*80)
        
        # Save final stats
        self.save_stats()
        
        return {
            "packetstream_cost": self.packetstream_cost,
            "packetstream_data_gb": self.packetstream_data_used_gb,
            "google_api_requests": self.google_api_requests_made,
            "total_businesses": sum(stats['total_businesses'] for stats in self.query_stats.values())
        }
