# Here's a good explanation on how to fix detached HEAD for submodules.
# https://stackoverflow.com/questions/18770545
# https://gist.github.com/mjsteinbaugh/980d2a8147abaede00507c9cf013295d#file-git-submodule-detached-head-fix-sh-L1

git branch
git checkout master
git submodule add -b <branch> <repository> [<submodule-path>]

git branch --set-upstream-to=origin/master master
# git branch -u origin/master master

git submodule update --remote
