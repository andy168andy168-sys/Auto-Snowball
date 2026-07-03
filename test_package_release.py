from argparse import Namespace

from scripts.package_release import release_manifest


def test_release_manifest_uses_current_verification_evidence():
    args = Namespace(
        version="10.60",
        name="auto_snowball_web_v10_60_full_get_read_only_hardening",
        tests="255 passed",
        safety_tests="36 passed",
        browser_e2e="2 passed",
        actual_5050_playwright="1 passed",
        release_tooling="package integrity PASS",
        status="blocked",
        blocking_item=["正式 API 金鑰已設定", "小額灰度需手動確認"],
    )

    manifest = release_manifest(args, "candidate.zip", 123, "abc", ["part_00.b64"])

    assert manifest["version"] == "10.60"
    assert manifest["tests"] == "255 passed"
    assert manifest["production_safety_websocket"] == "36 passed"
    assert manifest["blocking_items"] == args.blocking_item


def test_blocked_manifest_fails_closed_without_explicit_evidence():
    args = Namespace(
        version="10.60",
        name="candidate",
        tests="not recorded",
        safety_tests="not recorded",
        browser_e2e="not recorded",
        actual_5050_playwright="not recorded",
        release_tooling="not recorded",
        status="blocked",
        blocking_item=[],
    )

    manifest = release_manifest(args, "candidate.zip", 123, "abc", [])

    assert manifest["status"] == "blocked"
    assert manifest["blocking_items"] == ["formal launch evidence not provided"]
