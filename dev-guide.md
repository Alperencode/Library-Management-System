# Git Branching Guide

To maintain a clean and structured development workflow, always create a new branch for each feature or bug fix.

## Creating and Working on a New Branch

1. **Pull the latest changes from `master`**  
   ```bash
   git checkout master
   git pull origin master
   ```

2. **Create and switch to a new branch** (follow the naming convention)  
   ```bash
   git checkout -b feat/register-endpoints
   ```

3. **Make changes and commit** (follow the commit message convention)  
   ```bash
   git add .
   git commit -m "feat: user registration operations"
   ```

4. **Push the branch to the remote repository**  
   ```bash
   git push -u origin feat/register-endpoints
   ```

## Switching Between Branches

- List available branches:  
  ```bash
  git branch  
  ```
- Switch to an existing branch:  
  ```bash
  git checkout feat/basic-database-operations  
  ```

## Naming Conventions

### Branch Naming  
Use the following conventions when creating branches:  
- **Features:** `feat/<feature-name>` (e.g., `feat/register-endpoints`)  
- **Bug Fixes:** `fix/<bug-description>` (e.g., `fix/login-bug`)  
- **Refactors:** `refactor/<code-structure>` (e.g., `refactor/database-schema`)  

### Commit Messages  
Use the following format for commit messages:  
```bash
feat: short description of the feature  
fix: short description of the fix  
refactor: short description of the refactor  
```
Examples:  
```bash
git commit -m "feat: implement user authentication"
git commit -m "fix: resolve login validation issue"
git commit -m "refactor: improve database query performance"
```