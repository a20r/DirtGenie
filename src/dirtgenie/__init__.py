"""
DirtGenie - AI-Powered Bikepacking Trip Planner

An intelligent trip planner that creates detailed bikepacking itineraries
using OpenAI's GPT models and Google Maps routing data.
"""

__version__ = "1.1.0"
__author__ = "Alex Wallar"
__email__ = "alex@wallar.me"

from .planner import (create_default_profile, create_geojson, generate_trip_plan, get_multi_waypoint_directions,
                      initialize_clients, plan_tour_itinerary, revise_trip_plan_with_feedback)

__all__ = [
    "create_default_profile",
    "create_geojson",
    "generate_trip_plan",
    "get_multi_waypoint_directions",
    "initialize_clients",
    "plan_tour_itinerary",
    "revise_trip_plan_with_feedback",
]
