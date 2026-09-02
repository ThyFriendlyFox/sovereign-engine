"""
Unit Tests for SOVEREIGN OS Alpha Unlimited Work Engine & AlphaAppWorkGenerator
"""

import unittest
from sovereign_infrastructure.nextgen_systems.alpha_unlimited_work_engine import (
    AlphaUnlimitedWorkEngine,
    AlphaAppWorkGenerator
)
from sovereign_infrastructure.nextgen_systems.full_saas_accounting_suite import GeneralLedgerEngine


class TestAlphaUnlimitedWorkEngine(unittest.TestCase):

    def test_alpha_app_work_generator_init(self):
        generator = AlphaAppWorkGenerator()
        self.assertEqual(len(generator.apps), 200)
        self.assertEqual(len(generator.completed_tasks), 0)

    def test_generate_work_for_individual_app(self):
        generator = AlphaAppWorkGenerator()
        
        # Test QuickBooks Online (Accounting & Tax)
        task1 = generator.generate_work_for_app("app_001")
        self.assertEqual(task1["status"], "COMPLETED_SUCCESSFULLY")
        self.assertEqual(task1["app_name"], "QuickBooks Online")
        self.assertEqual(task1["category"], "Accounting & Tax")
        self.assertIn("reconciled", task1["action_summary"])
        self.assertEqual(task1["execution_mode"], "ALPHA_UNLIMITED_AUTONOMIC")
        self.assertTrue(task1["general_ledger_synced"])

        # Test Stripe Payments (Payment Gateways & Subscriptions)
        task2 = generator.generate_work_for_app("Stripe Payments")
        self.assertEqual(task2["status"], "COMPLETED_SUCCESSFULLY")
        self.assertEqual(task2["app_name"], "Stripe Payments")
        self.assertEqual(task2["category"], "Payment Gateways & Subscriptions")
        self.assertIn("StoreKit 2", task2["action_summary"])

        # Test OpenAI GPT-4o (AI & Neural Engines)
        task3 = generator.generate_work_for_app("OpenAI GPT-4o")
        self.assertEqual(task3["status"], "COMPLETED_SUCCESSFULLY")
        self.assertEqual(task3["category"], "AI & Neural Engines")

        self.assertEqual(len(generator.completed_tasks), 3)

    def test_generate_work_with_gl_integration(self):
        gl = GeneralLedgerEngine()
        generator = AlphaAppWorkGenerator(gl_engine=gl)
        
        task = generator.generate_work_for_app("app_001")
        self.assertIsNotNone(task["journal_entry_id"])
        
        tb = gl.generate_trial_balance()
        self.assertTrue(tb["is_balanced"])

    def test_generate_work_for_all_200_apps(self):
        generator = AlphaAppWorkGenerator()
        res = generator.generate_work_for_all_200_apps(batch_size=50, parallel=True)

        self.assertEqual(res["total_apps_processed"], 200)
        self.assertEqual(res["total_tasks_completed"], 200)
        self.assertEqual(res["execution_mode"], "ALPHA_UNLIMITED_PARALLEL")
        self.assertEqual(res["general_ledger_variance"], 0.00)
        self.assertEqual(res["status"], "ALL_200_APPS_AUTONOMIC_WORK_COMPLETED")
        self.assertEqual(len(res["category_breakdown"]), 10)
        self.assertEqual(sum(res["category_breakdown"].values()), 200)

    def test_alpha_unlimited_work_engine_cycles(self):
        gl = GeneralLedgerEngine()
        engine = AlphaUnlimitedWorkEngine(gl_engine=gl, max_workers=20)

        report = engine.execute_unlimited_work_cycle(num_cycles=2)
        self.assertEqual(report["cycles_executed"], 2)
        self.assertEqual(report["total_apps_processed"], 400)
        self.assertEqual(report["total_tasks_completed"], 400)
        self.assertEqual(report["general_ledger_variance"], 0.00)
        self.assertEqual(report["status"], "UNLIMITED_WORK_CYCLE_SUCCESSFUL")
        self.assertGreater(report["throughput_tasks_per_sec"], 0)

    def test_alpha_unlimited_work_engine_audit(self):
        engine = AlphaUnlimitedWorkEngine()
        audit = engine.run_alpha_audit()

        self.assertEqual(audit["engine_name"], "SOVEREIGN OS Alpha Unlimited Work Engine")
        self.assertEqual(audit["capacity"], "UNLIMITED_PARALLEL_EXECUTION")
        self.assertEqual(audit["total_supported_apps"], 200)
        self.assertEqual(audit["status"], "ALPHA_ENGINE_ONLINE_OPTIMAL")
        self.assertEqual(audit["substrate_status"]["XFIN"], "HEALTHY")

    def test_worker_pool_scaling_and_telemetry(self):
        engine = AlphaUnlimitedWorkEngine(max_workers=10)
        scale_res = engine.scale_worker_pool(100)
        self.assertEqual(scale_res["max_workers"], 100)

        telemetry = engine.stream_autonomic_work_telemetry()
        self.assertEqual(telemetry["active_max_workers"], 100)


if __name__ == "__main__":
    unittest.main()
    assert telemetry["status"] == "TELEMETRY_STREAM_HEALTHY"
    assert telemetry["gl_variance_usd"] == 0.00


def test_work_history_filtering_and_clearing():
    generator = AlphaAppWorkGenerator()
    generator.generate_work_for_app("QuickBooks Online")
    generator.generate_work_for_app("Stripe Payments")

    acct_tasks = generator.get_work_history(category="Accounting & Tax")
    assert len(acct_tasks) == 1
    assert acct_tasks[0]["app_name"] == "QuickBooks Online"

    breakdown = generator.get_category_work_breakdown()
    assert breakdown["Accounting & Tax"] == 1
    assert breakdown["Payment Gateways & Subscriptions"] == 1

    generator.clear_history()
    assert len(generator.completed_tasks) == 0
