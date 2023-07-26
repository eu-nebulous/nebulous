#!/usr/bin/env python3

import subprocess
from pathlib import Path
from urllib.parse import urljoin

import yaml

WORK_PATH = "/opt"
SELF_NAME = "nebulous/nebulous"
DEPLOY_JOB_NAME = "nebulous-platform-apply-helm-charts"
BASE_URL = "https://opendev.org/"
BRANCH = "master"

SELF_PATH = Path(WORK_PATH, SELF_NAME)

subprocess.run(
    [
        "git",
        "-C",
        SELF_PATH,
        "fetch",
    ]
)
subprocess.run(
    [
        "git",
        "-C",
        SELF_PATH,
        "checkout",
        BRANCH,
    ]
)
subprocess.run(
    [
        "git",
        "-C",
        SELF_PATH,
        "merge",
        "--ff-only",
    ]
)

with open(SELF_PATH / "zuul.d" / "jobs.yaml") as f:
    jobs = yaml.safe_load(f)
    deploy_job = next(
        job["job"] for job in jobs if job["job"]["name"] == DEPLOY_JOB_NAME
    )
    del jobs

# collect required projects
for project in deploy_job["required-projects"]:
    print(f"Collecting {project}")
    repo_url = urljoin(BASE_URL, project)
    repo_path = Path(WORK_PATH, project)
    if (repo_path / ".git").exists():
        subprocess.run(
            [
                "git",
                "-C",
                repo_path,
                "fetch",
            ]
        )
        subprocess.run(
            [
                "git",
                "-C",
                repo_path,
                "checkout",
                BRANCH,
            ]
        )
        subprocess.run(
            [
                "git",
                "-C",
                repo_path,
                "merge",
                "--ff-only",
            ]
        )
    else:
        subprocess.run(
            [
                "mkdir",
                "-p",
                repo_path,
            ]
        )
        subprocess.run(
            [
                "git",
                "-C",
                repo_path,
                "clone",
                "-b",
                BRANCH,
                repo_url,
                ".",
            ]
        )

# deploy collected charts
for project in deploy_job["required-projects"]:
    print(f"Deploying charts of {project}")
    charts_path = Path(WORK_PATH, project, "charts")
    for chart_path in charts_path.iterdir():
        print(f"Deploying chart {chart_path.name}")
        subprocess.run(
            [
                "helm",
                "uninstall",
                chart_path.name,
                "--wait",
            ]
        )
        subprocess.run(
            [
                "helm",
                "install",
                chart_path.name,
                chart_path,
            ]
        )
