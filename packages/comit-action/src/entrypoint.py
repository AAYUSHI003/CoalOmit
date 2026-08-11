# Copyright 2026 CoalOmIT Authors.
# Licensed under the Apache License, Version 2.0.

import os
import subprocess
import sys
import requests


def main():
    model_path = os.getenv("INPUT_MODEL_PATH", "")
    methods = os.getenv("INPUT_METHODS", "int8,int4")
    region = os.getenv("INPUT_REGION", "GLOBAL")
    traffic = os.getenv("INPUT_TRAFFIC", "1000000")
    token = os.getenv("GITHUB_TOKEN", "")

    if not model_path:
        print("Error: INPUT_MODEL_PATH is required.")
        sys.exit(1)

    cmd = [
        "comit", "run", model_path,
        "--methods", methods,
        "--region", region,
        "--traffic", traffic,
        "--format", "markdown"
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"COMIT Error:\n{res.stderr}")
        sys.exit(res.returncode)

    markdown_output = res.stdout
    print(markdown_output)

    # Post as PR comment if running inside GitHub Actions PR context
    event_path = os.getenv("GITHUB_EVENT_PATH", "")
    repository = os.getenv("GITHUB_REPOSITORY", "")
    if token and event_path and repository and os.path.exists(event_path):
        try:
            import json
            with open(event_path, "r", encoding="utf-8") as f:
                event = json.load(f)
            pr_num = event.get("pull_request", {}).get("number")
            if pr_num:
                url = f"https://api.github.com/repos/{repository}/issues/{pr_num}/comments"
                headers = {
                    "Authorization": f"token {token}",
                    "Accept": "application/vnd.github.v3+json"
                }
                body = {
                    "body": f"🌱 **Carbon-Aware Compression (COMIT) Report**\n\n{markdown_output}"
                }
                requests.post(url, headers=headers, json=body)
                print("Posted report to Pull Request comments.")
        except Exception as e:
            print(f"Notice: Could not post PR comment: {e}")


if __name__ == "__main__":
    main()
