import json
import os
import time
from datetime import datetime
import requests

class CreditTracker:
    def __init__(self, api_key=None, proxy_user=None, proxy_pass=None):
        self.api_key = api_key
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        self.credits_used = 0
        self.credits_remaining = None
        self.query_stats = {}
        self.state_stats = {}
        self.start_time = time.time()
        
        # Proxy usage tracking
        self.proxy_requests_made = 0
        self.proxy_requests_failed = 0
        self.last_proxy_check = None
        
        # Load existing stats if available
        self.load_stats()
        
        # Check initial credits if API key provided
        if self.api_key:
            self.check_remaining_credits()
        
        # Initialize proxy status
        self.check_proxy_status()
    
    def load_stats(self):
        """Load existing credit statistics from file"""
        try:
            if os.path.exists("credit_stats.json"):
                with open("credit_stats.json", "r") as f:
                    data = json.load(f)
                    # Round to 3 decimal places for realistic display
                    self.credits_used = round(data.get("total_credits_used", 0), 3)
                    self.query_stats = data.get("query_stats", {})
                    
                    # Convert lists back to sets when loading
                    loaded_state_stats = data.get("state_stats", {})
                    for state, stats in loaded_state_stats.items():
                        if "queries" in stats and isinstance(stats["queries"], list):
                            stats["queries"] = set(stats["queries"])  # Convert list back to set
                    self.state_stats = loaded_state_stats
                    
                    print(f"📊 Loaded existing stats: ${self.credits_used:.3f} credits used")
        except Exception as e:
            print(f"⚠️  Could not load existing stats: {e}")
    
    def save_stats(self):
        """Save current credit statistics to file"""
        try:
            # Convert sets to lists for JSON serialization
            serializable_state_stats = {}
            for state, stats in self.state_stats.items():
                serializable_state_stats[state] = {
                    "total_requests": stats["total_requests"],
                    "total_credits": round(stats["total_credits"], 3),  # Round to 3 decimals
                    "counties": stats["counties"],
                    "queries": list(stats["queries"]),  # Convert set to list
                    "last_used": stats["last_used"]
                }
            
            data = {
                "last_updated": datetime.now().isoformat(),
                "total_credits_used": round(self.credits_used, 3),  # Round to 3 decimals
                "query_stats": self.query_stats,
                "state_stats": serializable_state_stats,  # Use serializable version
                "session_duration": time.time() - self.start_time
            }
            
            with open("credit_stats.json", "w") as f:
                json.dump(data, f, indent=2)
            
            print(f" Credit stats saved to credit_stats.json")
        except Exception as e:
            print(f"❌ Error saving credit stats: {e}")
    
    def check_remaining_credits(self):
        """Check remaining Google Maps API credits"""
        if not self.api_key:
            print("⚠️  No API key provided to check remaining credits")
            return
        
        try:
            # Use a simple geocoding request to check quota
            test_url = f"https://maps.googleapis.com/maps/api/geocode/json?address=test&key={self.api_key}"
            response = requests.get(test_url)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "OVER_QUERY_LIMIT":
                    print("⚠️  API quota exceeded!")
                    self.credits_remaining = 0
                elif data.get("status") == "REQUEST_DENIED":
                    print("❌ API key invalid or restricted")
                    self.credits_remaining = 0
                else:
                    # Note: Google doesn't provide exact credit count in response
                    # This is an estimate based on typical usage
                    print("✅ API key valid - credits available")
                    self.credits_remaining = "Unknown (check Google Cloud Console)"
            else:
                print(f"⚠️  Could not check API status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error checking API credits: {e}")
    
    def check_proxy_status(self):
        """Check if PacketStream proxy is working and estimate credits"""
        try:
            print("🔍 Checking PacketStream proxy status...")
            
            # Test proxy connection
            test_url = "http://httpbin.org/ip"
            proxy_url = f"http://{self.proxy_user}:{self.proxy_pass}@proxy.packetstream.io:31112"
            
            proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
            
            response = requests.get(test_url, proxies=proxies, timeout=15)
            
            if response.status_code == 200:
                print("✅ PacketStream proxy is active and working")
                self.credits_remaining = "Proxy Active - Credits Available"
                self.last_proxy_check = datetime.now().isoformat()
            else:
                print(f"⚠️  Proxy test failed: {response.status_code}")
                self.credits_remaining = "Proxy Inactive - Check Account"
                
        except Exception as e:
            print(f"❌ Proxy test error: {e}")
            self.credits_remaining = "Proxy Error - Check Connection"
    
    def track_proxy_request(self, success=True):
        """Track proxy usage to estimate remaining credits"""
        if success:
            self.proxy_requests_made += 1
        else:
            self.proxy_requests_failed += 1
        
        # Estimate remaining credits based on typical PacketStream limits
        # This is an approximation since we can't get exact API data
        estimated_total_requests = 10000  # Typical PacketStream monthly limit
        estimated_remaining = max(0, estimated_total_requests - self.proxy_requests_made)
        
        if estimated_remaining < 100:
            self.credits_remaining = f"Low Credits (~{estimated_remaining} requests left)"
        elif estimated_remaining < 1000:
            self.credits_remaining = f"Medium Credits (~{estimated_remaining} requests left)"
        else:
            self.credits_remaining = f"Good Credits (~{estimated_remaining} requests left)"
    
    def refresh_proxy_status(self):
        """Refresh proxy status and estimate remaining credits"""
        self.check_proxy_status()
        self.track_proxy_request(success=True)
    
    def track_query(self, query, state, county=None, results_count=0):
        """Track credits used for a specific query"""
        # Google Maps Geocoding API costs:
        # - $5 per 1000 requests
        # - Each business address lookup = 1 request
        
        if query not in self.query_stats:
            self.query_stats[query] = {
                "total_requests": 0,
                "total_credits": 0,
                "states": {},
                "counties": {},
                "last_used": None
            }
        
        # Update query stats
        self.query_stats[query]["total_requests"] += results_count  # Use results_count instead of 1
        self.query_stats[query]["total_credits"] = round(self.query_stats[query]["total_credits"] + (results_count * 0.005), 3)  # Round to 3 decimals
        self.query_stats[query]["last_used"] = datetime.now().isoformat()
        
        # Update state stats
        if state not in self.state_stats:
            self.state_stats[state] = {
                "total_requests": 0,
                "total_credits": 0,
                "counties": {},
                "queries": set(),
                "last_used": None
            }
        
        self.state_stats[state]["total_requests"] += results_count  # Use results_count
        self.state_stats[state]["total_credits"] = round(self.state_stats[state]["total_credits"] + (results_count * 0.005), 3)  # Round to 3 decimals
        self.state_stats[state]["queries"].add(query)
        self.state_stats[state]["last_used"] = datetime.now().isoformat()
        
        # Update county stats if provided
        if county:
            if county not in self.state_stats[state]["counties"]:
                self.state_stats[state]["counties"][county] = {
                    "total_requests": 0,
                    "total_credits": 0,
                    "last_used": None
                }
            
            self.state_stats[state]["counties"][county]["total_requests"] += results_count  # Use results_count
            self.state_stats[state]["counties"][county]["total_credits"] = round(self.state_stats[state]["counties"][county]["total_credits"] + (results_count * 0.005), 3)  # Round to 3 decimals
            self.state_stats[state]["counties"][county]["last_used"] = datetime.now().isoformat()
        
        # Update total credits used
        self.credits_used = round(self.credits_used + (results_count * 0.005), 3)  # Round to 3 decimals
        
        # Save stats after each update
        self.save_stats()
    
    def get_query_summary(self, query=None):
        """Get summary of credits used for queries"""
        if query:
            if query in self.query_stats:
                stats = self.query_stats[query]
                print(f"\n📊 QUERY SUMMARY: {query}")
                print(f"   Total Requests: {stats['total_requests']}")
                print(f"   Total Credits: ${stats['total_credits']:.3f}")
                print(f"   States Covered: {list(stats['states'].keys())}")
                print(f"   Last Used: {stats['last_used']}")
            else:
                print(f"❌ No data found for query: {query}")
        else:
            print(f"\n📊 ALL QUERIES SUMMARY:")
            for q, stats in self.query_stats.items():
                print(f"   {q}: {stats['total_requests']} requests, ${stats['total_credits']:.3f}")
    
    def get_state_summary(self, state=None):
        """Get summary of credits used per state"""
        if state:
            if state in self.state_stats:
                stats = self.state_stats[state]
                print(f"\n🌍 STATE SUMMARY: {state}")
                print(f"   Total Requests: {stats['total_requests']}")
                print(f"   Total Credits: ${stats['total_credits']:.3f}")
                print(f"   Counties: {list(stats['counties'].keys())}")
                print(f"   Queries: {list(stats['queries'])}")
                print(f"   Last Used: {stats['last_used']}")
            else:
                print(f"❌ No data found for state: {state}")
        else:
            print(f"\n�� ALL STATES SUMMARY:")
            for s, stats in self.state_stats.items():
                print(f"   {s}: {stats['total_requests']} requests, ${stats['total_credits']:.3f}")
    
    def get_final_report(self):
        """Generate final credit usage report"""
        total_time = time.time() - self.start_time
        
        # Refresh proxy status before final report
        self.refresh_proxy_status()
        
        print("\n" + "="*80)
        print(" FINAL CREDIT USAGE REPORT")
        print("="*80)
        
        print(f"⏰ Session Duration: {total_time:.1f} seconds")
        print(f" Total Credits Used: ${self.credits_used:.3f}")
        print(f" API Key Status: {'Valid' if self.credits_remaining != 0 else 'Invalid/Exceeded'}")
        
        # Show PacketStream proxy status
        if self.proxy_user and self.proxy_pass:
            print(f"🌐 PacketStream Status: {self.credits_remaining}")
            print(f"📊 Proxy Requests Made: {self.proxy_requests_made}")
            print(f"❌ Proxy Requests Failed: {self.proxy_requests_failed}")
            print(f"🔄 Last Proxy Check: {self.last_proxy_check}")
        
        print(f"\n📊 BY QUERY:")
        for query, stats in self.query_stats.items():
            print(f"   {query}: {stats['total_requests']} requests, ${stats['total_credits']:.3f}")
        
        print(f"\n🌍 BY STATE:")
        for state, stats in self.state_stats.items():
            print(f"   {state}: {stats['total_requests']} requests, ${stats['total_credits']:.3f}")
            
            # Show county breakdown
            for county, county_stats in stats['counties'].items():
                print(f"     {county}: {county_stats['total_requests']} requests, ${county_stats['total_credits']:.3f}")
        
        # Show proxy-based credit estimation
        if self.proxy_user and self.proxy_pass:
            print(f"\n💡 PacketStream Credits: {self.credits_remaining}")
        else:
            # Fallback to estimate if no proxy
            estimated_remaining = max(0, 200 - self.credits_used * 1000)
            print(f"\n💡 Estimated remaining requests: ~{estimated_remaining:.0f}")
        
        print("="*80)
        
        # Save final stats
        self.save_stats()
        
        return {
            "total_credits": self.credits_used,
            "total_requests": sum(stats['total_requests'] for stats in self.query_stats.values()),
            "states_covered": list(self.state_stats.keys()),
            "queries_used": list(self.query_stats.keys()),
            "packetstream_credits": self.credits_remaining,
            "proxy_requests": self.proxy_requests_made,
            "proxy_failures": self.proxy_requests_failed
        }
