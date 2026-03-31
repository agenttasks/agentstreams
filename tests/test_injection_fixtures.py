"""Tests for M10 injection test fixtures.

Verifies the security-audit scanner and extract-patterns pipeline handle
malicious content embedded in taxonomy-format files safely:
1. Security audit detects injections in fixture files (when not allowlisted)
2. Extract-patterns processes fixtures without executing injected content
3. Clean fixtures produce zero findings
4. Agent boundary fixtures are flagged correctly
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

audit_mod = import_module("security-audit")
Finding = audit_mod.Finding
check_prompt_injection = audit_mod.check_prompt_injection
check_shell_injection = audit_mod.check_shell_injection
check_secret_leakage = audit_mod.check_secret_leakage
check_dependency_risks = audit_mod.check_dependency_risks
check_agent_boundaries = audit_mod.check_agent_boundaries
check_crawled_content_handling = audit_mod.check_crawled_content_handling
scan_file = audit_mod.scan_file

extract_mod = import_module("extract-patterns")
parse_taxonomy_pages = extract_mod.parse_taxonomy_pages
classify_page_type = extract_mod.classify_page_type
extract_topics = extract_mod.extract_topics
analyze_page = extract_mod.analyze_page

FIXTURES_DIR = Path(__file__).parent / "fixtures"


# ── Helper ────────────────────────────────────────────────


def read_fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text()


# ── Classic injection detection ───────────────────────────


class TestClassicInjectionDetection:
    """Verify scanner catches classic prompt injection patterns."""

    def test_detects_ignore_instructions(self):
        content = read_fixture("injection_classic.md")
        findings = check_prompt_injection(Path("test_fixture_classic.md"), content)
        ignore_findings = [f for f in findings if "Classic prompt injection" in f.message]
        assert len(ignore_findings) >= 1

    def test_detects_jailbreak_pattern(self):
        content = read_fixture("injection_classic.md")
        findings = check_prompt_injection(Path("test_fixture_classic.md"), content)
        jailbreak = [f for f in findings if "Jailbreak" in f.message]
        assert len(jailbreak) >= 1

    def test_detects_xml_tag_injection(self):
        content = read_fixture("injection_classic.md")
        findings = check_prompt_injection(Path("test_fixture_classic.md"), content)
        xml_findings = [f for f in findings if "XML tag" in f.message or "privilege" in f.message]
        assert len(xml_findings) >= 1

    def test_detects_fake_system_message(self):
        content = read_fixture("injection_classic.md")
        findings = check_prompt_injection(Path("test_fixture_classic.md"), content)
        system_findings = [f for f in findings if "system message" in f.message.lower() or "Fake system" in f.message]
        assert len(system_findings) >= 1

    def test_all_findings_are_high_severity(self):
        content = read_fixture("injection_classic.md")
        findings = check_prompt_injection(Path("test_fixture_classic.md"), content)
        injection_findings = [f for f in findings if f.category == "prompt-injection" and "API_KEY" not in f.message and "secret" not in f.message.lower()]
        for f in injection_findings:
            assert f.severity == Finding.HIGH, f"Expected HIGH, got {f.severity}: {f.message}"

    def test_classic_total_finding_count(self):
        content = read_fixture("injection_classic.md")
        findings = check_prompt_injection(Path("test_fixture_classic.md"), content)
        # At least: 2x ignore-instructions, 1x jailbreak, 2x XML tag, 1x fake system
        assert len(findings) >= 5


# ── Secret leakage detection ─────────────────────────────


class TestSecretLeakageDetection:
    """Verify scanner catches secrets in fixture files."""

    def test_detects_anthropic_api_key(self):
        content = read_fixture("injection_secrets.md")
        findings = check_secret_leakage(Path("test_fixture_secrets.md"), content)
        anthropic_keys = [f for f in findings if "Anthropic" in f.message or "Generic API key" in f.message]
        assert len(anthropic_keys) >= 1

    def test_detects_github_pat(self):
        content = read_fixture("injection_secrets.md")
        findings = check_secret_leakage(Path("test_fixture_secrets.md"), content)
        github = [f for f in findings if "GitHub" in f.message]
        assert len(github) >= 1

    def test_detects_aws_key(self):
        content = read_fixture("injection_secrets.md")
        findings = check_secret_leakage(Path("test_fixture_secrets.md"), content)
        aws = [f for f in findings if "AWS" in f.message]
        assert len(aws) >= 1

    def test_detects_jwt(self):
        content = read_fixture("injection_secrets.md")
        findings = check_secret_leakage(Path("test_fixture_secrets.md"), content)
        jwt = [f for f in findings if "JWT" in f.message]
        assert len(jwt) >= 1

    def test_detects_private_key(self):
        content = read_fixture("injection_secrets.md")
        findings = check_secret_leakage(Path("test_fixture_secrets.md"), content)
        privkey = [f for f in findings if "Private key" in f.message]
        assert len(privkey) >= 1

    def test_detects_database_url(self):
        content = read_fixture("injection_secrets.md")
        findings = check_secret_leakage(Path("test_fixture_secrets.md"), content)
        db = [f for f in findings if "Database" in f.message]
        assert len(db) >= 1

    def test_detects_slack_token(self):
        content = read_fixture("injection_secrets.md")
        findings = check_secret_leakage(Path("test_fixture_secrets.md"), content)
        slack = [f for f in findings if "Slack" in f.message]
        assert len(slack) >= 1

    def test_all_secret_findings_are_critical(self):
        content = read_fixture("injection_secrets.md")
        findings = check_secret_leakage(Path("test_fixture_secrets.md"), content)
        for f in findings:
            assert f.severity == Finding.CRITICAL

    def test_secrets_total_count(self):
        content = read_fixture("injection_secrets.md")
        findings = check_secret_leakage(Path("test_fixture_secrets.md"), content)
        # anthropic keys, github, aws, jwt, db url, private key, slack
        assert len(findings) >= 7


# ── Polyglot / obfuscation detection ─────────────────────


class TestPolyglotDetection:
    """Verify scanner catches polyglot and obfuscated patterns."""

    def test_detects_hidden_injection_in_comments(self):
        content = read_fixture("injection_polyglot.md")
        findings = check_prompt_injection(Path("test_fixture_polyglot.md"), content)
        # HTML comments with "ignore all previous instructions"
        ignore = [f for f in findings if "injection" in f.message.lower() or "ignore" in f.message.lower()]
        assert len(ignore) >= 1

    def test_detects_hardcoded_secrets_in_polyglot(self):
        content = read_fixture("injection_polyglot.md")
        findings = check_secret_leakage(Path("test_fixture_polyglot.md"), content)
        assert len(findings) >= 1

    def test_detects_fake_system_in_comments(self):
        content = read_fixture("injection_polyglot.md")
        findings = check_prompt_injection(Path("test_fixture_polyglot.md"), content)
        system = [f for f in findings if "system" in f.message.lower()]
        assert len(system) >= 1


# ── Agent boundary fixtures ──────────────────────────────


class TestAgentBoundaryFixtures:
    """Verify agent boundary checks flag insecure agent definitions."""

    def test_flags_missing_tools_restriction(self):
        content = read_fixture("injection_agent_boundary.md")
        # Simulate path as if it were in .claude/agents/
        findings = check_agent_boundaries(
            Path("/project/.claude/agents/injection_agent_boundary.md"), content
        )
        assert any("no tools restriction" in f.message for f in findings)

    def test_flags_write_tools_on_readonly_agent(self):
        content = read_fixture("injection_agent_write_tools.md")
        findings = check_agent_boundaries(
            Path("/project/.claude/agents/injection_agent_write_tools.md"), content
        )
        assert any("write tools" in f.message for f in findings)

    def test_flags_wildcard_tools(self):
        content = read_fixture("injection_agent_wildcard.md")
        findings = check_agent_boundaries(
            Path("/project/.claude/agents/injection_agent_wildcard.md"), content
        )
        assert any("wildcard" in f.message for f in findings)


# ── Clean fixture (negative control) ─────────────────────


class TestCleanFixture:
    """Verify clean taxonomy produces zero findings."""

    def test_no_prompt_injection_findings(self):
        content = read_fixture("clean_taxonomy.md")
        findings = check_prompt_injection(Path("clean_taxonomy.md"), content)
        assert len(findings) == 0

    def test_no_secret_findings(self):
        content = read_fixture("clean_taxonomy.md")
        findings = check_secret_leakage(Path("clean_taxonomy.md"), content)
        assert len(findings) == 0

    def test_no_shell_injection_findings(self):
        content = read_fixture("clean_taxonomy.md")
        findings = check_shell_injection(Path("clean_taxonomy.py"), content)
        assert len(findings) == 0


# ── Extract-patterns safe handling ───────────────────────


class TestExtractPatternsSafety:
    """Verify extract-patterns processes injected content safely.

    The extractor should parse the taxonomy format and extract metadata
    without executing or propagating injected content.
    """

    def test_parses_classic_injection_pages(self):
        content = read_fixture("injection_classic.md")
        pages = parse_taxonomy_pages(content)
        assert len(pages) == 3

    def test_parses_secrets_injection_pages(self):
        content = read_fixture("injection_secrets.md")
        pages = parse_taxonomy_pages(content)
        assert len(pages) == 2

    def test_parses_polyglot_pages(self):
        content = read_fixture("injection_polyglot.md")
        pages = parse_taxonomy_pages(content)
        assert len(pages) == 3

    def test_parses_clean_pages(self):
        content = read_fixture("clean_taxonomy.md")
        pages = parse_taxonomy_pages(content)
        assert len(pages) == 2

    def test_injected_content_not_in_extracted_topics(self):
        """Injection text should not become a valid topic tag."""
        content = read_fixture("injection_classic.md")
        pages = parse_taxonomy_pages(content)
        for page in pages:
            result = analyze_page(page, "example.com")
            # "ignore-instructions" or "jailbreak" should not appear as topics
            for topic in result["topics"]:
                assert "ignore" not in topic.lower()
                assert "jailbreak" not in topic.lower()
                assert "dan" not in topic.lower()

    def test_classify_page_type_with_injected_content(self):
        """Page type classification should work despite injections."""
        content = read_fixture("injection_classic.md")
        pages = parse_taxonomy_pages(content)
        for page in pages:
            ptype = classify_page_type(page["url"], page["content"])
            # Should classify as a valid type, not something corrupted
            assert ptype in ("guide", "reference", "tutorial", "blog", "changelog", "api-doc")

    def test_clean_fixture_extracts_valid_patterns(self):
        """Clean fixture should produce valid SDK/API patterns."""
        content = read_fixture("clean_taxonomy.md")
        pages = parse_taxonomy_pages(content)
        results = [analyze_page(p, "example.com") for p in pages]
        # Should detect Python code
        all_langs = set()
        for r in results:
            all_langs.update(r["code_langs"])
        assert "python" in all_langs

    def test_extract_preserves_url_integrity(self):
        """URLs should be extracted correctly even from injected fixtures."""
        content = read_fixture("injection_classic.md")
        pages = parse_taxonomy_pages(content)
        urls = [p["url"] for p in pages]
        assert all(u.startswith("https://example.com/") for u in urls)


# ── Cross-check: scan_file on fixtures ───────────────────


class TestScanFileOnFixtures:
    """Run scan_file against fixture files to verify integrated behavior.

    Fixture files are in INJECTION_ALLOWLIST so scan_file skips injection/secret
    checks on them (by design — prevents CI false positives). We verify:
    1. Allowlisted fixtures produce 0 injection/secret findings via scan_file
    2. Clean fixtures produce 0 findings overall
    3. Direct check functions (without allowlist) still detect everything
    """

    def test_scan_allowlisted_classic_skips_injection_checks(self):
        """Allowlisted fixture files should not produce findings via scan_file."""
        fixture_path = FIXTURES_DIR / "injection_classic.md"
        findings = scan_file(fixture_path)
        injection_findings = [f for f in findings if f.category == "prompt-injection"]
        assert len(injection_findings) == 0  # allowlisted

    def test_scan_allowlisted_secrets_skips_secret_checks(self):
        """Allowlisted fixture files should not produce findings via scan_file."""
        fixture_path = FIXTURES_DIR / "injection_secrets.md"
        findings = scan_file(fixture_path)
        secret_findings = [f for f in findings if f.category == "secret-leakage"]
        assert len(secret_findings) == 0  # allowlisted

    def test_scan_clean_finds_nothing(self):
        fixture_path = FIXTURES_DIR / "clean_taxonomy.md"
        findings = scan_file(fixture_path)
        assert len(findings) == 0

    def test_direct_checks_still_detect_when_not_allowlisted(self):
        """Using non-allowlisted paths, the checks should detect injections."""
        content = read_fixture("injection_classic.md")
        findings = check_prompt_injection(Path("test_fixture_classic.md"), content)
        assert len(findings) >= 5  # proves detection works outside allowlist
