### git reset
```
git checkout --orphan temp_branch
git rm -r --cached .
git add -A
git commit -m "Initial commit"
git branch -D main
git branch -m main
git push -f origin main
```

### client fetch new reset
```
git fetch --all
git reset --hard origin/main
```
