#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime as dt
import json
import os
import re
import sys
from typing import Dict, List, Any
from pathlib import Path

import requests

MARKER_START = r"<!-- REPO_LIST:START -->"
MARKER_END = r"<!-- REPO_LIST:END -->"

def GHSession():
    S = requests.Session()
    S.headers.update({"Accept": "application/vnd.github+json", "User-Agent": "repo-list-updater"})
    Token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if Token:
        S.headers["Authorization"] = f"Bearer {Token}"
    return S

def FetchRepos(Session: requests.Session, URL: str) -> List[Dict[str, Any]]:
    # 分页获取仓库，最多5页
    AllRepos = []
    for Page in range(1, 6):
        Params = {"per_page": 100, "page": Page, "type": "public", "sort": "updated"}
        R = Session.get(URL, params=Params, timeout=30)
        R.raise_for_status()
        Batch = R.json()
        if not Batch:
            break
        AllRepos.extend(Batch)
    return AllRepos

def FetchReposOrg(Session: requests.Session, Org: str) -> List[Dict[str, Any]]:
    return FetchRepos(Session, f"https://api.github.com/orgs/{Org}/repos")

def FetchReposUser(Session: requests.Session, User: str) -> List[Dict[str, Any]]:
    return FetchRepos(Session, f"https://api.github.com/users/{User}/repos")

def HumanDT(S: str) -> str:
    try:
        return dt.datetime.fromisoformat(S.replace("Z", "+00:00")).date().isoformat()
    except Exception:
        return S or ""

def SortRepos(Repos: List[Dict[str, Any]], Key: str) -> List[Dict[str, Any]]:
    # 次级排序：星数相同按更新时间，更新时间相同按星数
    if Key == "stars":
        return sorted(Repos, key=lambda R: (R.get("stargazers_count", 0), R.get("updated_at", "")), reverse=True)
    if Key == "updated":
        return sorted(Repos, key=lambda R: (R.get("updated_at", ""), R.get("stargazers_count", 0)), reverse=True)
    return Repos

def Dedup(Repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    Seen = set()
    Out = []
    for R in Repos:
        K = R.get("full_name") or f"{R.get('owner',{}).get('login','')}/{R.get('name','')}"
        if K not in Seen:
            Seen.add(K)
            Out.append(R)
    return Out

def FilterRepos(Repos: List[Dict[str, Any]], Excludes: List[str]) -> List[Dict[str, Any]]:
    if not Excludes:
        return Repos
    ExcludeSet = set(Excludes)
    return [R for R in Repos if R.get("name") not in ExcludeSet]

def EscapeTableCell(Text: str) -> str:
    # 转义 Markdown 表格特殊字符
    return Text.replace("|", "\\|").replace("\n", " ").replace("\r", "")

def BuildTableBlock(Title: str, Repos: List[Dict[str, Any]]) -> str:
    Lines = [
        "| 项目名 | 描述 | 语言 | ⭐ Stars | 最近更新 |",
        "| :-- | :-- | :-- | --: | :-- |"
    ]
    for R in Repos:
        Name = R.get("name", "(unknown)")
        URL = R.get("html_url", "")
        Desc = EscapeTableCell(R.get("description") or "（暂无简介）")
        Lang = R.get("language") or "N/A"
        Stars = R.get("stargazers_count", 0)
        Updated = HumanDT(R.get("updated_at", ""))
        Lines.append(f"| [{Name}]({URL}) | {Desc} | {Lang} | {Stars} | {Updated} |")
    Lines.append("")
    return "\n".join(Lines)

def BuildMarkdownSection(Orgs: Dict[str, List[str]], Users: Dict[str, List[str]], Grouped: bool,
                         SortKey: str, Limit: int, Session: requests.Session) -> str:
    Blocks = []
    if Grouped:
        for Org, Excludes in Orgs.items():
            Repos = SortRepos(FilterRepos(FetchReposOrg(Session, Org), Excludes), SortKey)[:Limit]
            Blocks.append(BuildTableBlock(f"🚀 当前开源作品展示（{Org}）", Repos))
        for User, Excludes in Users.items():
            Repos = SortRepos(FilterRepos(FetchReposUser(Session, User), Excludes), SortKey)[:Limit]
            Blocks.append(BuildTableBlock(f"🚀 当前开源作品展示（{User}）", Repos))
        return "\n".join(Blocks).strip() + "\n"
    else:
        AllRepos: List[Dict[str, Any]] = []
        for Org, Excludes in Orgs.items():
            AllRepos.extend(FilterRepos(FetchReposOrg(Session, Org), Excludes))
        for User, Excludes in Users.items():
            AllRepos.extend(FilterRepos(FetchReposUser(Session, User), Excludes))
        AllRepos = SortRepos(Dedup(AllRepos), SortKey)[:Limit]
        return BuildTableBlock("# 🚀 当前开源作品展示", AllRepos)

def ReplaceInReadme(ReadmePath: str, NewBlock: str) -> bool:
    FilePath = Path(ReadmePath)
    Content = FilePath.read_text(encoding="utf-8")
    Pattern = re.compile(rf"({MARKER_START})\s*(.*?)\s*({MARKER_END})", re.DOTALL)
    if not Pattern.search(Content):
        NewContent = Content.rstrip() + "\n\n" + f"{MARKER_START}\n{NewBlock}{MARKER_END}\n"
    else:
        NewContent = Pattern.sub(rf"\1\n{NewBlock}\3", Content)
    if NewContent != Content:
        FilePath.write_text(NewContent, encoding="utf-8")
        return True
    return False

def LoadConfig(ConfigPath: str):
    if not ConfigPath:
        return None
    return json.loads(Path(ConfigPath).read_text(encoding="utf-8"))

def Main():
    Parser = argparse.ArgumentParser(description="Generate repo list section from multiple orgs/users.")
    Parser.add_argument("--config", help="JSON 配置文件路径")
    Parser.add_argument("--org", action="append", default=[], help="追加组织")
    Parser.add_argument("--user", action="append", default=[], help="追加用户")
    Parser.add_argument("--limit", type=int, default=None, help="展示数量")
    Parser.add_argument("--sort", choices=["stars", "updated"], default=None, help="排序方式")
    Parser.add_argument("--group-by", action="store_true", help="按组织/用户分组展示")
    Parser.add_argument("--flat", action="store_true", help="扁平展示")
    Parser.add_argument("--readme", default="README.md", help="README 路径")
    Args = Parser.parse_args()

    Cfg = LoadConfig(Args.config) if Args.config else {}

    # 支持新格式 dict 和旧格式 list
    CfgOrgs = Cfg.get("orgs") or {}
    CfgUsers = Cfg.get("users") or {}
    if isinstance(CfgOrgs, list):
        CfgOrgs = {O: [] for O in CfgOrgs}
    if isinstance(CfgUsers, list):
        CfgUsers = {U: [] for U in CfgUsers}

    # 命令行追加的 org/user 默认无黑名单
    for O in Args.org:
        if O not in CfgOrgs:
            CfgOrgs[O] = []
    for U in Args.user:
        if U not in CfgUsers:
            CfgUsers[U] = []

    Orgs, Users = CfgOrgs, CfgUsers
    Limit = Args.limit if Args.limit is not None else Cfg.get("limit", 8)
    SortKey = Args.sort or Cfg.get("sort", "stars")
    Grouped = Cfg.get("group_by", True)
    if Args.group_by:
        Grouped = True
    if Args.flat:
        Grouped = False

    if not Orgs and not Users:
        print("[ERROR] 未指定任何组织或用户", file=sys.stderr)
        sys.exit(2)

    Session = GHSession()
    SectionMd = BuildMarkdownSection(Orgs, Users, Grouped, SortKey, Limit, Session)
    Changed = ReplaceInReadme(Args.readme, SectionMd)
    print("[INFO] README 已更新 ✅" if Changed else "[INFO] 无变化")

if __name__ == "__main__":
    Main()
