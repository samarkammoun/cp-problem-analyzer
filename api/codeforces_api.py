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

def fetch_contest():
    url = "https://codeforces.com/api/contest.list"
    response = requests.get(url)
    data = response.json()
    if data['status'] != 'OK':
        raise Exception("API error")
    contests={}
    for contest in data.get("result"):
        id = contest.get("id")
        contests[id]=contest
    return contests



# testing the api
if __name__ == "__main__":
    handle = input("Enter Codeforces handle: ")
    submissions = fetch_submissions(handle)
    print(f"Fetched {len(submissions)} submissions.")
    print(fetch_contest())


