import re
from collections import defaultdict

def find_patterns_in_words(filename):
    pattern_counts = defaultdict(int)
    pattern = r"c(.i)" # Regular expression pattern: 'c' followed by any character and then 'i'
    
    with open(filename, "r") as file:
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

def print_pattern_stats(pattern_counts):
    total = sum(pattern_counts.values())
    
    if total == 0:
        print("No data to display.")
        return

    # Sort the dictionary by values in descending order
    sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Print the results
    print(f"{'Pattern':<10} {'Count':<10} {'Percentage':<10}")
    print("-" * 30)
    
    for pattern, count in sorted_patterns:
        percentage = (count / total) * 100
        print(f"{pattern:<10} {count:<10} {percentage:>6.2f}%")

# Example usage
matches = find_patterns_in_words("words.txt")
print_pattern_stats(matches)