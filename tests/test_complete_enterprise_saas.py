"""
Automated Test Suite for Complete Enterprise SaaS Ecosystem Matrix
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sovereign_infrastructure", "nextgen_systems")))

from complete_enterprise_saas_ecosystem import (
    FixedAssetDepreciationEngine,
    InventoryFIFOEngine,
    MultiEntityConsolidationEngine,
    MeteredUsageBillingEngine,
    SmartDunningEngine,
    GlobalSalesTaxEngine,
    PTOAccrualEngine,
    ExpenseOCRMatchingEngine,
    PurchaseOrderMatchingEngine
)

class TestCompleteEnterpriseSaaSEcosystem(unittest.TestCase):

    def setUp(self):
        self.depreciation = FixedAssetDepreciationEngine()
        self.fifo = InventoryFIFOEngine()
        self.consolidation = MultiEntityConsolidationEngine()
        self.metered = MeteredUsageBillingEngine()
        self.dunning = SmartDunningEngine()
        self.tax = GlobalSalesTaxEngine()
        self.pto = PTOAccrualEngine()
        self.ocr = ExpenseOCRMatchingEngine()
        self.po = PurchaseOrderMatchingEngine()

    def test_01_depreciation(self):
        res = self.depreciation.calculate_straight_line_depreciation(240000.0, 40000.0, 5)
        self.assertEqual(res["annual_depreciation"], 40000.0)

    def test_02_fifo_inventory(self):
        res = self.fifo.calculate_fifo_cogs(150)
        self.assertEqual(res["total_cogs"], 7750.0)

    def test_03_multi_entity(self):
        res = self.consolidation.consolidate_entities(500000.0, 250000.0, 50000.0)
        self.assertEqual(res["consolidated_revenue"], 700000.0)

    def test_04_metered_billing(self):
        res = self.metered.calculate_metered_bill(99.0, 20000)
        self.assertEqual(res["total_bill_usd"], 124.0)

    def test_05_smart_dunning(self):
        res = self.dunning.execute_dunning_retry("sub_101", 1)
        self.assertEqual(res["dunning_action"], "Immediate Retry")

    def test_06_sales_tax(self):
        res = self.tax.calculate_location_tax(100.0, "DE")
        self.assertEqual(res["tax_amount"], 19.0)

    def test_07_pto_accrual(self):
        res = self.pto.calculate_pto_accrual(160.0)
        self.assertEqual(res["accrued_pto_hours"], 8.0)

    def test_08_expense_ocr(self):
        res = self.ocr.process_receipt_ocr("AWS", 250.0)
        self.assertTrue(res["policy_compliant"])

    def test_09_po_3way_matching(self):
        res = self.po.match_3way_po(5000.0, 5000.0, 5000.0)
        self.assertTrue(res["is_3way_matched"])

if __name__ == "__main__":
    unittest.main()
