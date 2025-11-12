import os
import json
from api.codeforces_api import fetch_submissions, fetch_contest

# Extracts and normalizes submission data from the Codeforces API response.
def clean_submissions(submissions):
    cleaned_data = []
    for sub in submissions:
        problem = sub.get('problem', {})
        cleaned_data.append({
            'contestId': problem.get('contestId'),
            'problem_name': problem.get('name'),
            'tags': problem.get('tags', []),
            'rating': problem.get('rating'),
            'verdict': sub.get('verdict'),
            'creationTimeSeconds': sub.get('creationTimeSeconds')
        })
    return cleaned_data

# Returns a list of unique contest IDs the user has participated in.
def extract_participated_contests(submissions):
    participated = set()
    for sub in submissions:
        cid = sub.get("contestId")
        if cid:
            participated.add(cid)
    participated = list(participated)
    return participated

def save_cleaned_data(data, output_file_path):
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    # os.path.dirname(output_file_path) extracts the directory portion of the path
    # os.makedirs(dir, exist_ok=True) creates the directory, exist_ok=True means don’t raise an error if the directory already exists
    with open(output_file_path, "w", encoding="utf-8") as f:
        # with is a context manager: it automatically closes the file when the block ends
        # Writes the Python object data to the open file f in JSON format.
        # indent=4 pretty-prints the JSON with 4 spaces indentation so the file is human-readable.
        json.dump(data, f, indent=4)
    print(f"Saved cleaned data to {output_file_path} ({len(data)} submissions)")

# test
if __name__ == "__main__":
    handle = input("Enter Codeforces handle: ")

    # Fetch and clean submissions
    submissions = fetch_submissions(handle)
    cleaned_subs = clean_submissions(submissions)
    save_cleaned_data(cleaned_subs, "data/cleaned_submissions.json")

    # Fetch and save all contests (used later for analysis)
    all_contests = fetch_contest()
    save_cleaned_data(all_contests, "data/contests_stats.json")

    # Save participated contests for the user
    user_contests = extract_participated_contests(cleaned_subs)
    save_cleaned_data(user_contests, "data/user_participated_contests.json")
