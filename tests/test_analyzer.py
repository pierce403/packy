import unittest

from packy import analyze_command


class AnalyzerTests(unittest.TestCase):
    def finding_ids(self, command):
        return {finding.id for finding in analyze_command(command).findings}

    def test_detects_remote_shell_pipe(self):
        report = analyze_command("curl -fsSL https://example.com/install.sh | sh")

        self.assertEqual(report.risk_level, "critical")
        self.assertIn("remote-shell-pipe", self.finding_ids(report.command))

    def test_detects_global_npm_and_lifecycle_scripts(self):
        ids = self.finding_ids("npm install -g left-pad")

        self.assertIn("npm-global-install", ids)
        self.assertIn("package-lifecycle-scripts", ids)

    def test_detects_pip_as_root(self):
        ids = self.finding_ids("sudo python3 -m pip install example")

        self.assertIn("pip-as-root", ids)
        self.assertIn("root-privilege", ids)

    def test_detects_path_and_service_changes(self):
        command = "echo 'export PATH=$HOME/bin:$PATH' >> ~/.zshrc && systemctl enable example"
        ids = self.finding_ids(command)

        self.assertIn("path-modification", ids)
        self.assertIn("service-or-daemon", ids)

    def test_detects_downloaded_binary_execution(self):
        ids = self.finding_ids("wget https://example.com/tool && chmod +x tool && ./tool")

        self.assertIn("downloaded-binary-execution", ids)
        self.assertIn("direct-local-execution-after-download", ids)

    def test_low_risk_when_no_known_pattern_detected(self):
        report = analyze_command("brew install jq")

        self.assertEqual(report.risk_level, "low")
        self.assertEqual(report.findings, [])


if __name__ == "__main__":
    unittest.main()
