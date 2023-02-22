import json
import subprocess
import requests
import getopt
import sys
import os

def usage():
    print("Usage: python gitmirror.py -n <repo_name> [-u] [-a] [-i] [-h]\n",
        "-h: Help, display this usage menu\n",
        "-v: Verbose, print out status displays of what the script is currently doing\n",
        "-n: Repo name, this is the name to be used when creating the repos on github & gitlab\n",
        "-u: GitHub mirror, create a mirror on github\n",
        "-a: GitLab mirror, create a mirror on gitlab\n",
        "-i: Initialize a new repo in the current directory, otherwise the script modifies the current repo\n")

def create_github_repo(repo, token):
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {token}"}
    payload = {"name": repo}
    response = requests.post(url, headers=headers, json=payload).json()
    return response.get("ssh_url", None)

def create_gitlab_repo(repo, token):
    url = "https://gitlab.com/api/v4/projects"
    headers = {"Content-Type": "application/json"}
    params = {"private_token": token}
    payload = {"name": repo}
    response = requests.post(url, headers=headers, params=params, json=payload).json()
    return response.get("ssh_url_to_repo", None)

def main(argv):
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Load the config data from the config.json file
    config_file = os.path.join(script_dir, "config.json")
    with open(config_file) as f:
        config_data = json.load(f)

    github_token = config_data["tokens"]["github"]
    gitlab_token = config_data["tokens"]["gitlab"]
    repo = ""
    urls = {}
    verbose = False

    optstring = "hn:iuav"
    try:
        opts, _ = getopt.getopt(sys.argv[1:], optstring)
    except getopt.GetoptError as err:
        print("Failed to parse args: " + str(err))
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-n":
            repo = arg
        elif opt == "-h":
            usage()
            sys.exit()
        elif opt == "-u":
            if not repo:
                print("Need repo name")
                sys.exit(1)
            url = create_github_repo(repo, github_token)
            if not url or url == "null":
                print("Could not create github repo")
                sys.exit(1)
            else:
                urls["github"] = url
                if verbose:
                    print(f"Created GitHub repository {repo} at {url}")
        elif opt == "-a":
            if not repo:
                print("Need repo name")
                sys.exit(1)
            url = create_gitlab_repo(repo, gitlab_token)
            if not url or url == "null":
                print("Could not create gitlab repo")
                sys.exit(1)
            else:
                urls["gitlab"] = url
                if verbose:
                    print(f"Created GitLab repository {repo} at {url}")
        elif opt == "-i":
            subprocess.run(["git", "init"])
            if verbose:
                print("Initialized Git repository")
        elif opt == "-v" or opt == "--verbose":
            verbose = True
        else:
            print(f"Invalid option: {opt}")
            sys.exit(1)

    if "gitlab" in urls:
        url_gl = urls["gitlab"]
        subprocess.run(["git", "remote", "add", "origin", url_gl])
        subprocess.run(["git", "remote", "set-url", "--add", "--push", "origin", url_gl])
        if verbose:
            print(f"Added GitLab remote URL {url_gl} to Git repository and set it as main mirror")
    if "github" in urls:
        url_gh = urls["github"]
        subprocess.run(["git", "remote", "set-url", "--add", "--push", "origin", url_gh])
        if verbose:
            print(f"Added GitHub remote URL {url_gh} to Git repository")

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
