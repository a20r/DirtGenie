#!/usr/bin/env python3
"""
Test script to verify the revise_trip_plan_with_feedback fix.
"""
from dirtgenie.planner import initialize_clients, revise_trip_plan_with_feedback
import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_revision_with_mock_data():
    """Test the revision function with mock data to ensure it doesn't crash with NoneType error."""

    print("🧪 Testing revision function fix...")

    # Initialize clients first
    try:
        initialize_clients()
        print("✅ Clients initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize clients: {e}")
        return False

    # Mock data for testing
    original_plan = """
# Test Trip Plan
This is a test bikepacking trip from Boston to Vermont.

## Day 1
- Start in Boston
- Cycle 50km
- Stay at camping area
    """

    feedback = "Make the daily distances shorter, around 30km per day"

    mock_preferences = {
        'accommodation': 'camping',
        'fitness_level': 'beginner',
        'daily_distance': '30-50',
        'terrain': 'mixed',
        'budget': 'moderate',
        'interests': ['nature'],
        'stealth_camping': False,
        'tire_size': '700x35c'
    }

    mock_itinerary = {
        'itinerary': {
            'day_1': {
                'start_location': 'Boston, MA',
                'end_location': 'Cambridge, MA',
                'overnight_location': 'Local camping',
                'estimated_distance_km': 20
            }
        }
    }

    mock_directions = {
        'legs': [
            {
                'distance': {'value': 20000, 'text': '20 km'},  # 20km in meters
                'duration': {'value': 3600, 'text': '1 hour'},    # 1 hour in seconds
                'start_address': 'Boston, MA, USA',
                'end_address': 'Cambridge, MA, USA',
                'steps': []
            }
        ]
    }

    try:
        # Test the revision function
        print("🔄 Testing revision function...")
        revised_plan = revise_trip_plan_with_feedback(
            original_plan=original_plan,
            feedback=feedback,
            start="Boston, MA",
            end="Cambridge, MA",
            nights=1,
            preferences=mock_preferences,
            itinerary=mock_itinerary,
            directions=mock_directions,
            departure_date=None
        )

        if revised_plan and "Error" not in revised_plan:
            print("✅ Revision function executed successfully!")
            print(f"📝 Revised plan length: {len(revised_plan)} characters")
            print("🎉 NO MORE 'NoneType' object has no attribute 'chat' ERROR!")
            return True
        else:
            print(f"❌ Revision function returned an error: {revised_plan}")
            return False

    except Exception as e:
        import traceback
        print(f"❌ Revision function failed with error: {e}")
        print("Full traceback:")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_revision_with_mock_data()
    if success:
        print("\n🎉 SUCCESS: The revision bug has been fixed!")
        sys.exit(0)
    else:
        print("\n❌ FAILURE: The revision bug still exists.")
        sys.exit(1)
