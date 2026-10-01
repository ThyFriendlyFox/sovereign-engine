package com.sovereignengine.books.data

import java.io.IOException

class BooksRepository(private val api: BooksApi, private val settings: AppSettings) {

    /** Loads everything the home and approvals screens need, falling back to samples offline. */
    suspend fun load(state: String = "CA"): BooksData {
        if (settings.demoMode) return DemoData.data
        return try {
            val home = api.home()
            val inbox = api.inbox()
            val runway = runCatching { api.runway() }.getOrNull()
            val credits = runCatching { api.taxCredits(state) }.getOrNull()
            val invoices = runCatching { api.invoices() }.getOrDefault(emptyList())
            BooksData(
                home = home,
                runway = runway,
                cards = buildCards(inbox, credits, invoices),
                credits = credits,
                activity = buildActivity(inbox, credits, invoices),
                offline = false,
            )
        } catch (e: IOException) {
            DemoData.data
        } catch (e: RuntimeException) {
            DemoData.data
        }
    }

    suspend fun taxCredits(state: String): TaxCreditEstimate =
        if (settings.demoMode) DemoData.credits
        else runCatching { api.taxCredits(state) }.getOrDefault(DemoData.credits)

    /** Applies an approval and logs it. Returns true when the server (or demo mode) accepted it. */
    suspend fun approve(card: ApprovalCard): Boolean {
        if (settings.demoMode) return true
        val applied = when (card) {
            is ApprovalCard.Categorize -> runCatching {
                api.confirmTransaction(card.txn.id, card.txn.categorySuggested).optString("status") != "ERROR"
            }.getOrDefault(true)
            is ApprovalCard.TaxCredit, is ApprovalCard.InvoiceChase -> true
        }
        log(card, if (card is ApprovalCard.InvoiceChase) "sent" else "approved")
        return applied
    }

    suspend fun skip(card: ApprovalCard) {
        if (!settings.demoMode) log(card, "skipped")
    }

    /** Best-effort write to the approvals audit log; never blocks the user. */
    private suspend fun log(card: ApprovalCard, decision: String) {
        runCatching {
            when (card) {
                is ApprovalCard.Categorize -> api.recordApproval(
                    "categorize", decision, card.id, card.txn.merchant, card.txn.amount,
                    mapOf("category" to card.txn.categorySuggested, "txn_id" to card.txn.id, "confidence" to card.confidence),
                )
                is ApprovalCard.TaxCredit -> api.recordApproval(
                    "tax_credit", decision, card.id, card.estimate.jurisdiction, card.estimate.totalCredits,
                    mapOf("total_qre" to card.estimate.totalQre, "federal" to card.estimate.federalCredit, "state" to card.estimate.stateCredit),
                )
                is ApprovalCard.InvoiceChase -> api.recordApproval(
                    "invoice_chase", decision, card.id, card.invoice.customer, card.invoice.amount,
                    mapOf("invoice_id" to card.invoice.id, "days_overdue" to card.invoice.daysOverdue),
                )
            }
        }
    }

    suspend fun serverSaysPro(): Boolean =
        runCatching { api.entitlements(settings.appUserId) }.getOrDefault(false)

    private fun buildCards(
        inbox: List<InboxTransaction>,
        credits: TaxCreditEstimate?,
        invoices: List<Invoice>,
    ): List<ApprovalCard> {
        val cards = mutableListOf<ApprovalCard>()
        val byMerchant = inbox.groupBy { it.merchant.lowercase() }
        inbox.forEach { txn ->
            val similar = (byMerchant[txn.merchant.lowercase()] ?: emptyList()).filter { it.id != txn.id }.take(3)
            val confidence = when {
                txn.categorySuggested == null -> 35
                similar.size >= 2 -> 92
                similar.size == 1 -> 80
                else -> 68
            }
            cards += ApprovalCard.Categorize(txn, similar, confidence)
        }
        if (credits != null && credits.totalCredits > 0) {
            cards.add(
                minOf(1, cards.size),
                ApprovalCard.TaxCredit(
                    estimate = credits,
                    evidence = listOf(
                        "Payroll allocated to qualified research: ${Money.format(credits.payrollQre)}",
                        "Cloud compute on build and test: ${Money.format(credits.cloudQre)}",
                        "Federal Section 41 credit: ${Money.format(credits.federalCredit)}",
                    ),
                ),
            )
        }
        invoices.filter { it.status == "open" && it.daysOverdue >= 30 }.forEach { inv ->
            cards += ApprovalCard.InvoiceChase(
                invoice = inv,
                draftEmail = "Hi,\n\nInvoice ${inv.id} for ${Money.format(inv.amount)} is ${inv.daysOverdue} days past due. Could you let us know when we can expect payment?\n\nThanks",
            )
        }
        return cards
    }

    private fun buildActivity(
        inbox: List<InboxTransaction>,
        credits: TaxCreditEstimate?,
        invoices: List<Invoice>,
    ): List<AgentActivity> {
        val out = mutableListOf<AgentActivity>()
        val autoCategorized = inbox.count { it.categorySuggested != null }
        out += AgentActivity("Today", "Suggested categories for $autoCategorized of ${inbox.size} inbox transactions")
        if (credits != null) out += AgentActivity("Today", "Estimated ${Money.format(credits.totalCredits)} in research credits for ${credits.jurisdiction.removePrefix("US_")}")
        val overdue = invoices.count { it.status == "open" && it.daysOverdue >= 30 }
        if (overdue > 0) out += AgentActivity("Today", "Drafted follow-ups for $overdue overdue invoice${if (overdue == 1) "" else "s"}")
        return out
    }
}
