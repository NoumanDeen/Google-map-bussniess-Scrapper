import sys
import os

# Force UTF-8 encoding for Windows - remove problematic chcp command
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        # Fallback for older Python versions
        pass

from Google import Scraper
import requests
import time
import json
import random
import pandas as pd
from counties_data import counties_data
from credit_tracker import CorrectedCreditTracker
from datetime import datetime
from Utils import proxy_user, proxy_pass, AUTOSAVE_EVERY_COUNTIES, SHUFFLE_COUNTIES, RESUME

def print_welcome_banner():
    """Print a stylish welcome banner"""
    print("\n" + "="*100)
    print("*" + " "*30 + "GOOGLE MAPS BUSINESS SCRAPER" + " "*36 + "*")
    print("="*100)
    print(">" + " "*30 + "PROFESSIONAL GMB PROFILE EXTRACTOR" + " "*30 + "<")
    print("="*100)
    print("Powered by Hastylead")
    print("="*100 + "\n")

def get_counties_from_data(state_code):
    """Get counties from counties_data.py file"""
    try:
        print(f"[INFO] Getting counties from counties_data.py for {state_code}...")
        
        if state_code in counties_data:
            counties = counties_data[state_code]
            print(f"[SUCCESS] Found {len(counties)} counties for {state_code}")
            return counties
        else:
            print(f"[ERROR] No counties available for {state_code}")
            return []
            
    except Exception as e:
        print(f"[ERROR] Error getting counties: {e}")
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
                print(f"\n[SUCCESS] SELECTED: {state_names[selected_state]} ({selected_state})")
                return selected_state
            
            # Handle full state name input
            choice_upper = choice.upper()
            for state_code, state_name in state_names.items():
                if choice_upper == state_name.upper():
                    print(f"\n[SUCCESS] SELECTED: {state_name} ({state_code})")
                    return state_code
            
            # Handle state abbreviation input
            if choice.upper() in states.values():
                selected_state = choice.upper()
                print(f"\n[SUCCESS] SELECTED: {state_names[selected_state]} ({selected_state})")
                return selected_state
            
            print(f"\n[ERROR] INVALID SELECTION: {choice}")
            print("   Please enter a number 1-50, full state name, or state abbreviation.")
                
        except (ValueError, IndexError):
            print("[ERROR] Invalid input. Please try again.")

def display_counties(counties, state):
    """Display counties with coordinates"""
    print(f"\n[INFO] COUNTIES IN {state}:")
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
    print(f"\n[INFO] COUNTY SELECTION:")
    print(f"Total counties available: {len(counties)}")
    print("Which counties do you want to search?")
    print("1. All counties")
    print("2. Select specific counties")
    
    while True:
        try:
            choice = input("\n[INPUT] Enter your choice (1 or 2): ").strip()
            
            if choice == "1":
                selected_counties = counties
                print(f"[SUCCESS] Selected: All {len(counties)} counties")
                return selected_counties
            
            elif choice == "2":
                print("\nAvailable counties:")
                for i, county in enumerate(counties, 1):
                    print(f"{i}. {county['name']}")
                
                print("\nEnter county numbers separated by commas (e.g., 1,2):")
                county_input = input().strip()
                selected_indices = [int(x.strip()) - 1 for x in county_input.split(',')]
                
                selected_counties = [counties[i] for i in selected_indices if 0 <= i < len(counties)]
                print(f"[SUCCESS] Selected: {len(selected_counties)} counties")
                return selected_counties
            
            else:
                print("[ERROR] Invalid choice. Please enter 1 or 2.")
                
        except ValueError:
            print("[ERROR] Invalid input. Please try again.")

def check_packetstream_before_scraping():
    """Check PacketStream proxy status before starting scraping"""
    print("\n🌐 CHECKING PACKETSTREAM PROXY STATUS")
    print("=" * 50)
    
    if not proxy_user or not proxy_pass:
        print("❌ PacketStream credentials not found!")
        print("   Please check your Utils.py file")
        return False
    
    try:
        print(f"🔍 Testing proxy for user: {proxy_user}")
        
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
            print(f"   Your proxy IP: {data.get('origin', 'Unknown')}")
            print("💡 Proxy has credits available - ready to scrape!")
            return True
        else:
            print(f"❌ Proxy test failed: {response.status_code}")
            print("💡 Check your PacketStream account or credentials")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - proxy may be slow")
        print(" Try again or check your connection")
        return False
    except requests.exceptions.ConnectionError:
        print(" Connection error - check your internet connection")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    # Print stylish welcome banner
    print_welcome_banner()
    
    # 🔧 ADD THIS CHECK HERE
    print("\n🔍 PRE-FLIGHT CHECKS")
    print("=" * 50)
    
    # Check PacketStream proxy
    proxy_ok = check_packetstream_before_scraping()
    if not proxy_ok:
        print("\n❌ PACKETSTREAM CHECK FAILED!")
        print("   Please fix your proxy settings before continuing.")
        print("   Check your Utils.py file and PacketStream account.")
        input("\nPress Enter to exit...")
        return
    
    print("✅ All pre-flight checks passed!")
    print("=" * 50)
    
    # Initialize credit tracker with PacketStream credentials
    api_key = "AIzaSyDD8LALkNo36hN295bcI3Wim-LUvlm5G3s"  # From Utils.py
    credit_tracker = CorrectedCreditTracker(
        api_key=api_key,
        proxy_user=proxy_user,  # PacketStream username
        proxy_pass=proxy_pass   # PacketStream password
    )
    
    # Step 1: Get search query first
    print("[INPUT] ENTER YOUR SEARCH QUERY:")
    print("   Examples: 'mobile home parks', 'property management', 'real estate'")
    print("-" * 60)
    base_search = input("Query: ").strip()
    
    # Step 2: Ask which state
    selected_state = get_state_input()
    print(f"\n[SUCCESS] Selected state: {selected_state}")
    
    # Step 3: Fetch counties from counties_data.py
    counties = get_counties_from_data(selected_state)
    if not counties:
        print(f"[ERROR] No counties found for {selected_state}")
        return
    
    # Step 4: Show counties and their coordinates
    display_counties(counties, selected_state)
    
    # Step 5: Ask which counties user wants
    selected_counties = get_county_selection(counties)
    print(f"\n[SUCCESS] Selected counties: {len(selected_counties)} counties")
    
       # Step 6: Ask for output file name
    print("\n" + "="*50)
    print(" OUTPUT FILE CONFIGURATION")
    print("="*50)
    
    print("Enter output file name (will append state):")
    filenm_base = input().strip()
    os.makedirs("Output", exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_filename = os.path.join("Output", f"{filenm_base} - {selected_state} - {timestamp}.xlsx")

    # Confirm before starting
    print(f"\n[INFO] SUMMARY:")
    print(f"Search Query: {base_search}")
    print(f"State: {selected_state}")
    print(f"Counties: {len(selected_counties)} counties selected")
    print(f"Output File: {output_filename}")
    confirm = input("\n Start scraping? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("[CANCELLED] Scraping cancelled.")
        return
    
    # Start scraping
    start_time = time.time()
    print(f"\n[TIME] Start time: {time.strftime('%H:%M:%S')}")
    
    all_state_data = [] # Collect data from all counties

    completed_path = "completed_counties.txt"
    completed = set()
    if RESUME and os.path.exists(completed_path):
        with open(completed_path, "r", encoding="utf-8") as f:
            completed = {line.strip() for line in f if line.strip()}

    if SHUFFLE_COUNTIES:
        random.shuffle(selected_counties)

    for i, county in enumerate(selected_counties, 1):
        county_full = f"{county['name']}, {selected_state}"
        if RESUME and f"{county['name']},{selected_state}" in completed:
            print(f"[RESUME] Skipping already completed: {county_full}")
            continue
        
        search_term = f"{base_search} in {county_full}"
        
        print(f"\n[PROGRESS] County {i}/{len(selected_counties)}: {county_full}")
        print(f" Coords: {county['lat']:.4f}, {county['lon']:.4f}")
        print(f"[SEARCH] Search term: {search_term}")
        
        try:
            # Create scraper for each county
            out_name = f"{filenm_base} - {county['name']}_{selected_state}"
            s = Scraper(search_term, "", county['lat'], county['lon'], credit_tracker)
            county_data = s.start_and_return_data()

            # Track credits used for this query/county
            # Each business address lookup uses 1 geocoding API call
            businesses_found = len(county_data)
            
            # Track query statistics (no costs, just usage)
            credit_tracker.track_query(
                query=base_search,
                state=selected_state,
                county=county['name'],
                businesses_found=businesses_found
            )
            
            print(f"[SUCCESS] Completed {county['name']} - {businesses_found} businesses found")
            print(f"[USAGE] Businesses found: {businesses_found}")
            print(f"[PACKETSTREAM] Cost so far: ${credit_tracker.packetstream_cost:.2f}")
            print(f"[GOOGLE API] Requests: {credit_tracker.google_api_requests_made}")

            # Add county information to each business record
            for business in county_data:
                business['County'] = county['name']
                business['State'] = selected_state
                all_state_data.append(business)
            
            if AUTOSAVE_EVERY_COUNTIES > 0 and (i % AUTOSAVE_EVERY_COUNTIES == 0):
                pd.DataFrame(all_state_data).to_excel(output_filename, index=False)
                print(f"[AUTOSAVE] Progress saved to {output_filename}")

            if RESUME:
                with open(completed_path, "a", encoding="utf-8") as f:
                    f.write(f"{county['name']},{selected_state}\n")

        except Exception as e:
            print(f"[ERROR] Error scraping {county['name']}: {e}")
            continue
    
    total_time = time.time() - start_time
    print(f"\n[SUCCESS] All counties completed in {total_time:.1f} seconds")
    
      # Save all collected data to a single state file
    if all_state_data:
        try:
            df = pd.DataFrame(all_state_data)
            df.to_excel(output_filename, index=False)
            print(f"\n[SUCCESS] All data saved to {output_filename}")
        except Exception as e:
            print(f"[ERROR] Error saving state-level file: {e}")
       
    else:
        print("[ERROR] No data collected to save.")
    
    # Generate final credit report
    print("\n" + "="*60)
    print("[REPORT] GENERATING CREDIT USAGE REPORT")
    print("="*60)
    
    credit_tracker.get_final_report()

if __name__ == '__main__':
    main()
    
    # Keep the window open after completion
    print("\n" + "="*60)
    print("[COMPLETE] SCRAPING COMPLETED!")
    print("="*60)
    print("Press Enter to close the program...")
    input()
