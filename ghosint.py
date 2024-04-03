# Desc      : GHOSINT - An OSINT tool based on python to get GitHub user information.
# Author    : Hiiruki <hi@hiiruki.dev>
# URL       : https://github.com/hiiruki/ghosint

import requests
import os
from dotenv import load_dotenv

# Font colors
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

prCyan(r"""

   _____ _    _  ____   _____ _____ _   _ _______ 
  / ____| |  | |/ __ \ / ____|_   _| \ | |__   __|
 | |  __| |__| | |  | | (___   | | |  \| |  | |   
 | | |_ |  __  | |  | |\___ \  | | | . ` |  | |   
 | |__| | |  | | |__| |____) |_| |_| |\  |  | |   
  \_____|_|  |_|\____/|_____/|_____|_| \_|  |_|   
                                                  
          GitHub OSINT Tool by @hiiruki           

""")

# Prompt user to enter the username
username = input("Enter the username: ")

# Set up the request headers
headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28" # https://docs.github.com/en/rest/about-the-rest-api/api-versions?apiVersion=2022-11-28
}

# Load environment variables from .env file
load_dotenv()

# Read the token from environment variable
gh_token = os.getenv("GITHUB_TOKEN")

if gh_token is None:
    raise ValueError("GitHub token not found in environment variables")

# Update the Authorization header with the token
headers["Authorization"] = f"Bearer {gh_token}"

# Send the GET request to the GitHub API
# https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#get-a-user
url = f"https://api.github.com/users/{username}"
response = requests.get(url, headers=headers)

# Parse the response JSON into a Python dictionary
user_info = response.json()

# Check if the request was successful (status code 200)
if response.status_code != 200:
    # Print error message if request was not successful
    print("Failed to fetch data from the API:", response.status_code)
    exit()

# Send the GET request to fetch social accounts
social_url = f"https://api.github.com/users/{username}/social_accounts"
social_response = requests.get(social_url, headers=headers)

# Parse the response JSON into a Python list of dictionaries
social_accounts = social_response.json()

"""
# API endpoint to fetch the user's public events
Parameters `per_page` is used to specify the number of events to fetch per page.
The number of results per page (max 100). Default: 30

This parameter is used to overcome the default pagination limit of 30 events per page.
Because some users have a lot of starring, following, and other activities, so the commit events are not shown (not found) in the first page.
This causes the latest commit to not be found and the commit email to be empty.

For more information, see:
https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api?apiVersion=2022-11-28
https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28#list-public-events-for-a-user
"""
url = f"https://api.github.com/users/{username}/events/public?per_page=100"

# Fetch data from the API
response = requests.get(url)

"""
# Initialize variables to store the latest commit details

Some users have been inactive for a long time or there is no any activity.
To resolve this you can do the manual method with the .patch method.
Which manually checking the user account and the repository.

you can read my write-up about it here:
https://hiiruki.dev/writeups/sourcing-games/game2-05/
"""
# Initialize variable with a default value
latest_commit_head = None
commit_message = None
commit_url = None
commit_api = None
repo_name = None
repo_url = None
author_name = None
author_email = None
repo_commit_feed = None
repo_releases_feed = None
repo_tags_feed = None


# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse JSON response
    events = response.json()

    # Iterate through each event
    for event in events:
        # Check if the event type is "PushEvent"
        if event["type"] == "PushEvent":
            # Get the latest commit's details
            latest_commit_head = event["payload"]["head"]
            latest_commit = event["payload"]["commits"][0]
            
            # Extract commit message and URL
            commit_message = latest_commit["message"]
            commit_api = latest_commit["url"]

            # Extract commit author's email and name
            author_email = latest_commit["author"]["email"]
            author_name = latest_commit["author"]["name"]

            # Construct commit URL
            commit_sha = commit_api.split("/").pop()
            commit_url = f"https://github.com/{event['repo']['name']}/commit/{commit_sha}"

            # Extract repository name from the URL
            repo_name = commit_api.split("/repos/")[-1].split("/commits/")[0]
            
            # Construct repository URL
            repo_url = f"https://github.com/{repo_name}"

            # Construct Feed URL
            repo_commit_feed = f"https://github.com/{username}/{repo_name}/commits.atom"
            repo_releases_feed = f"https://github.com/{username}/{repo_name}/releases.atom"
            repo_tags_feed = f"https://github.com/{username}/{repo_name}/tags.atom"
            
            # Break the loop as we found the latest PushEvent
            break
else:
    # Print error message if request was not successful
    print("Failed to fetch data from the API:", response.status_code)

# Print the user information
prGreen("\n============ Basic Information ============\n")
print("Username         :", user_info["login"])
print("Name             :", user_info["name"])
print("ID               :", user_info["id"])
print("Node ID          :", user_info["node_id"])
print("Avatar URL 1     :", user_info["avatar_url"])
print("Avatar URL 2     :", f"https://github.com/{username}.png") # same as avatar_url but with .png extension
print("Location         :", user_info["location"])
print("Bio              :", user_info["bio"])
print("Company          :", user_info["company"])
print("Hireable         :", user_info["hireable"])
print("Organizations    :", user_info["organizations_url"])
print("Followers        :", user_info["followers"])
print("Following        :", user_info["following"])
print("Type             :", user_info["type"])
print("Created          :", user_info["created_at"])
print("Updated          :", user_info["updated_at"])

"""
# Print the user's social accounts

idk how many social accounts can be shown on the profile (with icons)
because there is no official documentation about it, but there are 10 social providers I found
- twitter
- facebook
- instagram
- linkedin
- mastodon
- reddit
- twitch
- youtube
- hometown
- generic (for other social accounts or can be used for personal website)
"""

prGreen("\n================= Socials =================\n")
print("Email (Public)   :", user_info["email"])
# Check if author_email is still None
if author_email is None:
    print("Email (Commit)   : None (See note in bottom of this tools)")
else:
    # Print the user's email if available
    print("Email (Commit)   :", author_email)
    print("GitHub           :", user_info["html_url"])
print("Gravatar ID      :", user_info["gravatar_id"] if user_info["gravatar_id"] else None)
print("Blog             :", user_info["blog"] if user_info["blog"] else None)
print("GitHub Pages     :", f"https://{username}.github.io/")

"""
# Print other social accounts if available

References:
https://github.blog/changelog/2023-02-02-add-more-social-links-to-your-user-profile/
https://docs.github.com/en/rest/users/social-accounts?apiVersion=2022-11-28#list-social-accounts-for-a-user
https://github.com/orgs/community/discussions/57260
https://stackoverflow.com/questions/76031624/how-many-social-accounts-icons-can-be-shown-on-your-github-bio/76191105#76191105
"""
social_providers = ['twitter', 'facebook', 'instagram', 'linkedin', 'mastodon', 'reddit', 'twitch', 'youtube', 'hometown', 'generic']
for provider in social_providers:
    account = next((acc for acc in social_accounts if acc['provider'] == provider), None)
    if account:
        print(f"{provider.capitalize():<17}: {account['url']}")
    else:
        print(f"{provider.capitalize():<17}: None")

# Send the GET request to fetch social accounts

# social_url = f"https://api.github.com/users/{username}/social_accounts"
# social_response = requests.get(social_url, headers=headers)

# # Parse the social accounts response JSON into a Python list of dictionaries
# social_accounts = social_response.json()

# for account in social_accounts:
#     print(account["provider"].capitalize(), ":", account["url"])

# Print the user's credentials
prGreen("\n============= User Credentials =============\n")
print("Public PGP/GPG Key   :", f"https://github.com/{username}.gpg")
print("Public SSH Key       :", f"https://github.com/{username}.keys")

# Print the user's public repositories and gists
prGreen("\n============ Repos Information ============\n")
print("Public Repos :", user_info["public_repos"])
print("Public Gists :", user_info["public_gists"])
print("GitHub Gist  :", f"https://gist.github.com/{username}/")

prGreen("\n============== Latest Commit ==============\n")
if latest_commit_head is None:
    print("No latest commit found.\n")
else:
    print("Latest Commit Hash   :", latest_commit_head)
    print("Commit Message       :", commit_message)
    print("Commit URL           :", commit_url)
    
if commit_api is None:
    print("Commit API URL       : None (See note in bottom of this tools)")
else:
    print("Commit API URL       :", commit_api)

print("Repository Name      :", repo_name)
print("Repository URL       :", repo_url)
print("Latest Commit Patch  :", f"{commit_url}.patch" if {commit_url} else None)
print("Latest Commit Diff   :", f"{commit_url}.diff" if {commit_url} else None)
print("Author's Name        :", author_name)
print("Author's Email       :", author_email)
    

# Print the user's public events
prGreen("\n==========| User Feeds (RSS) |==========\n")
print("Public Activity      :", f"https://github.com/{username}.atom")
if repo_commit_feed is None:
    print("Repository Commits   : None (See note in bottom of this tools)")
else:
    # Print the user's repository feeds if available
    print("Repository Commits   :", repo_commit_feed)

if repo_releases_feed is None:
    print("Repository Releases  : None (See note in bottom of this tools)")
else:
    # Print the user's repository feeds if available
    print("Repository Releases  :", repo_releases_feed)

if repo_tags_feed is None:
    print("Repository Tags      : None (See note in bottom of this tools)")
else:
    # Print the user's repository feeds if available
    print("Repository Tags      :", repo_tags_feed)

# Print the GitHub API URLs
prGreen("\n========== GitHub API Information ==========\n")
print("API URL              :", user_info["url"])
print("API Gists            :", user_info["gists_url"])
print("API Repos            :", user_info["repos_url"])
if commit_api is None:
    print("Commit API           : None (See note in bottom of this tools)")
else:
    print("Commit API           :", commit_api)
print("API Followers        :", user_info["followers_url"])
print("API Following        :", user_info["following_url"])
print("API Starred          :", user_info["starred_url"])
print("API Subscriptions    :", user_info["subscriptions_url"])
print("API Organizations    :", user_info["organizations_url"])
print("API Received Events  :", user_info["received_events_url"])
print("API Events (Private) :", user_info["events_url"])
print("API Events (Public)  :", url)
print("\n")

# Check if any of the variables are None
if any(v is None for v in [latest_commit_head, commit_message, commit_url, commit_api, repo_name, repo_url, author_name, author_email]):
    prRed("==========! Important Notes !==========\n")
    print("NOTE: If the result is \"None\" or \"No latest commit found\" it is because there are no public events, it's typically due to users being inactive for a long time or there being no activity at all or there is so many non-commit events like starring, following, and other activities, so the commit events are not shown (not found) in the first page.\n\nTo resolve this, you can use the manual method with the .patch method, which involves adding \".patch\" to the end of the URL of the latest commit.\n")
