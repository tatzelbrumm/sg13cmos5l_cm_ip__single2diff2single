# Git Submodule Cheatsheet

## Mental model

```text
A superproject tracks a submodule COMMIT,
not the submodule's files and not merely its branch.
```

## Terminology

```text
superproject = repository containing the submodule
submodule    = separate Git repository embedded at a path
gitlink      = superproject entry recording the submodule commit
.gitmodules  = version-controlled path/URL configuration
```

## Six commands worth memorizing

```bash
git submodule add URL path

git clone --recurse-submodules URL

git submodule update --init --recursive

git submodule status --recursive

git diff --submodule

git push --recurse-submodules=check
```

## Commands

```bash
# ADD
git submodule add URL path

# CLONE PROJECT INCLUDING SUBMODULES
git clone --recurse-submodules URL

# INITIALIZE AFTER ORDINARY CLONE
git submodule update --init --recursive

# SHOW SUBMODULES
git submodule status
git submodule status --recursive

# RESTORE SUBMODULES TO COMMITS RECORDED BY SUPERPROJECT
git submodule update --recursive

# GET LATEST FROM CONFIGURED SUBMODULE BRANCH
git submodule update --remote path

# CONFIGURE BRANCH USED BY --remote
git submodule set-branch --branch main path

# CHANGE URL
git submodule set-url path URL

# RESYNC AFTER .gitmodules URL CHANGED
git submodule sync --recursive

# SEE SUBMODULE COMMIT DIFFERENCES
git diff --submodule

# RUN COMMAND IN EACH SUBMODULE
git submodule foreach 'git status'
git submodule foreach --recursive 'git status'

# DEINITIALIZE LOCALLY
git submodule deinit path

# REMOVE FROM PROJECT
git submodule deinit -f -- path
git rm path

# SAFER SUPERPROJECT PUSH
git push --recurse-submodules=check
```
