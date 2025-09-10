#!/usr/bin/env python3
"""
Content Maker - Main entry point
"""

import sys
import os

# Add src to path so we can import from the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main function
from content_maker.core.main import main

if __name__ == "__main__":
    main()