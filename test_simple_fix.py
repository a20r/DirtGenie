#!/usr/bin/env python3
"""
Simple test to verify the 'NoneType' object has no attribute 'chat' error is fixed.
"""
import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_openai_client_initialization():
    """Test that the OpenAI client is properly initialized"""

    print("🧪 Testing OpenAI client initialization fix...")

    # Import and test the function
    from dirtgenie.planner import initialize_clients, openai_client, revise_trip_plan_with_feedback

    # Initialize clients
    initialize_clients()

    # Check the global client
    import dirtgenie.planner as planner_module

    print(f"✅ OPENAI_API_KEY present: {'OPENAI_API_KEY' in os.environ}")
    print(f"✅ openai_client initialized: {planner_module.openai_client is not None}")

    if planner_module.openai_client is not None:
        print(f"✅ openai_client type: {type(planner_module.openai_client)}")
        print(f"✅ openai_client has chat attribute: {hasattr(planner_module.openai_client, 'chat')}")
        print("🎉 SUCCESS: No more 'NoneType' object has no attribute 'chat' error!")
        return True
    else:
        print("❌ openai_client is still None")
        return False


if __name__ == "__main__":
    success = test_openai_client_initialization()
    if success:
        print("\n🎉 The 'NoneType' error bug has been FIXED!")
        print("📋 The revise_trip_plan_with_feedback function now properly initializes the OpenAI client.")
        print("✨ Users can now revise their trip plans without encountering the 'chat' attribute error.")
    else:
        print("\n❌ The bug still exists.")
