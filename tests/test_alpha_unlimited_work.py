"""
Automated Test Suite for SOVEREIGN OS Alpha Unlimited Work Engine
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sovereign_infrastructure", "nextgen_systems")))

from alpha_unlimited_work_engine import AlphaUnlimitedWorkEngine, AlphaAppWorkGenerator

class TestAlphaUnlimitedWorkEngine(unittest.TestCase):

    def setUp(self):
        self.engine = AlphaUnlimitedWorkEngine()

    def test_01_alpha_engine_audit(self):
        audit = self.engine.run_alpha_audit()
        self.assertEqual(audit["capacity"], "UNLIMITED_PARALLEL_EXECUTION")
        self.assertEqual(audit["total_supported_apps"], 200)

    def test_02_generate_work_single_app(self):
        task = self.engine.work_generator.generate_work_for_app("app_001")
        self.assertEqual(task["app_name"], "QuickBooks Online")
        self.assertEqual(task["status"], "COMPLETED_SUCCESSFULLY")

    def test_03_generate_work_all_200_apps(self):
        res = self.engine.work_generator.generate_work_for_all_200_apps()
        self.assertEqual(res["total_apps_processed"], 200)
        self.assertEqual(res["total_tasks_completed"], 200)
        self.assertEqual(res["status"], "ALL_200_APPS_AUTONOMIC_WORK_COMPLETED")

if __name__ == "__main__":
    unittest.main()
