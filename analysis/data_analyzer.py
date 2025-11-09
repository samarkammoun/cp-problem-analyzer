import json
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime


def load_data(file_path="data/cleaned_submissions.json"):
    #with is a context manager, it automatically closes the file when done, so you don’t have to call f.close()
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

    # json.load(f) reads the contents of the file, which must be in JSON format, and converts it into Python objects:
    # JSON objects → Python dictionaries (dict)
    # JSON arrays → Python lists (list)
    # Strings, numbers, booleans, null → Python equivalents

def analyze_data(submissions):
    tags_counter = Counter()
    verdict_counter = Counter()
    rating_counter = Counter()
    timeline = Counter()

    for sub in submissions:
        # update counter for the tags
        tags_counter.update(sub.get("tags",[]))

        # update counter for the verdicts
        verdict_counter[sub.get("verdict","UNKNOWN")]+=1

        # update counter for the ratings
        if sub.get("rating"):
            rating_counter[sub["rating"]]+=1

        # Timeline (convert unix time to month)
        date = datetime.fromtimestamp(sub["creationTimeSeconds"]).strftime("%Y-%m")
        timeline[date] += 1

    return {
        "tags": tags_counter,
        "verdicts": verdict_counter,
        "ratings": rating_counter,
        "timeline": timeline
    }

def plot_stats(stats):
    # Tags
    plt.figure(figsize=(8, 4))
    plt.bar(stats["tags"].keys(), stats["tags"].values())
    plt.title("Problems by Topic")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Verdicts
    plt.figure(figsize=(6, 4))
    plt.bar(stats["verdicts"].keys(), stats["verdicts"].values(), color="orange")
    plt.title("Verdict Distribution")
    plt.tight_layout()
    plt.show()

    # Rating
    plt.figure(figsize=(6, 4))
    plt.bar(stats["ratings"].keys(), stats["ratings"].values(), color="green")
    plt.title("Problem Ratings")
    plt.tight_layout()
    plt.show()

    # Timeline
    plt.figure(figsize=(8, 4))
    plt.plot(list(stats["timeline"].keys()), list(stats["timeline"].values()), marker="o")
    plt.title("Accepted Submissions Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Most rating per month
    avg_ratings = difficulty_trend(data)
    months = list(avg_ratings.keys())
    ratings = list(avg_ratings.values())

    plt.figure(figsize=(10, 4))
    plt.plot(months, ratings, marker='o')
    plt.title("Average Rating of Accepted Problems Over Time")
    plt.xlabel("Month")
    plt.ylabel("Average Rating")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def topic_success_rates(submissions):
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

def difficulty_trend(submissions):
    monthly_ratings = {}

    for s in submissions:
        if s.get("verdict") == "OK" and s.get("rating"):
            # Convert timestamp to month string
            month = datetime.fromtimestamp(s["creationTimeSeconds"]).strftime("%Y-%m")
            if month not in monthly_ratings:
                monthly_ratings[month] = Counter()
            monthly_ratings[month][s.get("rating")]+=1

    avg_ratings = {month: max(monthly_ratings.get(month), key=monthly_ratings.get(month).get) for month in monthly_ratings}
    return avg_ratings


if __name__ == "__main__":
    data = load_data()
    stats = analyze_data(data)
    plot_stats(stats)
    success_rate, attempts, accepted = topic_success_rates(data)
    sorted_topics = sorted(success_rate.items(), key=lambda x: x[1])
    # 5 weakest topics
    weakest = sorted_topics[:5]
    # 5 strongest topics
    strongest = sorted_topics[-5:]

    #print("Weakest topics:", weakest)
    #print("Strongest topics:", strongest)
    #print(difficulty_trend(data))