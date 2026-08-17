"""
Automated Testing Suite for Sovereign Engine Dashboard REST API & 15+ Enterprise SaaS Endpoints
"""

import sys
import os
import unittest
import json
import io

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sovereign_dashboard_server import SovereignDashboardHandler


class TestDashboardAPI(unittest.TestCase):

    def invoke_endpoint(self, path: str, method: str = "GET", body: dict = None) -> dict:
        body_bytes = json.dumps(body).encode("utf-8") if body else b""
        rfile = io.BytesIO(body_bytes)
        wfile = io.BytesIO()

        handler = SovereignDashboardHandler.__new__(SovereignDashboardHandler)
        handler.path = path
        handler.rfile = rfile
        handler.wfile = wfile
        handler.headers = {"Content-Length": str(len(body_bytes))}

        handler.response_code = None
        handler.response_headers = {}

        def mock_send_response(code, message=None):
            handler.response_code = code

        def mock_send_header(keyword, value):
            handler.response_headers[keyword] = value

        def mock_end_headers():
            pass

        handler.send_response = mock_send_response
        handler.send_header = mock_send_header
        handler.end_headers = mock_end_headers

        if method.upper() == "GET":
            handler.do_GET()
        else:
            handler.do_POST()

        output_bytes = wfile.getvalue()
        self.assertEqual(handler.response_code, 200)
        return json.loads(output_bytes.decode("utf-8")) if output_bytes else {}

    def test_01_overview_endpoint(self):
        res = self.invoke_endpoint("/api/v1/overview", "GET")
        self.assertEqual(res["arr"], 1787040.0)
        self.assertEqual(res["cores_entangled"], 6)

    def test_02_ledger_endpoint(self):
        res = self.invoke_endpoint("/api/v1/ledger", "GET")
        self.assertEqual(res["net_income"], 331246.0)
        self.assertEqual(res["status"], "QUICKBOOKS_REPLACED")

    def test_03_balance_sheet_endpoint(self):
        res = self.invoke_endpoint("/api/v1/balance_sheet", "GET")
        self.assertTrue(res["is_balanced"])

    def test_04_cash_flow_endpoint(self):
        res = self.invoke_endpoint("/api/v1/cash_flow", "GET")
        self.assertGreater(res["net_cash_flow"], 0)

    def test_05_ap_aging_endpoint(self):
        res = self.invoke_endpoint("/api/v1/ap/aging", "GET")
        self.assertIn("total_ap", res)

    def test_06_orchestrator_audit_endpoint(self):
        res = self.invoke_endpoint("/api/v1/orchestrator/audit", "GET")
        self.assertTrue(res["trial_balance_balanced"])
        self.assertEqual(res["system_health_status"], "AUDIT_PASSED")

    def test_07_orchestrator_statement_endpoint(self):
        res = self.invoke_endpoint("/api/v1/orchestrator/statement", "GET")
        self.assertIn("cores_status", res)
        self.assertIn("financial_audit", res)

    def test_08_fixed_assets_depreciate_endpoint(self):
        res = self.invoke_endpoint("/api/v1/fixed_assets/depreciate", "POST", {"cost": 240000.0, "salvage": 40000.0, "useful_life_years": 5})
        self.assertEqual(res["annual_depreciation"], 40000.0)
        self.assertEqual(res["status"], "NETSUITE_FIXED_ASSETS_VERIFIED")

    def test_09_inventory_fifo_cogs_endpoint(self):
        res = self.invoke_endpoint("/api/v1/inventory/fifo_cogs", "POST", {"units_sold": 150})
        self.assertEqual(res["total_cogs"], 7750.0)
        self.assertEqual(res["status"], "QUICKBOOKS_FIFO_VERIFIED")

    def test_10_subsidiary_consolidate_endpoint(self):
        res = self.invoke_endpoint("/api/v1/subsidiary/consolidate", "POST", {"us_revenue": 500000.0, "eu_revenue": 250000.0, "intercompany_sales": 50000.0})
        self.assertEqual(res["consolidated_revenue"], 700000.0)
        self.assertEqual(res["status"], "NETSUITE_MULTI_ENTITY_CONSOLIDATED")

    def test_11_metered_billing_calculate_endpoint(self):
        res = self.invoke_endpoint("/api/v1/metered_billing/calculate", "POST", {"base_subscription": 99.0, "api_calls_used": 20000})
        self.assertEqual(res["total_bill_usd"], 124.0)
        self.assertEqual(res["status"], "STRIPE_METERED_BILLING_VERIFIED")

    def test_12_dunning_retry_endpoint(self):
        res = self.invoke_endpoint("/api/v1/dunning/retry", "POST", {"subscriber_id": "sub_101", "retry_attempt": 1})
        self.assertEqual(res["dunning_action"], "Immediate Retry")
        self.assertEqual(res["status"], "REVENUECAT_DUNNING_ACTIVE")

    def test_13_tax_calculate_endpoint(self):
        res = self.invoke_endpoint("/api/v1/tax/calculate", "POST", {"amount": 100.0, "country_code": "DE"})
        self.assertEqual(res["tax_amount"], 19.0)
        self.assertEqual(res["status"], "AVALARA_STRIPE_TAX_VERIFIED")

    def test_14_pto_accrual_endpoint(self):
        res = self.invoke_endpoint("/api/v1/pto/accrual", "POST", {"hours_worked": 160.0})
        self.assertEqual(res["accrued_pto_hours"], 8.0)
        self.assertEqual(res["status"], "GUSTO_PTO_ACCRUED")

    def test_15_expense_ocr_match_endpoint(self):
        res = self.invoke_endpoint("/api/v1/expense/ocr_match", "POST", {"merchant": "AWS", "amount": 250.0})
        self.assertEqual(res["auto_category"], "5030 - Cloud Compute")
        self.assertEqual(res["status"], "EXPENSIFY_OCR_MATCHED")

    def test_16_po_match_3way_endpoint(self):
        res = self.invoke_endpoint("/api/v1/po/match_3way", "POST", {"po_amount": 5000.0, "receiving_slip_amount": 5000.0, "vendor_invoice_amount": 5000.0})
        self.assertTrue(res["is_3way_matched"])
        self.assertEqual(res["status"], "BILL_COM_3WAY_MATCHED")

    def test_17_xfin_settle_endpoint(self):
        res = self.invoke_endpoint("/api/v1/xfin/settle", "POST", {"user_id": "usr_x1", "fiat_amount": 100.0, "currency": "EUR"})
        self.assertEqual(res["status"], "SETTLED")
        self.assertEqual(res["settled_usd"], 108.70)

    def test_18_xfin_hedge_endpoint(self):
        res = self.invoke_endpoint("/api/v1/xfin/hedge", "POST", {"currency": "EUR", "amount_usd": 50000.0})
        self.assertEqual(res["status"], "ACTIVE_HEDGE")

    def test_19_aura_credit_risk_endpoint(self):
        res = self.invoke_endpoint("/api/v1/aura/credit_risk", "POST", {"user_id": "usr_a1", "payment_history_ratio": 0.98, "subscription_cost": 299.0})
        self.assertEqual(res["underwriting"]["status"], "APPROVED")

    def test_20_pulse_churn_risk_endpoint(self):
        res = self.invoke_endpoint("/api/v1/pulse/churn_risk", "POST", {"user_id": "usr_p1", "engagement_score": 0.85})
        self.assertIn("churn_risk", res)
        self.assertIn("discounted_ltv", res)

    def test_21_mint_tokens_endpoint(self):
        res = self.invoke_endpoint("/api/v1/mint/tokens", "POST", {"user_id": "usr_m1", "fiat_amount_usd": 100.0, "action": "mint"})
        self.assertEqual(res["system"], "MINT")
        self.assertGreater(res["tokens_minted"], 0)

    def test_22_grid_device_endpoint(self):
        res = self.invoke_endpoint("/api/v1/grid/device", "POST", {"device_id": "dev_g1", "device_type": "WEAR_OS_WATCH"})
        self.assertEqual(res["registration"]["status"], "ONLINE")

    def test_23_nexs_offering_endpoint(self):
        res = self.invoke_endpoint("/api/v1/nexs/offering", "POST", {"user_id": "usr_n1", "country_code": "BR", "base_usd_price": 20.0})
        self.assertEqual(res["adapted_usd_price"], 9.0)

    def test_24_orchestrator_lifecycle_endpoint(self):
        res = self.invoke_endpoint("/api/v1/orchestrator/lifecycle", "POST", {
            "user_id": "usr_full_vip", "country_code": "DE", "device_id": "dev_watch_de", "fiat_amount": 99.99, "currency": "EUR"
        })
        self.assertEqual(res["status"], "NEXTGEN_PIPELINE_SUCCESS")

    def test_25_gemini_chat_endpoint(self):
        res = self.invoke_endpoint("/api/v1/gemini/chat", "POST", {"message": "Audit cores"})
        self.assertIn("reply", res)


if __name__ == "__main__":
    unittest.main()
