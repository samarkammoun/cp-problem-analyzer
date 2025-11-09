import requests

def fetch_submissions(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    # The f at the start of the url means it’s an f-stringAn f-string allows you to insert variables or expressions directly inside a string using {}
    response = requests.get(url)
    # print(response.status_code)
    data = response.json() # Parses it from JSON (string) to a Python dictionary
    if data['status'] != 'OK':
        raise Exception("Invalid handle or API error")

    return data['result']

# Quick test
if __name__ == "__main__":
    handle = input("Enter Codeforces handle: ")
    submissions = fetch_submissions(handle)
    print(f"Fetched {len(submissions)} submissions.")

