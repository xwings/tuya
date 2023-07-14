### git reset
```
git checkout --orphan tmp-master # create a temporary branch
git add -A  # Add all files and commit them
git commit -m 'Add files'
git branch -D master # Deletes the master branch
git branch -m master # Rename the current branch to master
git push -f origin master # Force push master branch to Git server
```

### other client fetch new reset
```
git fetch --all
git reset --hard origin/master
```
