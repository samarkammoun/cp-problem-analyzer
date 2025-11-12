import json
import re
from collections import Counter
from datetime import datetime
from analysis.data_cleaner import extract_participated_contests

# Loads and parses JSON data from the given file path.
def load_data(file_path):
    #with is a context manager, it automatically closes the file when done, so you don’t have to call f.close()
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    # json.load(f) reads the contents of the file, which must be in JSON format, and converts it into Python objects:
    # JSON objects → Python dictionaries (dict)
    # JSON arrays → Python lists (list)
    # Strings, numbers, booleans, null → Python equivalents

def analyze_submissions(submissions):
    tags_counter = Counter()
    verdict_counter = Counter()
    rating_counter = Counter()
    timeline = Counter()

    for sub in submissions:
        # update counter for the tags
        # Problems solved per topic (tags)
        tags_counter.update(sub.get("tags",[]))

        # update counter for the verdicts
        # Verdict distribution
        verdict_counter[sub.get("verdict","UNKNOWN")]+=1

        # update counter for the ratings
        # Submissions per rating
        if sub.get("rating"):
            rating_counter[sub["rating"]]+=1

        # Timeline (convert unix time to month)
        # Activity timeline (per month)
        date = datetime.fromtimestamp(sub["creationTimeSeconds"]).strftime("%Y-%m")
        timeline[date] += 1

    return {
        "tags": tags_counter,
        "verdicts": verdict_counter,
        "ratings": rating_counter,
        "timeline": timeline
    }

# Calculates success rate per topic (tag). success_rate = accepted_submissions / total_attempts
def compute_topic_success_rates(submissions):
    attempts = Counter()
    accepted = Counter()

    for sub in submissions:
        tags = sub.get("tags", [])
        verdict = sub.get("verdict")
        for tag in tags:
            attempts[tag] += 1
            if verdict == "OK":
                accepted[tag] += 1

    success_rate = {tag: accepted[tag]/attempts[tag] for tag in attempts}
    return success_rate, attempts, accepted

# Computes the average solved problem rating per month based on 'OK' verdicts.
def compute_rating_trend(submissions):

    monthly_ratings = {}
    for s in submissions:
        if s.get("verdict") == "OK" and s.get("rating"):
            # Convert timestamp to month string
            month = datetime.fromtimestamp(s["creationTimeSeconds"]).strftime("%Y-%m")
            if month not in monthly_ratings:
                monthly_ratings[month] = Counter()
            monthly_ratings[month][s.get("rating")]+=1

    # Average (most frequent) rating per month
    avg_ratings = {month: max(monthly_ratings.get(month), key=monthly_ratings.get(month).get) for month in monthly_ratings}
    return avg_ratings

# Counts how many Div.1, Div.2, Div.3, Div.4 contests the user has participated in.
def analyze_contest_divisions(contests, participated):
    stats = {"Div.1": 0, "Div.2": 0, "Div.3": 0, "Div.4": 0}
    for cid in participated:
        contest = contests.get(cid)
        if contest is None:
            continue
        # re = regular expression engine
        # Used for text pattern matching, searching, replacing, validation
        name = contest.get("name", "")
        if re.search(r"Div\. ?1", name):
            stats["Div.1"] += 1
        elif re.search(r"Div\. ?2", name):
            stats["Div.2"] += 1
        elif re.search(r"Div\. ?3", name):
            stats["Div.3"] += 1
        elif re.search(r"Div\. ?4", name):
            stats["Div.4"] += 1
    return stats

# data visualization test
if __name__ == "__main__":
    # Load cleaned data
    submissions_data = load_data("data/cleaned_submissions.json")
    contests_data = load_data("data/contests_stats.json")

    # Submissions analysis
    submissions_stats = analyze_submissions(submissions_data)
    success_rate, attempts, accepted = compute_topic_success_rates(submissions_data)
    sorted_topics = sorted(success_rate.items(), key=lambda x: x[1])

    # Display strongest and weakest topics
    weakest = sorted_topics[:5]
    strongest = sorted_topics[-5:]
    print("Weakest topics:", weakest)
    print("Strongest topics:", strongest)

    # Difficulty trend
    print("Rating trend:", compute_rating_trend(submissions_data))

    # Contest participation
    participated_contests = extract_participated_contests(submissions_data)
    # because the contest IDs in contests_stats.json are strings
    participated_contests = map(str,participated_contests)
    div_stats = analyze_contest_divisions(contests_data, participated_contests)
    print("Contest Division Stats:", div_stats)

