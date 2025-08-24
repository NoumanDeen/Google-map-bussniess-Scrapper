#!/usr/bin/env python3
"""
Google Maps API Credit Checker
Check your available credits, usage, and billing information
"""

import requests
import json
import time
from datetime import datetime
import os

class GoogleMapsAPIChecker:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api"
        
    def check_api_status(self):
        """Check if API key is valid and get basic status"""
        print("🔍 CHECKING GOOGLE MAPS API STATUS")
        print("=" * 50)
        
        try:
            # Test with a simple geocoding request
            test_url = f"{self.base_url}/geocode/json?address=test&key={self.api_key}"
            response = requests.get(test_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "UNKNOWN")
                
                print(f"✅ API Key Status: {status}")
                
                if status == "OK":
                    print("✅ API key is valid and working")
                    return True
                elif status == "OVER_QUERY_LIMIT":
                    print("⚠️  API quota exceeded - check billing")
                    return False
                elif status == "REQUEST_DENIED":
                    print("❌ API key invalid or restricted")
                    return False
                elif status == "ZERO_RESULTS":
                    print("✅ API key valid (no results for test address)")
                    return True
                else:
                    print(f"⚠️  Unknown status: {status}")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error checking API: {e}")
            return False
    
    def check_quota_usage(self):
        """Check quota usage (approximate)"""
        print("\n📊 CHECKING QUOTA USAGE")
        print("=" * 50)
        
        try:
            # Make a test request to see if we're near limits
            test_url = f"{self.base_url}/geocode/json?address=test&key={self.api_key}"
            response = requests.get(test_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response headers for quota info
                headers = response.headers
                
                print("📈 Response Headers Analysis:")
                for header, value in headers.items():
                    if 'quota' in header.lower() or 'limit' in header.lower():
                        print(f"   {header}: {value}")
                
                # Check if we're getting rate limited
                if data.get("status") == "OVER_QUERY_LIMIT":
                    print("⚠️  QUOTA EXCEEDED - You've hit your daily/monthly limit")
                    print("💡 Check your Google Cloud Console billing page")
                else:
                    print("✅ Quota appears to be available")
                    
        except Exception as e:
            print(f"❌ Error checking quota: {e}")
    
    def estimate_remaining_requests(self, cost_per_request=0.005):
        """Estimate remaining requests based on typical limits"""
        print("\n💡 ESTIMATED REMAINING REQUESTS")
        print("=" * 50)
        
        # Common Google Maps API limits
        limits = {
            "Free Tier": 1000,
            "Paid Tier (Basic)": 100000,
            "Paid Tier (Premium)": 1000000
        }
        
        print("📋 Typical Google Maps API Limits:")
        for tier, limit in limits.items():
            print(f"   {tier}: {limit:,} requests per month")
        
        print(f"\n💰 Cost per request: ${cost_per_request}")
        print(f"💵 Cost per 1,000 requests: ${cost_per_request * 1000}")
        
        # If you have billing info, you could estimate based on your plan
        print("\n💡 To get exact remaining requests:")
        print("   1. Go to https://console.cloud.google.com/")
        print("   2. Navigate to APIs & Services > Dashboard")
        print("   3. Click on Geocoding API")
        print("   4. Check the Quotas tab")
    
    def test_geocoding_request(self):
        """Test a real geocoding request"""
        print("\n🧪 TESTING GEOCODING REQUEST")
        print("=" * 50)
        
        try:
            test_address = "1600 Amphitheatre Parkway, Mountain View, CA"
            test_url = f"{self.base_url}/geocode/json?address={test_address}&key={self.api_key}"
            
            print(f"�� Testing address: {test_address}")
            
            response = requests.get(test_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "UNKNOWN")
                
                print(f"✅ Request Status: {status}")
                
                if status == "OK":
                    results = data.get("results", [])
                    if results:
                        result = results[0]
                        formatted_address = result.get("formatted_address", "N/A")
                        print(f"�� Formatted Address: {formatted_address}")
                        
                        # Show address components
                        components = result.get("address_components", [])
                        print("�� Address Components:")
                        for comp in components:
                            types = comp.get("types", [])
                            long_name = comp.get("long_name", "")
                            short_name = comp.get("short_name", "")
                            print(f"   {types}: {long_name} ({short_name})")
                        
                        print("✅ Geocoding API is working correctly!")
                        return True
                    else:
                        print("⚠️  No results returned")
                        return False
                else:
                    print(f"❌ Request failed with status: {status}")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing geocoding: {e}")
            return False
    
    def get_billing_info(self):
        """Provide information about checking billing"""
        print("\n💳 BILLING INFORMATION")
        print("=" * 50)
        
        print("🔗 Google Cloud Console Links:")
        print("   📊 Dashboard: https://console.cloud.google.com/")
        print("   💰 Billing: https://console.cloud.google.com/billing")
        print("   📈 APIs: https://console.cloud.google.com/apis/dashboard")
        print("   �� Credentials: https://console.cloud.google.com/apis/credentials")
        
        print("\n📋 How to check your exact usage:")
        print("   1. Login to Google Cloud Console")
        print("   2. Go to Billing > Reports")
        print("   3. Filter by 'Maps Platform'")
        print("   4. Check daily/monthly usage")
        
        print("\n💰 Current Pricing (Geocoding API):")
        print("   • $5.00 per 1,000 requests")
        print("   • $0.005 per individual request")
        print("   • Free tier: 1,000 requests/month")
    
    def run_full_check(self):
        """Run complete API check"""
        print("�� GOOGLE MAPS API CREDIT CHECKER")
        print("=" * 60)
        print(f"⏰ Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"�� API Key: {self.api_key[:10]}...{self.api_key[-10:]}")
        print("=" * 60)
        
        # Run all checks
        self.check_api_status()
        self.check_quota_usage()
        self.estimate_remaining_requests()
        self.test_geocoding_request()
        self.get_billing_info()
        
        print("\n" + "=" * 60)
        print("✅ CHECK COMPLETE")
        print("=" * 60)

def main():
    # Get API key from environment or use the one from your code
    api_key = os.getenv('GOOGLE_MAPS_API_KEY', 'AIzaSyDD8LALkNo36hN295bcI3Wim-LUvlm5G3s')
    
    if not api_key:
        print("❌ No API key found!")
        print("Set GOOGLE_MAPS_API_KEY environment variable or update the script")
        return
    
    # Create checker and run full check
    checker = GoogleMapsAPIChecker(api_key)
    checker.run_full_check()

if __name__ == "__main__":
    main()
