
# **Codeforces Progress Tracker**

A Python-based analytical tool that helps Codeforces users visualize their competitive programming progress.
It fetches your submissions, cleans and analyzes the data, and presents insightful visualizations through an interactive Streamlit dashboard.

---

## **Table of Contents**

* [Overview](#overview)
* [Features](#features)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Requirements](#requirements)
* [License](#license)

---

## **Overview**

This project analyzes a user's Codeforces activity by fetching their submission and contest data from the Codeforces API.
It provides clear statistics about performance, participation, and progress and helps you understand your strengths and weaknesses across topics, contests, and time.

---

## **Features**

### **1. Data Fetching and Integration**

* Fetches a user’s **Codeforces submissions** and **contest metadata** via the Codeforces API.
* Automatically saves fetched data in JSON format under the `data/` directory for reusability.

### **2. Data Cleaning and Preprocessing**

* Removes duplicates and invalid submissions.
* Converts timestamps into readable dates.
* Extracts participated contests from submissions.
* Saves cleaned data as `cleaned_submissions.json`.

### **3. Analytical Insights**

* **Verdict Analysis:** Counts Accepted, Wrong Answer, Time Limit, and other verdicts.
* **Timeline Analysis:** Tracks submission activity over time.
* **Topic Success Rate:** Computes success/failure rates for each problem topic.
* **Contest Division Analysis:** Counts participation in Div. 1, Div. 2, Div. 3, and Div. 4 contests.
* **Rating Trend Analysis:** Shows problem rating evolution over time.

### **4. Interactive Visualizations (Streamlit)**

* Displays **bar charts** for verdict distribution.
* Displays **line charts** for submission timelines.
* Displays **pie/bar charts** for division participation.
* Highlights **strongest and weakest topics** based on success rate.
* Shows **difficulty/rating progression** over time.

### **5. User Interaction**

* Streamlit input field for entering a Codeforces handle.
* “Analyze” button triggers full analysis workflow.
* Displays informative status messages and warnings during execution.

### **6. Data Management**

* Stores all cleaned and analyzed data locally.
* Supports reloading from JSON for faster reuse.
* Clean module separation between fetching, cleaning, and analysis.

### **7. Modular Architecture**

* Organized into packages:

  * `api/` → API communication
  * `analysis/` → Data cleaning and analysis
  * `ui/` → Streamlit dashboard
* Uses `__init__.py` for proper package recognition.
* Extensible structure for adding new modules and features.

### **8. Technical Highlights**

* Built with **Python** and **Streamlit**.
* Uses **pandas** for data analysis and visualization.

---

## **Project Structure**

```
cp-problem-analyzer/
│
├── api/
│   ├── __init__.py
│   └── codeforces_api.py
│
├── analysis/
│   ├── __init__.py
│   ├── data_cleaner.py
│   └── data_analyzer.py
│
├── ui/
│   ├── __init__.py
│   └── app.py
│
├── data/
│   ├── cleaned_submissions.json
│   ├── contests_stats.json
│
├── requirements.txt
└── README.md
```

---

## **Installation**

1. Clone the repository:

   ```bash
   git clone https://github.com/samarkammoun/cp-problem-analyzer.git
   cd cp-problem-analyzer
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # On Windows
   pip install -r requirements.txt
   ```

---

## **Usage**

1. Run the Streamlit interface:

   ```bash
   streamlit run ui/app.py
   ```

2. Enter your **Codeforces handle** and click **Analyze**.

3. Explore:

   * Verdict charts
   * Timeline trends
   * Topic success rates
   * Contest division statistics

---

## **Requirements**

This project requires the following Python libraries:

* streamlit
* pandas
* requests

(Full list in `requirements.txt`.)

---

## **License**

This project is licensed under the [MIT License](LICENSE).
You are free to use, modify, and distribute this project with proper attribution.
