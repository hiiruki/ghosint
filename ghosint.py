# Desc      : GHOSINT - An OSINT tool based on python to get GitHub user information.
# Author    : Hiiruki <hi@hiiruki.dev>
# URL       : https://github.com/hiiruki/ghosint

import requests

print("""

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
    "Authorization": "<YOUR_GITHUB_TOKEN>",
    "X-GitHub-Api-Version": "2022-11-28"
}

# Send the GET request to the GitHub API
url = f"https://api.github.com/users/{username}"
response = requests.get(url, headers=headers)

# Parse the response JSON into a Python dictionary
user_info = response.json()

# Print the user information
print("\n============= User Information =============\n")
print("Username         : ", user_info["login"])
print("Name             : ", user_info["name"])
print("ID               : ", user_info["id"])
print("Node ID          : ", user_info["node_id"])
print("Avatar           : ", user_info["avatar_url"])
print("Gravatar ID      : ", user_info["gravatar_id"])
print("Location         : ", user_info["location"])
print("Bio              : ", user_info["bio"])
print("Email            : ", user_info["email"])
print("Twitter          : ", user_info["twitter_username"])
print("GitHub           : ", user_info["html_url"])
print("Company          : ", user_info["company"])
print("Hireable         : ", user_info["hireable"])
print("Organizations    : ", user_info["organizations_url"])
print("Followers        : ", user_info["followers"])
print("Following        : ", user_info["following"])
print("Type             : ", user_info["type"])
print("Created          : ", user_info["created_at"])
print("Updated          : ", user_info["updated_at"])

print("\n============= Repo Information =============\n")
print("Public Repos : ", user_info["public_repos"])
print("Public Gists : ", user_info["public_gists"])
print("GitHub Gist  : ", f"https://gist.github.com/{username}/\n")
