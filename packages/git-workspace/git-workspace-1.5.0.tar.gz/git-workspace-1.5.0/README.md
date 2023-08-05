# Git Workspace

This script is intended to ease the development in multirepo environment. By defining a workspace file
that contains all the repositories one can easily share the environment setup without the need for manual
git clones. With git configuration user and host can also be set for the repositories. This allows one
to use e.g. multiple bitbucket repositories with different SSH keys easily without altering the host in
each git clone command.

This script also provides a command to check the overall state of the workspace (branches, untracked files etc.).
Few commands are overridden, but most are plain passthroughs to git and are run in all of the workspace
repositories.

```
Installation:

  - pip install git-workspace

Usage:

git ws <cmd> [arg]

positional arguments:
  {init,clone,state,help,command,graphops,go}
    init                Create a new (empty) workspace definition to the
                        current directory
    clone               Clone the repositories defined in the $WORKSPACE_FILE
                        file
    state               Display workspace state
    help                Display this help and exit
    command             The command can also be any CLI command such as 'ls
                        -la' or 'echo'.It will be run under each workspace
                        directory.
    graphops (go)       Graphops commands


optional arguments:
  -h, --help            show this help message and exit
```
```
usage: git-ws command [-h] ...

positional arguments:
  clicommand  CLI command as if run in the directory

optional arguments:
  -h, --help  show this help message and exit
```
```
usage: git-ws graphops [-h]
                       {simulate,execute,visualize,visualize-and-save} ...

positional arguments:
  {simulate,execute,visualize,visualize-and-save}
    simulate            Run simulation of the operation pipeline
    execute             Run the operation pipeline
    visualize           Visualize the pipelines as directed graphs
    visualize-and-save  Visualize the pipelines as directed graphs and save

optional arguments:
  -h, --help            show this help message and exit
```
```
Configuration:

  Configuration is currently in two parts. One is shareable workspace file and the other one will be user specific
  configuration containing git host and user. This is to allow for example multiple bitbucket accounts and ssh keys.
  Downside is that in the first version of this script, the user and host must be the same for all repositories.
  This is something to be looked into.

  $WORKSPACE_FILE:
    - One line, one repository
    - <path>/<repository>.git
    - e.g.
      MyGithubAccount/exmplarepository.git
      MyFriendsGithubAccount/collaborativerepository.git

  $WORKSPACE_GIT_CONFIGURATION:
    - Git user
    - Git host
    - e.g.
      GITUSER=git
      GITHOST=github.com
      
  .git-ws.graphops example:
    {
      "deploy": {
        "script": "foobar3.sh",
        "requires": ["a", "b"],
        "environment": {
          "somekey": "somevalue"
        }
      }
    }

https://github.com/XC-/git-workspace
Licensed under MIT license
```