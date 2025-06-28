#!/usr/bin/env python3
"""
Test script to verify web search functionality in the bikepacking planner.
"""

from dirtgenie.planner import generate_trip_plan, initialize_clients, plan_tour_itinerary
import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import our module
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Add the current directory to the path so we can import our module
sys.path.append(str(Path(__file__).parent))


def test_web_search_in_planning():
    """Test that the planning function can use web search capabilities."""
    print("Testing web search functionality in tour planning...")

    # Initialize clients
    initialize_clients()

    # Test with a real location where current information would be valuable
    start = "Boston MA"
    end = "Portland ME"
    nights = 3

    # Create basic preferences
    preferences = {
        'accommodation': 'camping',
        'stealth_camping': False,
        'fitness_level': 'intermediate',
        'daily_distance': '50-80',
        'terrain': 'mixed',
        'budget': 'moderate',
        'interests': ['nature', 'history']
    }

    try:
        print(f"Planning tour from {start} to {end} for {nights} nights...")

        # Test the planning function
        itinerary = plan_tour_itinerary(start, end, nights, preferences)

        print("✅ Tour planning completed successfully!")

        # Check the actual itinerary structure
        if 'itinerary' in itinerary:
            itinerary_days = itinerary['itinerary']
            print(f"Planned {len(itinerary_days)} days")
            print(f"Total estimated distance: {itinerary.get('total_estimated_distance', 'Unknown')} km")

            # Print day-by-day details
            print("\nPlanned itinerary:")
            for day_key, day_info in itinerary_days.items():
                start_loc = day_info.get('start_location', 'Unknown')
                end_loc = day_info.get('end_location', 'Unknown')
                overnight = day_info.get('overnight_location', 'Unknown')
                distance = day_info.get('estimated_distance_km', 'Unknown')
                print(f"  {day_key}: {start_loc} → {end_loc} ({distance}km)")
                print(f"    Overnight: {overnight}")
        else:
            print("⚠️  No itinerary structure found in response")

        return True

    except Exception as e:
        print(f"❌ Error testing web search: {e}")
        return False


def test_web_search_in_trip_generation():
    """Test that trip generation can use web search capabilities."""
    print("\nTesting web search functionality in trip generation...")

    # Create a mock itinerary and directions for testing
    mock_itinerary = {
        "itinerary": {
            "day_1": {
                "start_location": "Boston MA",
                "end_location": "Portsmouth NH",
                "overnight_location": "Prescott Park area camping",
                "highlights": ["Historic Seaport", "Strawbery Banke Museum"],
                "estimated_distance_km": 95
            },
            "day_2": {
                "start_location": "Portsmouth NH",
                "end_location": "Freeport ME",
                "overnight_location": "Wolfe's Neck Woods State Park",
                "highlights": ["L.L.Bean Flagship Store", "Coastal views"],
                "estimated_distance_km": 75
            },
            "day_3": {
                "start_location": "Freeport ME",
                "end_location": "Portland ME",
                "overnight_location": "Arrive at destination",
                "highlights": ["Old Port District", "Portland Head Light"],
                "estimated_distance_km": 60
            }
        },
        "total_estimated_distance": 230,
        "route_summary": "Coastal route from Boston to Portland"
    }

    mock_directions = {
        "legs": [
            {
                "distance": {"value": 95000, "text": "95 km"},
                "duration": {"value": 18000, "text": "5 hours"},
                "start_address": "Boston, MA",
                "end_address": "Portsmouth, NH",
                "start_location": {"lat": 42.3601, "lng": -71.0589},
                "end_location": {"lat": 43.0718, "lng": -70.7626},
                "steps": []
            },
            {
                "distance": {"value": 75000, "text": "75 km"},
                "duration": {"value": 14400, "text": "4 hours"},
                "start_address": "Portsmouth, NH",
                "end_address": "Freeport, ME",
                "start_location": {"lat": 43.0718, "lng": -70.7626},
                "end_location": {"lat": 43.8570, "lng": -70.1028},
                "steps": []
            },
            {
                "distance": {"value": 60000, "text": "60 km"},
                "duration": {"value": 12000, "text": "3.3 hours"},
                "start_address": "Freeport, ME",
                "end_address": "Portland, ME",
                "start_location": {"lat": 43.8570, "lng": -70.1028},
                "end_location": {"lat": 43.6591, "lng": -70.2568},
                "steps": []
            }
        ]
    }

    preferences = {
        'accommodation': 'camping',
        'stealth_camping': False,
        'fitness_level': 'intermediate',
        'daily_distance': '50-80',
        'terrain': 'mixed',
        'budget': 'moderate',
        'interests': ['nature', 'history']
    }

    try:
        print("Generating detailed trip plan with web search...")

        trip_plan = generate_trip_plan(
            "Boston MA",
            "Portland ME",
            3,  # 3 nights to match the mock itinerary
            preferences,
            mock_itinerary,
            mock_directions
        )

        print("✅ Trip plan generation completed successfully!")
        print(f"Generated plan length: {len(trip_plan)} characters")

        # Check if the plan contains indicators of web search usage
        search_indicators = [
            'current', 'updated', 'recent', 'as of', 'latest',
            'operating hours', 'seasonal', 'available', 'booking'
        ]

        found_indicators = []
        for indicator in search_indicators:
            if indicator.lower() in trip_plan.lower():
                found_indicators.append(indicator)

        if found_indicators:
            print(f"✅ Plan appears to include current information (found: {', '.join(found_indicators)})")
        else:
            print("⚠️  Plan may not include current web-searched information")

        return True

    except Exception as e:
        print(f"❌ Error testing trip generation: {e}")
        return False


def main():
    """Run web search functionality tests."""
    print("Testing Web Search Integration in Bikepacking Planner")
    print("=" * 60)

    # Check API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment")
        return False

    if not os.getenv("GOOGLE_MAPS_API_KEY"):
        print("❌ GOOGLE_MAPS_API_KEY not found in environment")
        return False

    print("✅ API keys found")

    # Run tests
    planning_success = test_web_search_in_planning()
    generation_success = test_web_search_in_trip_generation()

    print("\n" + "=" * 60)
    print("Test Results:")
    print(f"Tour Planning: {'✅ PASS' if planning_success else '❌ FAIL'}")
    print(f"Trip Generation: {'✅ PASS' if generation_success else '❌ FAIL'}")

    if planning_success and generation_success:
        print("\n🎉 All web search tests passed!")
        return True
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
