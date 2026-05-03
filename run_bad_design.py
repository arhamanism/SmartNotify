# run_bad_design.py
"""
Runs the BAD implementation demo — shows the tightly coupled,
anti-pattern version of the notification system.

Run:  python run_bad_design.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bad_design.bad_implementation import run_bad_demo

if __name__ == "__main__":
    run_bad_demo()
