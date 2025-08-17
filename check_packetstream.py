#!/usr/bin/env python3
"""
PacketStream Status Checker
Check if your PacketStream proxy is working
"""

import requests
from Utils import proxy_user, proxy_pass

def check_packetstream_status():
    """Check PacketStream proxy status"""
    print("🌐 PACKETSTREAM STATUS CHECKER")
    print("=" * 50)
    
    if not proxy_user or not proxy_pass:
        print("❌ PacketStream credentials not found in Utils.py")
        return
    
    try:
        print(f"🔍 Checking status for user: {proxy_user}")
        
        # Test proxy connection
        test_url = "http://httpbin.org/ip"
        proxy_url = f"http://{proxy_user}:{proxy_pass}@proxy.packetstream.io:31112"
        
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
        
        print("🌐 Testing proxy connection...")
        response = requests.get(test_url, proxies=proxies, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS! PacketStream proxy is working")
            print(f" Your IP: {data.get('origin', 'Unknown')}")
            print("💡 Your proxy has credits available")
            print(" Note: Exact credit amount not available via API")
        else:
            print(f"❌ Proxy test failed: {response.status_code}")
            print("💡 Check your PacketStream account or credentials")
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - proxy may be slow")
    except requests.exceptions.ConnectionError:
        print(" Connection error - check your internet connection")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_packetstream_status()
