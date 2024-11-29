#!/bin/bash

# Navigate to the specific directory
cd ~/Vault/asi0-Github-repos/sovereign-university-data-paid/ || exit

# Checkout the main branch
git checkout main
git pull

# Rebase the main branch with dev branch
REBASE_OUTPUT=$(git rebase dev)

# Check if the rebase output contains "Fast-forwarded"
if echo "$REBASE_OUTPUT" | grep -q "Fast-forwarded"; then
  echo "Changes have been rebased into the main branch."
else
  echo "No changes were rebased."
fi

# Push the changes to the remote repository
git push

# Syncing the website
echo "Syncing website in progress ..."
curl -X POST https://api.testnet.planb.network/github/sync
curl -X POST https://api.planb.network/github/sync

# Checkout the dev branch
git checkout dev

