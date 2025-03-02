import urllib.error
import urllib.request
import json
import argparse


def fetch_github_activity(username):
    url = f'https://api.github.com/users/{username}/events'
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            status_code = response.getcode()
        return json.loads(data), status_code

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: Username '{username}' not found (404).")
            return None, 404
        print(f"HTTP Error: {e.code} - {e.reason}")
        return None, e.code

    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return None, None

    except json.JSONDecodeError:
        print(f"Failed to parse JSON response")
        return None, None

def displayActivity(events):
    i = 1
    for event in events:
        match event["type"]:
            case "PushEvent":
                commitCount = len(event["payload"]["commits"])
                action = f"Pushed {commitCount} commit(s) to {event["repo"]["name"]}"
            case "IssuesEvent":
                action = f"{event["payload"]["action"].capitalize()} an issue in {event["repo"]["name"]}"
            case "WatchEvent":
                action = f"Starred {event["repo"]["name"]}"
            case "ForkEvent":
                action = f"Forked {event["repo"]["name"]}" 
            case "CreateEvent":
                action = f"Created {event["payload"]["ref_type"]} in {event["repo"]["name"]}"
            case _:
                action = f"{event["type"].replace("Event","")} in {event["repo"]["name"]}"
        print(f"{i}  -  {action}")
        i += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Github User Activity CLI-based")
    parser.add_argument("username", type=str, help="Github username to fetch activity")
    args = parser.parse_args()
    if args.username == "" or args.username == " ":
        print("Invalid username input. Please insert appropiate value.")
    else:
        events, status_code = fetch_github_activity(args.username)
        displayActivity(events)