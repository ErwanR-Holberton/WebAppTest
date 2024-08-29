if __name__ != "__main__":
    from FlaskApp import *
import os
import re
from collections import defaultdict

prefix = "/Pattern_fr/"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_dir, 'words.txt')

def find_patterns_in_words():
    pattern_counts = defaultdict(int)
    pattern = r"c(.i)" # Regular expression pattern: 'c' followed by any character and then 'i'
    
    with open(file_path, "r") as file:
        lines = file.readlines()
        
    for line in lines:
        word = line.strip()  # Remove any surrounding whitespace or newline characters
        # Find all matches in the word
        matches = re.findall(pattern, word)
        for match in matches:
            # match[0] is the single letter found
            key = f"c{match[0]}i"
            pattern_counts[key] += 1

    # Convert defaultdict to a regular dict for returning
    return dict(pattern_counts)

def get_pattern_data():
    pattern_counts = find_patterns_in_words()

    # Calculate the total sum of all values
    total = sum(pattern_counts.values())

    # Check if there is any data to avoid division by zero
    if total == 0:
        return []

    # Calculate percentages and prepare the sorted list
    sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
    results = [(pattern, count, (count / total) * 100) for pattern, count in sorted_patterns]
    
    return results


def routes():
    @app.route(prefix)
    def index_Pattern_fr():
        results = get_pattern_data()
        return render_template(prefix + 'patterns.html', results=results)

