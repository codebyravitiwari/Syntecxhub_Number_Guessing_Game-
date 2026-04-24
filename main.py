#!/usr/bin/env python3
"""
Number Guessing Game - Professional CLI Edition
A polished terminal-based guessing game with difficulty levels, high score tracking,
and robust input validation.
"""

import random
import json
import os
import sys
from typing import Dict, Optional, Tuple

SCORES_FILE = 'scores.json'
BORDERS = {
    'top': '╔' + '═' * 50 + '╗',
    'bottom': '╚' + '═' * 50 + '╝',
    'side': '║',
    'fill': '═'
}

DIFFICULTIES = {
    'easy': {'min': 1, 'max': 50, 'attempts': 15},
    'medium': {'min': 1, 'max': 100, 'attempts': 10},
    'hard': {'min': 1, 'max': 500, 'attempts': 7}
}

PERFORMANCE_RATINGS = {
    'excellent': 3,
    'great': 5,
    'good': 8,
    'average': 12,
    'needs_work': float('inf')
}

def clear_screen():
    """Clear the terminal screen cross-platform."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_welcome():
    """Display the welcome screen with ASCII art."""
    clear_screen()
    print(BORDERS['top'])
    print(f"{BORDERS['side']:2}        🎯 NUMBER GUESSING GAME 🎯        {BORDERS['side']}")
    print(BORDERS['bottom'])
    print(f"\\n{BORDERS['side']} I'm thinking of a number! Can you guess it?     {BORDERS['side']}")
    print(f"{BORDERS['side']:2} Use hints: TOO HIGH or TOO LOW!              {BORDERS['side']}")
    print(BORDERS['bottom'])
    print()

def display_menu():
    """Display main menu options."""
    print("Select Difficulty:")
    print("1. 🟢 Easy   (1-50, 15 attempts)")
    print("2. 🟡 Medium (1-100, 10 attempts)")
    print("3. 🔴 Hard   (1-500, 7 attempts)")
    print("4. 📊 View High Scores")
    print("5. ❌ Exit")
    print()

def select_difficulty() -> Optional[str]:
    """Get validated difficulty selection from user."""
    while True:
        try:
            choice = input("Enter choice (1-5): ").strip()
            if choice in ['1', '2', '3']:
                return ['easy', 'medium', 'hard'][int(choice) - 1]
            elif choice == '4':
                display_high_scores()
                input("\\nPress Enter to continue...")
                return None
            elif choice == '5':
                print("Thanks for playing! 👋")
                sys.exit(0)
            else:
                print("\\n❌ Invalid choice. Please select 1-5.")
        except KeyboardInterrupt:
            print("\\n\\nThanks for playing! 👋")
            sys.exit(0)

def display_high_scores():
    """Display current high scores."""
    scores = load_scores()
    clear_screen()
    print(BORDERS['top'])
    print(f"{BORDERS['side']:18} 🏆 HIGH SCORES 🏆 {BORDERS['side']:18}")
    print(BORDERS['bottom'])
    for diff, attempts in scores.items():
        attempts_str = str(attempts) if attempts != float('inf') else '---'
        print(f"{BORDERS['side']} {diff.capitalize():10} : {attempts_str:3} attempts {BORDERS['side']}")
    print(BORDERS['bottom'])

def validate_guess(guess_str: str, min_val: int, max_val: int) -> Optional[int]:
    """Validate and parse user guess."""
    try:
        guess = int(guess_str.strip())
        if min_val <= guess <= max_val:
            return guess
        else:
            print(f"\\n❌ Guess must be between {min_val} and {max_val}")
            return None
    except ValueError:
        print("\\n❌ Please enter a valid number.")
        return None

def get_rating(attempts: int, max_attempts: int) -> str:
    """Determine performance rating based on attempts used."""
    ratio = attempts / max_attempts
    for rating, threshold in PERFORMANCE_RATINGS.items():
        if ratio <= threshold / max(PERFORMANCE_RATINGS['needs_work'], max_attempts):
            return rating.replace('_', ' ').title()
    return 'Needs Work'

def play_game(difficulty: str) -> Tuple[bool, int]:
    """Main game logic."""
    config = DIFFICULTIES[difficulty]
    number = random.randint(config['min'], config['max'])
    max_attempts = config['attempts']
    attempts = 0

    print(f"\\n🎮 {difficulty.capitalize()} mode selected!")
    print(f"Range: {config['min']} - {config['max']} | Max attempts: {max_attempts}")
    print(f"Good luck! (Type 'quit' to exit anytime)\\n")

    while attempts < max_attempts:
        guess_str = input(f"Attempt {attempts + 1}/{max_attempts} - Your guess: ").strip().lower()
        
        if guess_str == 'quit':
            print("Game quit. Better luck next time!")
            return False, 0
        
        guess = validate_guess(guess_str, config['min'], config['max'])
        if guess is None:
            continue
        
        attempts += 1
        
        if guess < number:
            print("📈 Too LOW!")
        elif guess > number:
            print("📉 Too HIGH!")
        else:
            print(f"\\n🎉 CONGRATULATIONS! You got it in {attempts} attempts! 🎉")
            rating = get_rating(attempts, max_attempts)
            print(f"Rating: {rating} ({rating}! {'⭐' * (4 - min(3, attempts // 2))})")
            
            # Update high score
            scores = load_scores()
            if attempts < scores.get(difficulty, float('inf')):
                scores[difficulty] = attempts
                save_scores(scores)
                print("\\n🏆 New high score! 🎉")
            else:
                print(f"\\nCurrent high score: {scores.get(difficulty, '---')} attempts")
            
            return True, attempts
    
    print(f"\\n💥 Game Over! The number was {number}.")
    return False, max_attempts

def load_scores() -> Dict[str, float]:
    """Load high scores from JSON file."""
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r') as f:
                return {k: float(v) for k, v in json.load(f).items()}
        except (json.JSONDecodeError, ValueError):
            pass
    # Initialize with infinity
    return {diff: float('inf') for diff in DIFFICULTIES}

def save_scores(scores: Dict[str, float]):
    """Save high scores to JSON file."""
    os.makedirs(os.path.dirname(SCORES_FILE) if os.path.dirname(SCORES_FILE) else '.', exist_ok=True)
    with open(SCORES_FILE, 'w') as f:
        json.dump({k: int(v) if v != float('inf') else float('inf') for k, v in scores.items()}, f, indent=2)

def main():
    """Main game loop."""
    display_welcome()
    
    while True:
        display_menu()
        difficulty = select_difficulty()
        if difficulty:
            won, attempts = play_game(difficulty)
            print("\\n" + '='*50)
            replay = input("Play again? (y/n): ").strip().lower()
            if replay != 'y':
                print("Thanks for playing! 👋")
                break

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\\n\\nThanks for playing! 👋")
        sys.exit(0)
