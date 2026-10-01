package com.sovereignengine.books.data

/**
 * Sample data used when the books API is unreachable or demo mode is on.
 * It mirrors the founder story: three cards, ninety seconds, done.
 */
object DemoData {

    private val similar = listOf(
        InboxTransaction("txn_s1", "2026-08-30", "Notion Labs", "Notion Labs", 4200.0, false, "Software", "Business Checking", "4521"),
        InboxTransaction("txn_s2", "2026-07-30", "Notion Labs", "Notion Labs", 4200.0, false, "Software", "Business Checking", "4521"),
        InboxTransaction("txn_s3", "2026-06-30", "Notion Labs", "Notion Labs", 3900.0, false, "Software", "Business Checking", "4521"),
    )

    val credits = TaxCreditEstimate(
        jurisdiction = "US_CA",
        cloudQre = 18_400.0,
        payrollQre = 61_000.0,
        totalQre = 79_400.0,
        federalCredit = 11_116.0,
        stateCredit = 11_910.0,
        totalCredits = 23_026.0,
        amortizationDeduction = 15_880.0,
        references = listOf(
            "IRC Section 41: Credit for increasing research activities",
            "IRC Section 174: Amortization of research and experimental expenditures",
            "California R&D Credit (Revenue and Taxation Code 23609)",
        ),
    )

    val cards: List<ApprovalCard> = listOf(
        ApprovalCard.Categorize(
            txn = InboxTransaction("txn_demo_1", "2026-09-30", "Notion Labs", "Notion Labs", 4200.0, false, "Software", "Business Checking", "4521"),
            similar = similar,
            confidence = 74,
        ),
        ApprovalCard.TaxCredit(
            estimate = credits,
            evidence = listOf(
                "412 commits across 3 engineering projects this quarter",
                "Payroll: 4 engineers, 61,000 USD allocated to qualified research",
                "Cloud compute: 18,400 USD on build and test infrastructure",
            ),
        ),
        ApprovalCard.InvoiceChase(
            invoice = Invoice("inv_demo_1", "Harbor Logistics", 12_500.0, "open", "2026-07-02", 90),
            draftEmail = "Hi Dana,\n\nInvoice INV-0412 for 12,500 USD was due on July 2 and is now 90 days past due. Could you let us know when we can expect payment, or if anything is holding it up?\n\nThanks,\nSovereign Demo Co",
        ),
    )

    val data = BooksData(
        home = HomeSnapshot("Sovereign Demo Co", 24_180.42, cards.size, false, "offline"),
        runway = Runway(4.84, 24_180.42, "Runway about 4.8 months at 5,000 USD per month burn"),
        cards = cards,
        credits = credits,
        activity = listOf(
            AgentActivity("07:02", "Categorized 11 transactions with high confidence"),
            AgentActivity("07:02", "Posted 11 journal entries; trial balance OK"),
            AgentActivity("07:05", "Found 61,000 USD of payroll that qualifies for Section 41"),
            AgentActivity("07:06", "Drafted a follow-up for one invoice 90 days overdue"),
        ),
        offline = true,
    )
}
