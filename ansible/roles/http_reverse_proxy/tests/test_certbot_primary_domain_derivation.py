"""
Tests for Task 28: Derive nginx_certbot_primary_domain from nginx_certbot_domains.

The role's cert_stat task references
/etc/letsencrypt/live/{{ nginx_certbot_primary_domain }}/fullchain.pem,
which must equal the first comma-separated entry in
nginx_certbot_domains (that is the directory name certbot creates).
Deriving it in vars/main.yml gives a single source of truth and avoids
drift between the domains list and the cert directory name.

Verifies that:
- vars/main.yml defines nginx_certbot_primary_domain as a real key
  (not a commented stub).
- The expression references nginx_certbot_domains, splits on ',',
  indexes [0], and pipes through `trim`.
- No commented-out stub for the same key remains.

Run with:
    python -m unittest discover -s ansible/roles/http_reverse_proxy/tests \
        -p "test_certbot_primary_domain_derivation.py" -v
"""
import os
import re
import unittest

import yaml

VARS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "vars", "main.yml"
)

EXPECTED_VAR = "nginx_certbot_primary_domain"


class TestCertbotPrimaryDomainDerivation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(VARS_FILE) as f:
            cls.raw = f.read()
        cls.parsed = yaml.safe_load(cls.raw) or {}

    def test_primary_domain_defined_as_real_key(self):
        self.assertIn(
            EXPECTED_VAR,
            self.parsed,
            f"{EXPECTED_VAR} must be a real (uncommented) key in vars/main.yml.",
        )

    def test_primary_domain_is_derived_from_domains(self):
        value = self.parsed.get(EXPECTED_VAR, "")
        self.assertIn(
            "nginx_certbot_domains",
            value,
            f"{EXPECTED_VAR} must be derived from nginx_certbot_domains, "
            "not a separately-defined secret.",
        )

    def test_primary_domain_uses_split_index_zero(self):
        value = self.parsed.get(EXPECTED_VAR, "")
        # tolerate either '.split(",")[0]' or ".split(',')[0]"
        self.assertRegex(
            value,
            r"""\.split\(\s*['"],['"]\s*\)\s*\[\s*0\s*\]""",
            f"{EXPECTED_VAR} must use .split(',')[0] to extract the first domain.",
        )

    def test_primary_domain_trims_whitespace(self):
        value = self.parsed.get(EXPECTED_VAR, "")
        self.assertIn(
            "trim",
            value,
            f"{EXPECTED_VAR} must pipe through `trim` to tolerate "
            "'a.example.com, b.example.com' style spacing.",
        )

    def test_no_commented_stub_remains(self):
        # The original vars/main.yml had a commented example for the
        # same key. Once the real derivation is in place, the stub
        # should be removed to avoid two definitions a reader has to
        # reconcile.
        commented_stub = re.search(
            rf"^\s*#\s*{re.escape(EXPECTED_VAR)}\s*:",
            self.raw,
            re.MULTILINE,
        )
        self.assertIsNone(
            commented_stub,
            f"A commented-out '{EXPECTED_VAR}:' stub still exists in "
            "vars/main.yml — remove it to keep a single source of truth.",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
