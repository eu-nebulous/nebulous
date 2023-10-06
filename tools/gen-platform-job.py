#!/usr/bin/env python3

import yaml


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


with open("data/repos.yaml") as f:
    repos = yaml.safe_load(f)

repo_deps = []
requires = []
helm_charts = {}

for repo in repos:
    repo_base, repo_name = repo.split("/")
    repo_dashed = f"{repo_base}-{repo_name}"
    repo_deps.append(
        {
            "name": f"{repo_dashed}-build-container-images",
            "soft": True,
        }
    )
    repo_deps.append(
        {
            "name": f"{repo_dashed}-upload-container-images",
            "soft": True,
        }
    )
    requires.append(f"{repo_dashed}-container-images")
    helm_charts[repo_dashed] = f"../{repo_name}/charts/{repo_dashed}"

job = {
    "name": "nebulous-platform-apply-helm-charts",
    "parent": "nebulous-apply-helm-charts",
    "dependencies": [
        {"name": "opendev-buildset-registry", "soft": False},
        *repo_deps,
    ],
    "required-projects": repos,
    "requires": requires,
    "description": "Deploy a Kubernetes cluster and apply charts.",
    "vars": {"helm_charts": helm_charts},
}
jobs = [{"job": job}]

with open("zuul.d/jobs.yaml", "w") as f:
    yaml.dump(jobs, f, sort_keys=False, Dumper=IndentDumper)
