#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime as dt
import json
import os
import re
import sys
from typing import Dict, List, Any

import requests

MARKER_START = r"<!-- REPO_LIST:START -->"
MARKER_END = r"<!-- REPO_LIST:END -->"

def gh_session():
    s = requests.Session()
    s.headers.update({
        "Accept": "application/vnd.github+json",
        "User-Agent": "repo-list-updater"
    })
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        s.headers["Authorization"] = f"Bearer {token}"
    return s

def fetch_repos_org(session: requests.Session, org: str) -> List[Dict[str, Any]]:
    all_repos = []
    page = 1
    while page <= 5:
        url = f"https://api.github.com/orgs/{org}/repos"
        params = {"per_page": 100, "page": page, "type": "public", "sort": "updated"}
        r = session.get(url, params=params, timeout=30)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        all_repos.extend(batch)
        page += 1
    return all_repos

def fetch_repos_user(session: requests.Session, user: str) -> List[Dict[str, Any]]:
    all_repos = []
    page = 1
    while page <= 5:
        url = f"https://api.github.com/users/{user}/repos"
        params = {"per_page": 100, "page": page, "type": "public", "sort": "updated"}
        r = session.get(url, params=params, timeout=30)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        all_repos.extend(batch)
        page += 1
    return all_repos

def human_dt(s: str) -> str:
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).date().isoformat()
    except Exception:
        return s or ""

def sort_repos(repos: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
    if key == "stars":
        return sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)
    if key == "updated":
        return sorted(repos, key=lambda r: r.get("updated_at", ""), reverse=True)
    return repos

def dedup(repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for r in repos:
        k = r.get("full_name") or f"{r.get('owner',{}).get('login','')}/{r.get('name','')}"
        if k not in seen:
            seen.add(k)
            out.append(r)
    return out

def build_table_block(title: str, repos: List[Dict[str, Any]]) -> str:
    lines = []
    lines.append(f"## {title}")
    lines.append("")
    lines.append("| 项目名 | 描述 | 语言 | ⭐ Stars | 最近更新 |")
    lines.append("| :-- | :-- | :-- | --: | :-- |")
    for r in repos:
        name = r.get("name", "(unknown)")
        url = r.get("html_url", "")
        desc = r.get("description") or "（暂无简介）"
        lang = r.get("language") or "N/A"
        stars = r.get("stargazers_count", 0)
        updated = human_dt(r.get("updated_at", ""))
        lines.append(f"| [{name}]({url}) | {desc} | {lang} | {stars} | {updated} |")
    lines.append("")
    return "\n".join(lines)

def build_markdown_section(orgs: List[str], users: List[str], grouped: bool, sort_key: str,
                           limit: int, session: requests.Session) -> str:
    blocks = []
    if grouped:
        # 每个组织/用户独立一组
        for org in orgs:
            repos = fetch_repos_org(session, org)
            repos = sort_repos(repos, sort_key)[:limit]
            blocks.append(build_table_block(f"🚀 当前开源作品展示（{org}）", repos))
        for user in users:
            repos = fetch_repos_user(session, user)
            repos = sort_repos(repos, sort_key)[:limit]
            blocks.append(build_table_block(f"🚀 当前开源作品展示（{user}）", repos))
        return "\n".join(blocks).strip() + "\n"
    else:
        # 合并为一组
        all_repos: List[Dict[str, Any]] = []
        for org in orgs:
            all_repos.extend(fetch_repos_org(session, org))
        for user in users:
            all_repos.extend(fetch_repos_user(session, user))
        all_repos = dedup(all_repos)
        all_repos = sort_repos(all_repos, sort_key)[:limit]
        header = "# 🚀 当前开源作品展示"
        table = build_table_block(header, all_repos)
        return table

def replace_in_readme(readme_path: str, new_block: str) -> bool:
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(rf"({MARKER_START}\s*)(.*?)(\s*{MARKER_END})", re.DOTALL)
    if not pattern.search(content):
        content_new = content.rstrip() + "\n\n" + f"{MARKER_START}\n{new_block}{MARKER_END}\n"
    else:
        content_new = pattern.sub(rf"\1{new_block}\3", content)

    if content_new != content:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content_new)
        return True
    return False

def load_config(path: str):
    if not path:
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Generate repo list section from multiple orgs/users.")
    parser.add_argument("--config", help="JSON 配置文件路径（包含 orgs/users/limit/sort/group_by）")
    parser.add_argument("--org", action="append", default=[], help="追加一个组织，可多次传")
    parser.add_argument("--user", action="append", default=[], help="追加一个用户，可多次传")
    parser.add_argument("--limit", type=int, default=None, help="展示数量")
    parser.add_argument("--sort", choices=["stars", "updated"], default=None, help="排序方式")
    parser.add_argument("--group-by", action="store_true", help="按组织/用户分组展示")
    parser.add_argument("--flat", action="store_true", help="忽略分组，扁平展示")
    parser.add_argument("--readme", default="README.md", help="README 路径")
    args = parser.parse_args()

    cfg = load_config(args.config) if args.config else {}
    orgs = (cfg.get("orgs") or []) + args.org
    users = (cfg.get("users") or []) + args.user
    limit = args.limit if args.limit is not None else cfg.get("limit", 8)
    sort_key = args.sort or cfg.get("sort", "stars")
    grouped = cfg.get("group_by", True)
    if args.group_by:
        grouped = True
    if args.flat:
        grouped = False

    if not orgs and not users:
        print("[ERROR] 未指定任何组织或用户（orgs/users）。", file=sys.stderr)
        sys.exit(2)

    session = gh_session()
    section_md = build_markdown_section(orgs, users, grouped, sort_key, limit, session)

    changed = replace_in_readme(args.readme, section_md)
    print("[INFO] README 已更新 ✅" if changed else "[INFO] 无变化，README 未改动。")

if __name__ == "__main__":
    main()
