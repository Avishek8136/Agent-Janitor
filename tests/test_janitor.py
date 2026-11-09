import unittest
from pathlib import Path
from agent_janitor.scanner import Scanner
from agent_janitor.models import TrapClassification, TicketStatus
from agent_janitor.classifier import classify_todo
from agent_janitor.trackers.mock_tracker import MockTracker
from agent_janitor.cleaner import CodeCleaner

class TestAgentJanitor(unittest.TestCase):
    def setUp(self):
        self.sample_dir = Path(__file__).parent / "sample_project"
        self.mock_file = self.sample_dir / "bug_statuses.json"

    def test_scanner_finds_todos(self):
        scanner = Scanner(self.sample_dir)
        items = list(scanner.scan_all())
        self.assertGreaterEqual(len(items), 4)

        # Check Java TODO detection
        java_todos = [i for i in items if i.file_path.name == "SurfaceControlTest.java"]
        self.assertEqual(len(java_todos), 2)
        self.assertTrue(any(i.bug_id == "888123" for i in java_todos))
        self.assertTrue(any(i.bug_id == "444001" for i in java_todos))

    def test_classification_dead_ends_and_scope_creeps(self):
        scanner = Scanner(self.sample_dir)
        tracker = MockTracker(self.mock_file)
        items = list(scanner.scan_all())

        for item in items:
            if item.bug_id:
                item.ticket_status = tracker.check_status(item.bug_id)
            item.classification = classify_todo(item)

        dead_ends = [i for i in items if i.classification == TrapClassification.DEAD_END]
        scope_creeps = [i for i in items if i.classification == TrapClassification.SCOPE_CREEP_RISK]

        # b/888123 (RESOLVED) and b/444001 (WONT_FIX) should be DEAD_END
        self.assertEqual(len(dead_ends), 2)

        # b/999456 (OPEN) should be SCOPE_CREEP_RISK
        self.assertEqual(len(scope_creeps), 1)
        self.assertEqual(scope_creeps[0].bug_id, "999456")

    def test_cleaner_diff(self):
        scanner = Scanner(self.sample_dir)
        tracker = MockTracker(self.mock_file)
        items = list(scanner.scan_all())
        for item in items:
            if item.bug_id:
                item.ticket_status = tracker.check_status(item.bug_id)
            item.classification = classify_todo(item)

        dead_ends = [i for i in items if i.classification == TrapClassification.DEAD_END]
        cleaner = CodeCleaner(dry_run=True)
        diffs = cleaner.prune_items(dead_ends)

        self.assertEqual(len(diffs), 1)  # Only SurfaceControlTest.java has dead ends
        file_path, diff_str = diffs[0]
        self.assertEqual(file_path.name, "SurfaceControlTest.java")
        self.assertIn("-    // TODO(b/888123): Fix surface flickering", diff_str)

if __name__ == "__main__":
    unittest.main()
