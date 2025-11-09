
from datetime import datetime
import os
import json

def clean_data(submissions):
    data = []
    for sub in submissions:
        problem = sub.get('problem', {})
        ts = sub.get('creationTimeSeconds')
        data.append({
            'problem_name': problem.get('name'),
            'tags': problem.get('tags', []),
            'rating': problem.get('rating'),
            'verdict': sub.get('verdict'),
            'creationTimeSeconds': sub.get('creationTimeSeconds')
        })
    return data

def save_cleaned_data(data, output_file_path="data/cleaned_submissions.json"):
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved cleaned data to {output_file_path} ({len(data)} submissions)")


# Quick test
if __name__ == "__main__":
    from api.codeforces_api import fetch_submissions
    handle = input("Enter handle: ")
    subs = fetch_submissions(handle)
    cleaned_data = clean_data(subs)
    save_cleaned_data(cleaned_data)
