package com.sovereignengine.books.data

data class HomeSnapshot(
    val businessName: String,
    val cashBalance: Double,
    val inboxCount: Int,
    val bankConnected: Boolean,
    val mode: String,
)

data class InboxTransaction(
    val id: String,
    val date: String,
    val name: String,
    val merchant: String,
    /** Plaid convention: positive is money out, negative is money in. */
    val amount: Double,
    val pending: Boolean,
    val categorySuggested: String?,
    val accountName: String,
    val mask: String,
)

data class Runway(
    val monthsRunway: Double,
    val cash: Double,
    val message: String,
)

data class TaxCreditEstimate(
    val jurisdiction: String,
    val cloudQre: Double,
    val payrollQre: Double,
    val totalQre: Double,
    val federalCredit: Double,
    val stateCredit: Double,
    val totalCredits: Double,
    val amortizationDeduction: Double,
    val references: List<String>,
)

data class Invoice(
    val id: String,
    val customer: String,
    val amount: Double,
    val status: String,
    val dueDate: String?,
    val daysOverdue: Int,
)

data class AgentActivity(
    val time: String,
    val text: String,
)

/** One decision the agents could not make alone. */
sealed class ApprovalCard {
    abstract val id: String

    data class Categorize(
        val txn: InboxTransaction,
        val similar: List<InboxTransaction>,
        val confidence: Int,
    ) : ApprovalCard() {
        override val id get() = "cat_" + txn.id
    }

    data class TaxCredit(
        val estimate: TaxCreditEstimate,
        val evidence: List<String>,
    ) : ApprovalCard() {
        override val id get() = "credit_" + estimate.jurisdiction
    }

    data class InvoiceChase(
        val invoice: Invoice,
        val draftEmail: String,
    ) : ApprovalCard() {
        override val id get() = "inv_" + invoice.id
    }
}

data class BooksData(
    val home: HomeSnapshot,
    val runway: Runway?,
    val cards: List<ApprovalCard>,
    val credits: TaxCreditEstimate?,
    val activity: List<AgentActivity>,
    val offline: Boolean,
)
