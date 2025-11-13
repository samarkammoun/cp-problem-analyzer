import os
import sys

# Add project root to Python path dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
import streamlit as st
from api.codeforces_api import fetch_submissions, fetch_contest
from analysis.data_cleaner import clean_submissions, save_cleaned_data, extract_participated_contests
from analysis.data_analyzer import analyze_submissions, compute_topic_success_rates, compute_rating_trend, analyze_contest_divisions, load_data

st.title("Codeforces Progress Tracker")

handle = st.text_input("Enter your Codeforces handle:")
if st.button("Analyze"):
    if not handle:
        st.warning("Please enter a valid handle.")
    else:
        st.info(f"Fetching data for {handle}...")

        # Step 1: Fetch + clean submissions
        submissions = fetch_submissions(handle)
        cleaned_subs = clean_submissions(submissions)
        save_cleaned_data(cleaned_subs, "data/cleaned_submissions.json")

        # Step 2: Fetch contests
        contests = fetch_contest()
        save_cleaned_data(contests, "data/contests_stats.json")

        # Step 3: Load data
        submissions_data = load_data("data/cleaned_submissions.json")
        contests_data = load_data("data/contests_stats.json")

        # Submissions analysis
        submissions_stats = analyze_submissions(submissions_data)

        # Topic success rates
        success_rate, attempts, accepted = compute_topic_success_rates(submissions_data)
        sorted_topics = sorted(success_rate.items(), key=lambda x: x[1])
        weakest = sorted_topics[:5]
        strongest = sorted_topics[-5:]

        st.subheader("Weakest Topics")
        st.table(pd.DataFrame(weakest, columns=["Topic", "Success Rate"]))

        st.subheader("Strongest Topics")
        st.table(pd.DataFrame(strongest, columns=["Topic", "Success Rate"]))

        # Verdict distribution
        st.subheader("Verdict Distribution")
        st.bar_chart(pd.DataFrame(submissions_stats["verdicts"], index=[0]).T)

        # Submissions over time
        st.subheader("Submissions Over Time")
        timeline_df = pd.DataFrame(list(submissions_stats["timeline"].items()), columns=["Month", "Submissions"])
        timeline_df = timeline_df.sort_values("Month")
        st.line_chart(timeline_df.set_index("Month"))

        # Difficulty / Rating trend
        st.subheader("Problem Rating Trend")
        rating_trend = compute_rating_trend(submissions_data)
        rating_df = pd.DataFrame(list(rating_trend.items()), columns=["Month", "Most Solved Rating"])
        rating_df = rating_df.sort_values("Month")
        st.line_chart(rating_df.set_index("Month"))

        # Contest participation
        st.subheader("Contest Division Participation")
        participated_contests = extract_participated_contests(submissions_data)
        participated_contests = map(str, participated_contests)  # Ensure string IDs
        div_stats = analyze_contest_divisions(contests_data, participated_contests)

        # Visualize divisions as bar chart
        divs_df = pd.DataFrame(list(div_stats.items()), columns=["Division", "Count"])
        divs_df = divs_df.sort_values("Division")  # from Div.1 to Div.4
        st.bar_chart(divs_df.set_index("Division"))

        st.success("Analysis Complete!")

