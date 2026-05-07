# GitHub Token Setup for Project Board Automation

## Problem
The current token in `/home/yug/Documents/devinciwatch/old/token.txt` lacks required scopes for GitHub Projects V2.

## Solution
1. Go to: https://github.com/settings/tokens
2. Click **Edit** on your token (or create new one)
3. Add these scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `project` (Full control of projects)
   - ✅ `read:project` (Read access to projects)
   - ✅ `write:org` (Read and write org data)
4. Generate/Save token
5. Update token file:
   ```bash
   echo "ghp_YOUR_NEW_TOKEN_HERE" > /home/yug/Documents/devinciwatch/old/token.txt
   ```

## Verify
```bash
TOKEN=$(cat /home/yug/Documents/devinciwatch/old/token.txt | tr -d '\n')
curl -s -I -H "Authorization: Bearer $TOKEN" https://api.github.com/user | grep X-OAuth-Scopes
```
Should show: `X-OAuth-Scopes: repo, project, read:project, write:org`

## Then Run
```bash
cd /home/yug/Documents/devinciwatch/new
python3 /tmp/create_scrum_board.py
```

## Manual Alternative
If token update is not possible, follow manual steps in `.github/PROJECT_SETUP.md`:
1. Go to https://github.com/yugmerabtene/PROJET-M2-CYBER-2026/projects
2. Create Project → Scrum Board
3. Add Epics, Story Points, Sprint fields
4. Add issues #1-5 to board
5. Configure fields for each issue
