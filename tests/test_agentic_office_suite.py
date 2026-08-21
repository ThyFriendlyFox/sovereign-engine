"""
Automated Test Suite for SOVEREIGN OS Mega Office Suite & Agentic Multi-Artifact AI Generator
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sovereign_infrastructure", "nextgen_systems")))

from agentic_multi_artifact_generator import AgenticMultiArtifactGenerator
from mega_office_business_suite import (
    MegaOfficeBusinessSuite,
    SovereignDocsModule,
    SovereignSheetsModule,
    SovereignSlidesModule,
    SovereignSignModule,
    SovereignMailModule,
    SovereignDriveModule,
    SovereignFormsModule,
    SovereignCalendarModule
)
from full_saas_accounting_suite import GeneralLedgerEngine


class TestAgenticOfficeSuite(unittest.TestCase):

    def setUp(self):
        self.gl = GeneralLedgerEngine()
        self.generator = AgenticMultiArtifactGenerator(gl_engine=self.gl)
        self.office = MegaOfficeBusinessSuite(gl_engine=self.gl)

    def test_01_supported_artifact_types_count(self):
        self.assertEqual(len(self.generator.supported_artifact_types), 8)

    def test_02_generate_spreadsheet_artifact(self):
        art = self.generator.generate_artifact("SPREADSHEET", "Q1 Financial Model")
        self.assertEqual(art["artifact_type"], "SPREADSHEET")
        self.assertIn("headers", art["content"])

    def test_03_generate_presentation_artifact(self):
        art = self.generator.generate_artifact("PRESENTATION", "Board Pitch Deck")
        self.assertEqual(art["artifact_type"], "PRESENTATION")
        self.assertEqual(len(art["content"]["slides"]), 3)

    def test_04_generate_diagram_artifact(self):
        art = self.generator.generate_artifact("DIAGRAM", "System Architecture Flow")
        self.assertEqual(art["artifact_type"], "DIAGRAM")
        self.assertIn("Mermaid", art["content"]["diagram_type"])

    def test_05_generate_invoice_bill_artifact(self):
        art = self.generator.generate_artifact("INVOICE_BILL", "Enterprise SaaS Invoice")
        self.assertEqual(art["artifact_type"], "INVOICE_BILL")
        self.assertEqual(art["content"]["total_due"], 173200.00)
        self.assertIsNotNone(art["content"]["gl_entry_id"])

    def test_06_generate_contract_legal_artifact(self):
        art = self.generator.generate_artifact("CONTRACT_LEGAL", "SLA Agreement")
        self.assertEqual(art["artifact_type"], "CONTRACT_LEGAL")
        self.assertIn("Wyoming DUNA DAO", art["content"]["governance"])

    def test_07_generate_code_module_artifact(self):
        art = self.generator.generate_artifact("CODE_MODULE", "Autonomic Worker Module")
        self.assertEqual(art["artifact_type"], "CODE_MODULE")
        self.assertEqual(art["content"]["language"], "Python 3.11")

    def test_08_generate_analytics_report_artifact(self):
        art = self.generator.generate_artifact("ANALYTICS_REPORT", "Executive Cohort Report")
        self.assertEqual(art["artifact_type"], "ANALYTICS_REPORT")
        self.assertEqual(art["content"]["metrics"]["arr"], 1787040.00)

    def test_09_sovereign_sheets_solver(self):
        res = self.office.sheets.solve_formulas({"revenue_rows": [100.0, 200.0], "expense_rows": [50.0, 50.0]})
        self.assertEqual(res["net_profit"], 200.0)

    def test_10_sovereign_sign_execution(self):
        res = self.office.sign.execute_signature("Master SLA", "cfo@apex.com")
        self.assertEqual(res["status"], "SOVEREIGN_SIGN_EXECUTED")
        verification = self.office.sign.verify_zk_proof(res["signature_id"], res["zk_proof_signature"])
        self.assertTrue(verification["is_valid"])

    def test_11_mega_office_suite_audit(self):
        audit = self.office.run_full_office_audit()
        self.assertEqual(audit["status"], "MEGA_OFFICE_SUITE_FULLY_OPERATIONAL")
        self.assertEqual(len(audit["apps_included"]), 8)
        self.assertIn("SovereignForms", audit["apps_included"])
        self.assertIn("SovereignCalendar", audit["apps_included"])

    def test_12_generate_multi_artifact_suite(self):
        suite = self.generator.generate_multi_artifact_suite("Enterprise Release Suite", "Apex Global")
        self.assertEqual(suite["artifacts_count"], 8)
        self.assertEqual(suite["status"], "MULTI_ARTIFACT_SUITE_GENERATED")

    def test_13_export_artifacts(self):
        art = self.generator.generate_artifact("DOCUMENT", "System Architecture Blueprint")
        json_export = self.generator.export_artifact_as_json(art["artifact_id"])
        md_export = self.generator.export_artifact_as_markdown(art["artifact_id"])
        self.assertIn("Blueprint", json_export)
        self.assertIn("# System Architecture Blueprint", md_export)

    def test_14_sovereign_forms_and_calendar(self):
        form = self.office.forms.create_form("Lead Intake", [{"name": "company", "type": "text"}])
        self.assertEqual(form["status"], "SOVEREIGN_FORMS_CREATED")
        resp = self.office.forms.submit_response(form["form_id"], {"company": "Acme Corp"})
        self.assertTrue(resp["validated"])

        event = self.office.calendar.schedule_event("Quarterly Audit", "2026-09-15T14:00:00Z")
        self.assertEqual(event["status"], "SOVEREIGN_CALENDAR_EVENT_SCHEDULED")
        conflict = self.office.calendar.resolve_conflict(event["event_id"])
        self.assertFalse(conflict["conflict_detected"])

    def test_15_business_package_execution(self):
        pkg = self.office.create_business_package("Apex Corp", "Apex Global", 200000.0)
        self.assertEqual(pkg["status"], "BUSINESS_PACKAGE_CREATED_SUCCESSFULLY")
        self.assertIsNotNone(pkg["multi_artifact_suite"])


if __name__ == "__main__":
    unittest.main()
