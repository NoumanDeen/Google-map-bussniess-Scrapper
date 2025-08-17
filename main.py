from Google import Scraper
import requests
import time
import json
import pandas as pd
import os
from counties_data import counties_data
from credit_tracker import CreditTracker
from datetime import datetime
from Utils import proxy_user, proxy_pass  # Import proxy credentials

def print_welcome_banner():
    """Print a stylish welcome banner"""
    print("\n" + "="*100)
    print("🎯" + " "*30 + "GOOGLE MAPS BUSINESS SCRAPER" + " "*36 + "🎯")
    print("="*100)
    print("🌟" + " "*30 + "PROFESSIONAL GMB PROFILE EXTRACTOR" + " "*30 + "🌟")
    print("="*100)
    print("🚀 Powered by Hastylead")
    print("="*100 + "\n")

def get_counties_from_data(state_code):
    """Get counties from counties_data.py file"""
    try:
        print(f"🌐 Getting counties from counties_data.py for {state_code}...")
        
        if state_code in counties_data:
            counties = counties_data[state_code]
            print(f"✅ Found {len(counties)} counties for {state_code}")
            return counties
        else:
            print(f"❌ No counties available for {state_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error getting counties: {e}")
        return []

def get_state_input():
    """Get state selection from user"""
    states = {
        "1": "AL", "2": "AK", "3": "AZ", "4": "AR", "5": "CA",
        "6": "CO", "7": "CT", "8": "DE", "9": "FL", "10": "GA",
        "11": "HI", "12": "ID", "13": "IL", "14": "IN", "15": "IA",
        "16": "KS", "17": "KY", "18": "LA", "19": "ME", "20": "MD",
        "21": "MA", "22": "MI", "23": "MN", "24": "MS", "25": "MO",
        "26": "MT", "27": "NE", "28": "NV", "29": "NH", "30": "NJ",
        "31": "NM", "32": "NY", "33": "NC", "34": "ND", "35": "OH",
        "36": "OK", "37": "OR", "38": "PA", "39": "RI", "40": "SC",
        "41": "SD", "42": "TN", "43": "TX", "44": "UT", "45": "VT",
        "46": "VA", "47": "WA", "48": "WV", "49": "WI", "50": "WY"
    }
    
    # Full state names mapping
    state_names = {
        "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
        "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
        "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
        "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
        "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
        "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
        "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
        "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
        "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
        "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
    }
    
    print("\n" + "" + "="*78 + "🌍")
    print("🏛️  SELECT YOUR TARGET STATE (All 50 US States Available)")
    print("" + "="*78 + "🌍")
    
    # Display states in columns with full names
    for i in range(0, 50, 5):
        row_states = []
        for j in range(5):
            if i + j < 50:
                num = str(i + j + 1)
                state_code = states[num]
                state_name = state_names[state_code]
                row_states.append(f"{num:>2}. {state_name}")
        print("  ".join(row_states))
    
    print("" + "="*78 + "🌍")
    
    while True:
        try:
            choice = input("\n ENTER STATE SELECTION:\n   Number (1-50) • Full Name • Abbreviation\n   Example: 1, Alabama, or AL\n\n   Your choice: ").strip()
            
            # Handle numeric input
            if choice in states:
                selected_state = states[choice]
                print(f"\n✅ SELECTED: {state_names[selected_state]} ({selected_state})")
                return selected_state
            
            # Handle full state name input
            choice_upper = choice.upper()
            for state_code, state_name in state_names.items():
                if choice_upper == state_name.upper():
                    print(f"\n✅ SELECTED: {state_name} ({state_code})")
                    return state_code
            
            # Handle state abbreviation input
            if choice.upper() in states.values():
                selected_state = choice.upper()
                print(f"\n✅ SELECTED: {state_names[selected_state]} ({selected_state})")
                return selected_state
            
            print(f"\n❌ INVALID SELECTION: {choice}")
            print("   Please enter a number 1-50, full state name, or state abbreviation.")
                
        except (ValueError, IndexError):
            print("❌ Invalid input. Please try again.")

def display_counties(counties, state):
    """Display counties with coordinates"""
    print(f"\n️  COUNTIES IN {state}:")
    print("-" * 80)
    print(f"{'#':<3} {'County':<25} {'Coordinates':<25}")
    print("-" * 80)
    
    # Show all counties
    for i, county in enumerate(counties, 1):
        lat = county.get('lat', 0)
        lon = county.get('lon', 0)
        
        if lat == 0 and lon == 0:
            coords_display = 'N/A'
        else:
            coords_display = f"({lat:.4f}, {lon:.4f})"
        
        print(f"{i:<3} {county['name']:<25} {coords_display}")
    
    print(f"Total: {len(counties)} counties")

def get_county_selection(counties):
    """Ask user which counties they want"""
    print(f"\n🏘️  COUNTY SELECTION:")
    print(f"Total counties available: {len(counties)}")
    print("Which counties do you want to search?")
    print("1. All counties")
    print("2. Select specific counties")
    
    while True:
        try:
            choice = input("\n🏘️  Enter your choice (1 or 2): ").strip()
            
            if choice == "1":
                selected_counties = counties
                print(f"✅ Selected: All {len(counties)} counties")
                return selected_counties
            
            elif choice == "2":
                print("\nAvailable counties:")
                for i, county in enumerate(counties, 1):
                    print(f"{i}. {county['name']}")
                
                print("\nEnter county numbers separated by commas (e.g., 1,2):")
                county_input = input().strip()
                selected_indices = [int(x.strip()) - 1 for x in county_input.split(',')]
                
                selected_counties = [counties[i] for i in selected_indices if 0 <= i < len(counties)]
                print(f"✅ Selected: {len(selected_counties)} counties")
                return selected_counties
            
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")
                
        except ValueError:
            print("❌ Invalid input. Please try again.")

def main():
    # Print stylish welcome banner
    print_welcome_banner()
    
    # Initialize credit tracker with PacketStream credentials
    api_key = "AIzaSyDD8LALkNo36hN295bcI3Wim-LUvlm5G3s"  # From Utils.py
    credit_tracker = CreditTracker(
        api_key=api_key,
        proxy_user=proxy_user,  # PacketStream username
        proxy_pass=proxy_pass   # PacketStream password
    )
    
    # Step 1: Get search query first
    print("🔍 ENTER YOUR SEARCH QUERY:")
    print("   Examples: 'mobile home parks', 'property management', 'real estate'")
    print("-" * 60)
    base_search = input("Query: ").strip()
    
    # Step 2: Ask which state
    selected_state = get_state_input()
    print(f"\n✅ Selected state: {selected_state}")
    
    # Step 3: Fetch counties from counties_data.py
    counties = get_counties_from_data(selected_state)
    if not counties:
        print(f"❌ No counties found for {selected_state}")
        return
    
    # Step 4: Show counties and their coordinates
    display_counties(counties, selected_state)
    
    # Step 5: Ask which counties user wants
    selected_counties = get_county_selection(counties)
    print(f"\n✅ Selected counties: {len(selected_counties)} counties")
    
    # Step 6: Ask for output file name
    print("\n" + "="*50)
    print(" OUTPUT FILE CONFIGURATION")
    print("="*50)
    
    print("Enter output file name (will append state):")
    filenm_base = input().strip()
    
    # Confirm before starting
    print(f"\n📋 SUMMARY:")
    print(f"Search Query: {base_search}")
    print(f"State: {selected_state}")
    print(f"Counties: {len(selected_counties)} counties selected")
    print(f"Output File: {filenm_base} - {selected_state}.xlsx")
    
    confirm = input("\n Start scraping? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ Scraping cancelled.")
        return
    
    # Start scraping
    start_time = time.time()
    print(f"\n⏰ Start time: {time.strftime('%H:%M:%S')}")
    
    all_state_data = [] # Collect data from all counties
    for i, county in enumerate(selected_counties, 1):
        county_full = f"{county['name']}, {selected_state}"
        search_term = f"{base_search} in {county_full}"
        
        print(f"\n🚀 County {i}/{len(selected_counties)}: {county_full}")
        print(f" Coords: {county['lat']:.4f}, {county['lon']:.4f}")
        print(f"🔍 Search term: {search_term}")
        
        try:
            # Create scraper for each county
            out_name = f"{filenm_base} - {county['name']}_{selected_state}"
            s = Scraper(search_term, "", county['lat'], county['lon'])
            county_data = s.start_and_return_data()

            # Track credits used for this query/county
            # Each business address lookup uses 1 geocoding API call
            businesses_found = len(county_data)
            
            # Track credits for EACH business found (not just once per county)
            for _ in range(businesses_found):
                credit_tracker.track_query(
                    query=base_search,
                    state=selected_state,
                    county=county['name'],
                    results_count=1  # Each business = 1 API call
                )
            
            print(f"✅ Completed {county['name']} - {businesses_found} businesses found")
            print(f"💰 Credits used for this county: ${businesses_found * 0.005:.3f}")

            # Add county information to each business record
            for business in county_data:
                business['County'] = county['name']
                business['State'] = selected_state
                all_state_data.append(business)
            
        except Exception as e:
            print(f"❌ Error scraping {county['name']}: {e}")
            continue
    
    total_time = time.time() - start_time
    print(f"\n✅ All counties completed in {total_time:.1f} seconds")
    
    # Save all collected data to a single state file
    if all_state_data:
        try:
            df = pd.DataFrame(all_state_data)
            df.to_excel(f"{filenm_base} - {selected_state}.xlsx", index=False)
            print(f"\n✅ All data saved to {filenm_base} - {selected_state}.xlsx")
        except Exception as e:
            print(f"❌ Error saving state-level file: {e}")
    else:
        print("❌ No data collected to save.")
    
    # Generate final credit report
    print("\n" + "="*60)
    print("💰 GENERATING CREDIT USAGE REPORT")
    print("="*60)
    
    credit_tracker.get_final_report()

if __name__ == '__main__':
    main()
