#!/bin/bash
# Pull latest from GitHub
git pull origin main

# Upload to Databricks
python3 << 'EOF'
from databricks.sdk import WorkspaceClient
import pathlib

w = WorkspaceClient()
local_dir = pathlib.Path(".")
workspace_path = "/Workspace/Users/Keith.Dewar@brambles.com/sentinel"

for file_path in local_dir.glob("*"):
    if file_path.is_file() and not file_path.name.startswith("."):
        with open(file_path, "rb") as f:
            content = f.read()
        remote_path = f"{workspace_path}/{file_path.name}"
        w.workspace.upload(remote_path, content, overwrite=True)
        print(f"Uploaded {file_path.name}")

print("✅ Synced from GitHub to Databricks!")
EOF