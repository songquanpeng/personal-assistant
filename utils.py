import requests


def get_latest_version(repository="personal-assistant", username="songquanpeng"):
    try:
        data = requests.get(f"https://api.github.com/repos/{username}/{repository}/releases/latest").json()
    except:
        return None
    latest_version = data["tag_name"]
    return latest_version
