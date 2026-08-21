from __future__ import annotations

import copy
import hashlib
import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


TOOLS_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = TOOLS_DIR / "Scripts" / "GenerateAirportRules.py"
SPEC = importlib.util.spec_from_file_location("GenerateAirportRules", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("无法加载机场规则生成器")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class AirportRulesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.SourceBytes = (TOOLS_DIR / "机场通用规则.yaml").read_bytes()
        cls.SourceText = cls.SourceBytes.decode("utf-8-sig")
        cls.SourceDigest = hashlib.sha256(cls.SourceBytes).hexdigest()
        cls.Data = yaml.safe_load(cls.SourceText)

    def test_generated_config_matches_tracked_file(self) -> None:
        Generated, Stats = MODULE.BuildText(self.Data, self.SourceDigest)
        Tracked = (TOOLS_DIR / "机场通用规则.conf").read_bytes()
        self.assertEqual(MODULE.EncodeOutput(Generated), Tracked)
        self.assertEqual(Stats["group_count"], len(self.Data["proxy-groups"]))
        self.assertEqual(Stats["rule_count"], len(self.Data["rules"]))

    def test_generated_config_uses_shadowrocket_syntax(self) -> None:
        Generated, Stats = MODULE.BuildText(self.Data, self.SourceDigest)
        self.assertIn("[General]", Generated)
        self.assertIn("[Proxy Group]", Generated)
        self.assertIn("[Rule]", Generated)
        self.assertIn("FINAL,通用代理", Generated)
        self.assertNotIn("MATCH,", Generated)
        self.assertNotIn("rule-providers:", Generated)
        self.assertNotIn("payload:", Generated)
        self.assertEqual(Stats["remote_rule_count"], 4)

    def test_changed_region_filter_is_rejected(self) -> None:
        Data = copy.deepcopy(self.Data)
        Region = next(Group for Group in Data["proxy-groups"] if Group["name"] == "香港")
        Region["filter"] += "|测试"
        with self.assertRaisesRegex(ValueError, "YAML filter 已变化"):
            MODULE.BuildText(Data, self.SourceDigest)

    def test_unknown_provider_is_rejected(self) -> None:
        Data = copy.deepcopy(self.Data)
        Data["rule-providers"]["unknown"] = {
            "type": "http",
            "behavior": "domain",
            "url": "https://example.com/rules.list",
        }
        with self.assertRaisesRegex(ValueError, "适配表不同步"):
            MODULE.BuildText(Data, self.SourceDigest)

    def test_changed_provider_contract_is_rejected(self) -> None:
        Data = copy.deepcopy(self.Data)
        Data["rule-providers"]["private"]["behavior"] = "classical"
        with self.assertRaisesRegex(ValueError, "type/behavior 已变化"):
            MODULE.BuildText(Data, self.SourceDigest)

    def test_untrusted_shadowrocket_url_is_rejected(self) -> None:
        with patch.dict(
            MODULE.SHADOWROCKET_RULE_URLS,
            {"private": "https://example.com/private.list"},
            clear=False,
        ):
            with self.assertRaisesRegex(ValueError, "URL 不受信"):
                MODULE.BuildText(self.Data, self.SourceDigest)

    def test_byte_differences_are_not_synchronized(self) -> None:
        Generated, _ = MODULE.BuildText(self.Data, self.SourceDigest)
        GeneratedBytes = MODULE.EncodeOutput(Generated)
        self.assertFalse(MODULE.IsSynchronized(b"\xef\xbb\xbf" + GeneratedBytes, GeneratedBytes))
        self.assertFalse(MODULE.IsSynchronized(GeneratedBytes.replace(b"\n", b"\r\n"), GeneratedBytes))
        self.assertNotIn(b"\r\n", GeneratedBytes)
        self.assertFalse(GeneratedBytes.startswith(b"\xef\xbb\xbf"))


if __name__ == "__main__":
    unittest.main()
