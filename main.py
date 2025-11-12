

from api.codeforces_api import fetch_submissions
from analysis.data_cleaner import clean_submissions

handle=input("Enter Codeforces handle: ")
print("\nFetching data...")
subs = fetch_submissions(handle)
print(f"{len(subs)} submissions fetched.")

print("\nCleaning data...")
df = clean_submissions(subs)
print("Data cleaned. Preview:")
print(df.head())