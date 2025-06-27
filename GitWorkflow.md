# Git Workflow - Command Guide

## 🔄 Basic Workflow (Creating Checkpoints)

### Quick Template - Copy and Paste <-----------
```
git add .
git commit -m "CHANGE_THIS_MESSAGE"
git push
```

### Step by Step Details
1. Check current status
```
git status
```

2. Add changes
```
git add .                    # All files
git add src/main.py         # Only a specific file
git add src/                # Only a folder
```

3. Create commit (checkpoint)
```
git commit -m "Change description"
```

4. Upload to GitHub
```
git push
```

## 📝 Commit Message Examples
```
git commit -m "Add sum function"
git commit -m "Fix division by zero bug"
git commit -m "Refactor input code"
git commit -m "Add input validation"
git commit -m "Improve user interface"
git commit -m "Document main functions"
```

## ⏮️ Going Back to Previous Checkpoints
View commit history
```
git log --oneline           # Short list view
git log                     # Detailed list view
```

Go back temporarily (for review)
```
git checkout COMMIT_HASH    # Example: git checkout a1b2c3d
git checkout main           # Return to latest commit
```

Go back permanently (CAREFUL!)
Option 1: Create new commit that undoes changes
```
git revert COMMIT_HASH
```

Option 2: Delete commits (DANGEROUS)
```
git reset --hard COMMIT_HASH
git push --force
```

## 🔍 VERIFICATION Commands <-----------
When opening VSCode (optional)
```
git status              # Current status
git log --oneline       # Recent commits
git branch             # Current branch
```

To see differences
```
git diff               # Unsaved changes
git diff --staged      # Changes in staging
git show              # Last commit
```

## 🌿 Working with Branches
Create new branch for experimentation
```
git branch new-feature      # Create branch
git checkout new-feature    # Switch to branch
```

Or do both at once:
```
git checkout -b new-feature
```

Switch between branches
```
git checkout main             # Go to main
git checkout new-feature    # Go to feature
```

Merge branch with main
```
git checkout main
git merge new-feature
git push
```

## 🆘 Emergency Commands
If you made a mistake before commit
```
git restore file.py      # Undo changes in a file
git restore .           # Undo all changes
```

If you made a mistake after add
```
git reset file.py       # Remove file from staging
git reset              # Remove all from staging
```

If you need to make changes to the last commit
```
git add .
git commit --amend -m "Corrected message"
```

## 📊 Additional Useful Commands
View ignored files
```
cat .gitignore
```

View current configuration
```
git config --list
```

View configured remotes
```
git remote -v
```

Verify connection with GitHub
```
git remote show origin
```

## 🎯 Recommended Project Workflow <-----------
1. Before programming: `git status` (check status)
2. While programming: Save frequently (Ctrl+S)
3. Each completed feature:
```
git add .
git commit -m "Clear description"
git push
```

At end of day: Always push pending commits

## ⚠️ Important Notes

- Always commit before big experiments
- Clear and descriptive commit messages
- Push regularly to avoid losing work
- Don't use `git reset --hard` unless you're 100% sure