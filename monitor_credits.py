#!/usr/bin/env python3
"""
Credit Monitoring Script for GMB Scraper
Use this to check your current credit usage and remaining credits
"""

import json
import os
from credit_tracker import CreditTracker

def main():
    print("💰 CREDIT MONITORING DASHBOARD")
    print("=" * 50)
    
    # Check if credit stats exist
    if not os.path.exists("credit_stats.json"):
        print("❌ No credit statistics found.")
        print("   Run the scraper first to generate credit tracking data.")
        return
    
    # Load and display current stats
    try:
        with open("credit_stats.json", "r") as f:
            stats = json.load(f)
        
        print(f"📊 Last Updated: {stats.get('last_updated', 'Unknown')}")
        print(f"�� Total Credits Used: ${stats.get('total_credits_used', 0):.3f}")
        print(f"📈 Total Requests: {sum(q['total_requests'] for q in stats.get('query_stats', {}).values())}")
        
        # Show breakdown by query
        print(f"\n🔍 BY SEARCH QUERY:")
        for query, data in stats.get('query_stats', {}).items():
            print(f"   {query}: {data['total_requests']} requests, ${data['total_credits']:.3f}")
        
        # Show breakdown by state
        print(f"\n🌍 BY STATE:")
        for state, data in stats.get('state_stats', {}).items():
            print(f"   {state}: {data['total_requests']} requests, ${data['total_credits']:.3f}")
            
            # Show county breakdown
            for county, county_data in data.get('counties', {}).items():
                print(f"     {county}: {county_data['total_requests']} requests, ${county_data['total_credits']:.3f}")
        
        # Estimate remaining credits
        total_used = stats.get('total_credits_used', 0)
        estimated_remaining = max(0, 200 - total_used * 1000)  # Rough estimate
        print(f"\n💡 Estimated remaining requests: ~{estimated_remaining:.0f}")
        
        # Cost analysis
        print(f"\n💵 COST ANALYSIS:")
        print(f"   Current cost: ${total_used:.3f}")
        print(f"   Cost per 1000 requests: $5.00")
        print(f"   Cost per request: $0.005")
        
    except Exception as e:
        print(f"❌ Error reading credit stats: {e}")

if __name__ == "__main__":
    main()
