#!/usr/bin/env python3
"""
Simple launcher for the Snake Game
"""

import sys
import os

def main():
    """Launch the Snake Game with error handling"""
    
    print("🐍 Starting Snake Game - Multi-Player AI Battle")
    print("=" * 50)
    
    # Check if the main game file exists
    if not os.path.exists('snake_game.py'):
        print("❌ Error: snake_game.py not found!")
        print("Make sure you're in the correct directory.")
        sys.exit(1)
    
    try:
        # Import and run the game
        import snake_game
        print("✅ Game started successfully!")
        print("Use WASD keys to control your green snake.")
        print("Compete against 3 AI opponents for 60 seconds!")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure Python tkinter is installed:")
        print("  sudo apt-get install python3-tk  # Linux")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print("Check the console for more details.")
        sys.exit(1)

if __name__ == "__main__":
    main()