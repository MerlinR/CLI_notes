# Git cheatsheet


## Diffs
```
git diff master         # Shows diff compared to master and or branch
git diff                # Shows unstaged changes
git diff --staged       # Shows staged changes
git diff HEAD~2 HEAD    # Shows the changes between two commits
```

## View commits
```
git show 921a2ff        # Shows the given commit
git show HEAD           # Shows the last commit
git show HEAD~2         # Two steps before the last commit 
git show HEAD:file.js   # Shows the version of file.js stored in the last commit
```

## Unoding staged files
```
git restore --staged file.js # Copies the last version of file.js from repo to index
```

## Blame
```
git blame file.txt     # Shows the author of each line in file.txt
```

## Branches
```
git branch bugfix   # Creates a new branch called bugfix  
git checkout -b bugfix  # Creates and Switches to the bugfix branch
git branch -d bugfix      # Deletes the bugfix branch
git branch --merged    # Shows the merged branches 
```

### Delete remote branch
```
git push -d origin bugfix
```

## Stash
```
git stash push              # Creates a new stash
git stash push -m "name"    # Creates a new stash
git stash list              # Lists all the stashes 
git stash show 1            # shortcut for stash@{1}
git stash apply 1           # Applies the given stash to the working dir
git stash drop 1            # Deletes the given stash
git stash clear             # Deletes all the stashes
```

## Merge
```
git merge bugfix    # Merges the bugfix  branch into the current branch
git merge --no-ff bugfix # Creates a merge commit even if FF is possible
git merge --abort  # Aborts the merge 
```

## Remote branches
```
git remote                  # Shows remote repos
git remote add upstream url # Adds a new remote called upstream
git remote rm upstream      # Remotes upstream
```

## Undo, revert, rewrites
### Reset local changes
```
git reset --soft HEAD^  # Removes the last commit, keeps changed staged
git reset --mixed HEAD^ # Unstages the changes as well
git reset --hard HEAD^  # Discards local changes
```
### Revert commits
```
git revert 72856ea  # Reverts the given commit
git revert HEAD~3.. # Reverts the last three commits
```
### Alter last commit
```
git commit --amend
```

## Altering config
git config --global alias.lg “log --oneline"

