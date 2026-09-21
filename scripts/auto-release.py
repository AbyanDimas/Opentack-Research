#!/usr/bin/env python3
"""
Direct Automated Semantic Release for OpenStack Research Documentation.
Bumps semantic version, updates CHANGELOG.md, creates git tag, and publishes GitHub Release
directly on push without requiring a separate Release Pull Request.
"""
import os
import re
import subprocess
import sys
from datetime import datetime

def run_cmd(cmd, check=True):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed ({res.returncode}): {cmd}\n{res.stderr.strip()}")
    return res.stdout.strip()

def get_latest_tag():
    run_cmd("git fetch --tags", check=False)
    output = run_cmd("git tag --sort=-v:refname", check=False)
    for line in output.splitlines():
        tag = line.strip()
        if re.match(r"^v?\d+\.\d+\.\d+$", tag):
            return tag
    return "v1.0.0"

def parse_semver(tag_str):
    m = re.match(r"^v?(\d+)\.(\d+)\.(\d+)$", tag_str)
    if not m:
        return 1, 0, 0
    return int(m.group(1)), int(m.group(2)), int(m.group(3))

def main():
    repo = os.environ.get("GITHUB_REPOSITORY", "AbyanDimas/Opentack-Research")
    latest_tag = get_latest_tag()
    print(f"Current latest tag: {latest_tag}")

    # Fetch commits since latest tag
    log_cmd = f"git log {latest_tag}..HEAD --pretty=format:'%H|%s'"
    log_output = run_cmd(log_cmd, check=False)

    if not log_output:
        print("No commits found since latest tag. Nothing to release.")
        sys.exit(0)

    features = []
    fixes = []
    docs = []
    others = []
    has_breaking = False
    has_feature = False

    for line in log_output.splitlines():
        if not line or "|" not in line:
            continue
        sha, msg = line.split("|", 1)
        short_sha = sha[:7]
        commit_url = f"https://github.com/{repo}/commit/{sha}"
        formatted_entry = f"{msg} ([{short_sha}]({commit_url}))"

        # Skip release commits and skip-ci commits
        if re.match(r"^chore\((?:release|pages)\):", msg) or "[skip ci]" in msg:
            continue

        if "BREAKING CHANGE" in msg or re.search(r"^[a-z]+!:", msg):
            has_breaking = True
            features.append(formatted_entry)
        elif msg.startswith(("feat:", "feat(")):
            has_feature = True
            features.append(formatted_entry)
        elif msg.startswith(("fix:", "fix(")):
            fixes.append(formatted_entry)
        elif msg.startswith(("docs:", "docs(")):
            docs.append(formatted_entry)
        elif msg.startswith(("refactor:", "perf:", "style:", "ci:", "chore:")):
            others.append(formatted_entry)
        else:
            others.append(formatted_entry)

    total_changes = len(features) + len(fixes) + len(docs) + len(others)
    if total_changes == 0:
        print("Only release or skip-ci commits found since latest tag. Skipping release.")
        sys.exit(0)

    # Bump version
    major, minor, patch = parse_semver(latest_tag)
    if has_breaking:
        major += 1
        minor = 0
        patch = 0
    elif has_feature:
        minor += 1
        patch = 0
    else:
        patch += 1

    new_version = f"{major}.{minor}.{patch}"
    new_tag = f"v{new_version}"
    today = datetime.utcnow().strftime("%Y-%m-%d")

    print(f"Bumping version to: {new_tag} ({today})")

    # Generate release notes
    notes_lines = [f"## [{new_version}](https://github.com/{repo}/compare/{latest_tag}...{new_tag}) ({today})\n"]

    if features:
        notes_lines.append("### Features")
        for f in features:
            notes_lines.append(f"- {f}")
        notes_lines.append("")

    if fixes:
        notes_lines.append("### Bug Fixes")
        for fix in fixes:
            notes_lines.append(f"- {fix}")
        notes_lines.append("")

    if docs:
        notes_lines.append("### Documentation")
        for d in docs:
            notes_lines.append(f"- {d}")
        notes_lines.append("")

    if others:
        notes_lines.append("### Maintenance & Improvements")
        for o in others:
            notes_lines.append(f"- {o}")
        notes_lines.append("")

    release_body = "\n".join(notes_lines).strip()

    # Update CHANGELOG.md
    changelog_path = "CHANGELOG.md"
    existing_changelog = ""
    if os.path.exists(changelog_path):
        with open(changelog_path, "r", encoding="utf-8") as cf:
            existing_changelog = cf.read()

    header = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n"
    if existing_changelog.startswith("# Changelog"):
        body_without_header = re.sub(r"^# Changelog\s*(?:All notable changes[^\n]*\n+)?", "", existing_changelog).strip()
        updated_changelog = f"{header}{release_body}\n\n{body_without_header}\n"
    else:
        updated_changelog = f"{header}{release_body}\n\n{existing_changelog}".strip() + "\n"

    with open(changelog_path, "w", encoding="utf-8") as cf:
        cf.write(updated_changelog)

    print("Updated CHANGELOG.md successfully.")

    # Configure git author
    run_cmd('git config user.name "github-actions[bot]"')
    run_cmd('git config user.email "41898282+github-actions[bot]@users.noreply.github.com"')

    # Commit CHANGELOG.md and create Git tag
    run_cmd(f'git commit -am "chore(release): {new_tag} [skip ci]"', check=False)
    run_cmd(f'git tag -a "{new_tag}" -m "Release {new_tag}"')

    # Push commit and tag to origin
    print(f"Pushing commit and {new_tag} to origin pages...")
    run_cmd(f'git push origin pages "{new_tag}"')

    # Create GitHub Release
    print(f"Creating GitHub Release {new_tag}...")
    temp_notes_file = ".temp_release_notes.md"
    with open(temp_notes_file, "w", encoding="utf-8") as f:
        f.write(release_body)

    try:
        run_cmd(f'gh release create "{new_tag}" --title "{new_tag}" --notes-file "{temp_notes_file}"')
        print(f"✅ Successfully published GitHub Release {new_tag}!")
    finally:
        if os.path.exists(temp_notes_file):
            os.remove(temp_notes_file)

    # Set GitHub Actions output if available
    gh_output = os.environ.get("GITHUB_OUTPUT")
    if gh_output and os.path.exists(gh_output):
        with open(gh_output, "a", encoding="utf-8") as gh_out:
            gh_out.write(f"release_created=true\n")
            gh_out.write(f"tag_name={new_tag}\n")

if __name__ == "__main__":
    main()
