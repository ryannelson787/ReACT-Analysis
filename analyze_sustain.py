import csv

# Path to the CSV file to read
csv_file = 'sust_scores.csv'

scores = []

# Open the CSV file in read mode
with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)  # Use DictReader to read rows as dictionaries

    # Loop through each row in the CSV file
    for row in reader:
        # Access the data from the row (it's a dictionary)
        score = row['score']

        scores.append(score)

scores = [float(score) for score in scores]
avg = sum(scores) / len(scores)
print(f"AVG: {avg}")
scores.sort()
print("Highest: ", scores[0])
print("Lowest: ", scores[-1])
print("Above 50", sum(1 for score in scores if score > 50))
print("Above 60", sum(1 for score in scores if score > 60))
print("Above 70", sum(1 for score in scores if score > 70))