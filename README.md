# git-mirror-init

This `git-mirror` script allows you to mirror a local git repository on both GitHub and GitLab, while retaining GitLab as the primary remote repository.

## Prerequisites

Before using the script, you will need to generate personal access tokens for both GitHub and GitLab.

On GitHub, go to Settings -> Developer settings -> Personal access tokens -> Tokens (classic). Click "Generate new token (classic)", give it a name, and select "public_repo" as its only scope.

On GitLab, select "Access tokens" on the left-hand side, then create a new token and select "write_repository" as its only scope.

## Usage

### 1. Create the config file.

Make a copy of `example-config.json` in the `git-mirror` directory and rename it to `config.json`. Enter your GitHub and GitLab access tokens into the file.

### 2. Run the script

Run the `git-mirror.py` script within the local git repository that you want to mirror, specifying the following options: 

`python git-mirror.py -n <repo-name> -a -u`

The `-n` option specifies the name of the repository that will be created on both GitHub and GitLab. 
The `-a` and `-u` options indicate that mirrors should be created on GitLab and GitHub, respectively.
The `-v` option can be used for verbose output, which will print out status displays of what the script is currently doing. 

Double-check the repo name before you execute the command because it's annoying to delete the repos once they're made.

### 3. Push your local repo

Once the configurations have been set, push your local changes to the remote repositories using the following command: 

`git push -u origin main`

Replace `main` with the name of your main branch.

## Options
- `-h`: Help, displays usage information.
- `-v`: Verbose, prints out status displays of what the script is currently doing.
- `-n`: Repo name, specifies the name to be used when creating the repositories on GitHub and GitLab.
- `-u`: GitHub mirror, creates a mirror on GitHub.
- `-a`: GitLab mirror, creates a mirror on GitLab.
- `-i`: Initializes a new repository in the current directory. If this option is not specified, the script modifies the current repository.

## Limitations

Note that `git-mirror` currently only supports mirroring on GitHub and GitLab, and the primary repository must be GitLab. In the future, the script may be extended to allow arbitrary remotes and primary repositories.
