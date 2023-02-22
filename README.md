# git-mirror-init

This script will initialize a new git repo, then creates empty repositories on
github and gitlab using the given name, then sets both as the push destination.

## Usage

Create a `config.json` file in the same folder as `git-mirror-init.sh` with the
following format:

``` json
{
    "tokens": {
        "github": "YOUR_GITHUB_API_TOKEN",
        "gitlab": "YOUR_GITLAB_API_TOKEN"
    }
}
```

After that you can use the script:

`python git-mirror -n test -u -a`

This will create a repo on github and gitlab named "test" and sets up push and
pull configuration so that gitlab is the primary. You can also use the -v verbose
option to see what the script is doing.

## Options

-h: Help, display the usage
-v: Verbose, print out status displays of what the script is currently doing.
-n: Repo name, this is the name to be used when creating the repos on github & gitlab
-u: GitHub mirror, create a mirror on github
-a: GitLab mirror, create a mirror on gitlab
-i: Initialize a new repo in the current directory, otherwise the script modifies the current repo
