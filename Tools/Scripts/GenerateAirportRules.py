#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import difflib
import hashlib
from pathlib import Path
from urllib.parse import urlsplit

import yaml


SCRIPT_PATH = Path(__file__).resolve()
TOOLS_DIR = SCRIPT_PATH.parents[1]
SOURCE_PATH = TOOLS_DIR / "机场通用规则.yaml"
OUTPUT_PATH = TOOLS_DIR / "机场通用规则.conf"

REGION_FILTERS = {
    "香港": {
        "source": r"(?i)^(?!.*cn).*(港|hk|hongkong|hong.?kong)",
        "shadowrocket": r"(?=.*(港|HK|hk|HongKong|hongkong|Hong Kong|hong kong))^((?!(cn|CN)).)*$",
    },
    "台湾": {
        "source": r"(?i)^(?!.*cn).*(台湾|tw|taiwan)",
        "shadowrocket": r"(?=.*(台湾|TW|tw|Taiwan|taiwan))^((?!(cn|CN)).)*$",
    },
    "日本": {
        "source": r"(?i)^(?!.*cn).*(日本|jp|japan)",
        "shadowrocket": r"(?=.*(日本|JP|jp|Japan|japan))^((?!(cn|CN)).)*$",
    },
    "韩国": {
        "source": r"(?i)^(?!.*cn).*(韩国|kr|korea)",
        "shadowrocket": r"(?=.*(韩国|KR|kr|Korea|korea))^((?!(cn|CN)).)*$",
    },
    "新加坡": {
        "source": r"(?i)^(?!.*cn).*(新加坡|singapore|(^|[^a-z])(sg|sgp)([^a-z]|$))",
        "shadowrocket": r"(?=.*(新加坡|Singapore|singapore|SG|sg|SGP|sgp))^((?!(cn|CN)).)*$",
    },
    "英国": {
        "source": r"(?i)^(?!.*cn).*(英国|uk|britain|united.?kingdom)",
        "shadowrocket": r"(?=.*(英国|UK|uk|Britain|britain|United Kingdom|united kingdom))^((?!(cn|CN)).)*$",
    },
    "美国": {
        "source": r"(?i)^(?!.*cn).*(美国|us|america|united.?states)",
        "shadowrocket": r"(?=.*(美国|US|us|USA|usa|America|america|United States|united states))^((?!(cn|CN)).)*$",
    },
}

SHADOWROCKET_RULE_URLS = {
    "private": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/Lan/Lan.list",
    "reject": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/Advertising/Advertising.list",
    "direct": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/ChinaMax/ChinaMax.list",
    "proxy": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/Proxy/Proxy.list",
}

GENERAL_LINES = [
    "[General]",
    "# 本配置不包含节点或订阅 Token。请先在 Shadowrocket 首页添加机场订阅。",
    "skip-proxy = 192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,localhost,*.local,captive.apple.com",
    "tun-excluded-routes = 10.0.0.0/8,127.0.0.0/8,169.254.0.0/16,172.16.0.0/12,192.168.0.0/16,224.0.0.0/4,255.255.255.255/32",
    "dns-server = 223.5.5.5,119.29.29.29",
    "fallback-dns-server = system",
    "ipv6 = false",
    "dns-direct-system = false",
    "private-ip-answer = true",
    "dns-direct-fallback-proxy = true",
    "icmp-auto-reply = true",
    "block-quic = all-proxy",
]


def ValidateAdapters(Providers: dict) -> None:
    if set(Providers) != set(SHADOWROCKET_RULE_URLS):
        raise ValueError(
            f"规则集适配表不同步：YAML={sorted(Providers)} / Shadowrocket={sorted(SHADOWROCKET_RULE_URLS)}"
        )
    for Name, Provider in Providers.items():
        if not isinstance(Provider, dict) or Provider.get("type") != "http" or Provider.get("behavior") != "domain":
            raise ValueError(f"规则集 {Name} 的 type/behavior 已变化，必须重新评估 Shadowrocket 映射")
        Url = SHADOWROCKET_RULE_URLS[Name]
        Parts = urlsplit(Url)
        if (
            Parts.scheme != "https"
            or Parts.hostname != "raw.githubusercontent.com"
            or "/rule/Shadowrocket/" not in Parts.path
            or not Parts.path.endswith(".list")
        ):
            raise ValueError(f"规则集 {Name} 的 Shadowrocket URL 不受信：{Url}")


def BuildText(Data: dict, SourceDigest: str) -> tuple[str, dict[str, int]]:
    Providers = Data.get("rule-providers", {})
    Groups = Data.get("proxy-groups", [])
    Rules = Data.get("rules", [])
    if not isinstance(Providers, dict) or not isinstance(Groups, list) or not isinstance(Rules, list):
        raise ValueError("机场通用规则.yaml 缺少有效的 rule-providers、proxy-groups 或 rules")
    ValidateAdapters(Providers)

    Lines = [
        "# Shadowrocket 机场通用规则",
        "# 由 Tools/Scripts/GenerateAirportRules.py 根据机场通用规则.yaml 自动生成，请勿直接编辑。",
        f"# YAML SHA-256：{SourceDigest}",
        "# 节点由 Shadowrocket 中已添加的机场订阅提供。",
        "",
        *GENERAL_LINES,
        "",
        "[Proxy Group]",
    ]

    for Group in Groups:
        if not isinstance(Group, dict):
            raise ValueError("proxy-groups 中存在非映射项目")
        Name = str(Group["name"])
        GroupType = str(Group["type"])
        if GroupType == "select":
            Policies = [str(Value) for Value in Group.get("proxies", [])]
            if not Policies:
                raise ValueError(f"策略组 {Name} 没有可选策略")
            Lines.append(f"{Name} = select,{','.join(Policies)},select=0")
            continue
        if GroupType == "fallback" and Group.get("include-all"):
            FilterMapping = REGION_FILTERS.get(Name)
            if not FilterMapping:
                raise ValueError(f"缺少地区组 {Name} 的 Shadowrocket 过滤器")
            if Group.get("filter") != FilterMapping["source"]:
                raise ValueError(f"地区组 {Name} 的 YAML filter 已变化，必须同步更新 Shadowrocket 过滤器")
            Filter = FilterMapping["shadowrocket"]
            Url = str(Group.get("url", "http://www.gstatic.com/generate_204"))
            Interval = int(Group.get("interval", 300))
            Lines.append(
                f"{Name} = fallback,policy-regex-filter={Filter},"
                f"interval={Interval},timeout=5,select=0,url={Url}"
            )
            continue
        raise ValueError(f"不支持的策略组：{Name} / {GroupType}")

    Lines.extend(["", "[Rule]"])
    RemoteRuleCount = 0
    for RawRule in Rules:
        if not isinstance(RawRule, str) or not RawRule.strip():
            raise ValueError("rules 中存在非字符串或空规则")
        Parts = [Part.strip() for Part in RawRule.split(",")]
        if Parts[0] == "RULE-SET":
            ProviderName = Parts[1]
            if ProviderName not in Providers:
                raise ValueError(f"源规则集 {ProviderName} 不存在")
            ShadowrocketUrl = SHADOWROCKET_RULE_URLS.get(ProviderName)
            if not ShadowrocketUrl:
                raise ValueError(f"规则集 {ProviderName} 缺少 Shadowrocket 原生 URL")
            Parts[1] = ShadowrocketUrl
            RemoteRuleCount += 1
        elif Parts[0] == "MATCH":
            Parts[0] = "FINAL"
        Lines.append(",".join(Parts))

    Text = "\n".join(Lines) + "\n"
    Stats = {
        "group_count": len(Groups),
        "rule_count": len(Rules),
        "remote_rule_count": RemoteRuleCount,
    }
    return Text, Stats


def EncodeOutput(Text: str) -> bytes:
    return Text.encode("utf-8")


def IsSynchronized(Existing: bytes, Generated: bytes) -> bool:
    return Existing == Generated


def Main() -> int:
    Parser = argparse.ArgumentParser(description="从 YAML 权威源生成 Shadowrocket .conf")
    Mode = Parser.add_mutually_exclusive_group(required=True)
    Mode.add_argument("--write", action="store_true", help="根据 YAML 写入 Shadowrocket .conf")
    Mode.add_argument("--check", action="store_true", help="只检查生成结果是否同步，不写文件")
    Args = Parser.parse_args()

    SourceBytes = SOURCE_PATH.read_bytes()
    SourceText = SourceBytes.decode("utf-8-sig")
    SourceDigest = hashlib.sha256(SourceBytes).hexdigest()
    Data = yaml.safe_load(SourceText)
    Text, Stats = BuildText(Data, SourceDigest)
    GeneratedBytes = EncodeOutput(Text)
    if Args.check:
        ExistingBytes = OUTPUT_PATH.read_bytes() if OUTPUT_PATH.exists() else b""
        if not IsSynchronized(ExistingBytes, GeneratedBytes):
            Existing = ExistingBytes.decode("utf-8-sig", errors="replace")
            Diff = difflib.unified_diff(
                Existing.splitlines(),
                Text.splitlines(),
                fromfile=str(OUTPUT_PATH),
                tofile="重新生成结果",
                lineterm="",
            )
            print("机场通用规则.conf 与 YAML 权威源不同步。请运行：")
            print("python Tools/Scripts/GenerateAirportRules.py --write")
            print("\n".join(list(Diff)[:120]))
            return 1
        print({"status": "同步", **Stats})
        return 0

    OUTPUT_PATH.write_bytes(GeneratedBytes)
    print({"status": "已生成", **Stats})
    return 0


if __name__ == "__main__":
    raise SystemExit(Main())
