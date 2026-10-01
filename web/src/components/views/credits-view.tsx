"use client";

import { useEffect, useState } from "react";
import { DitherButton } from "@/components/dither-kit/button";
import { Badge } from "@/components/ui/badge";
import { useAppState } from "@/components/providers/app-state";
import { fetchApprovals, fetchTaxCredits, type ApprovalRow, type TaxCredits } from "@/lib/books-api";

const STATES = ["CA", "NY", "TX", "WA", "FL"] as const;

function money(n: number | undefined) {
  return (n ?? 0).toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });
}

export function CreditsView() {
  const { pushArtifact } = useAppState();
  const [state, setState] = useState<(typeof STATES)[number]>("CA");
  const [credits, setCredits] = useState<TaxCredits | null>(null);
  const [approvals, setApprovals] = useState<ApprovalRow[]>([]);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    setErr(null);
    fetchTaxCredits(state)
      .then(setCredits)
      .catch(() => setErr("Books API offline — start sovereign_dashboard_server.py on :8090"));
    fetchApprovals(20)
      .then((r) => setApprovals(r.approvals))
      .catch(() => setApprovals([]));
  }, [state]);

  const refs = (credits?.statutory_references ?? []).map((r) =>
    typeof r === "string" ? r : String(r.citation ?? r.name ?? JSON.stringify(r)),
  );

  return (
    <div className="flex h-full flex-col">
      <header className="border-b border-border px-6 py-4">
        <p className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">Compliance</p>
        <div className="flex flex-wrap items-end justify-between gap-3">
          <h1 className="text-xl font-medium tracking-tight">Tax credits</h1>
          <div className="flex gap-1">
            {STATES.map((s) => (
              <DitherButton
                key={s}
                color="grey"
                variant={s === state ? "solid" : "hatched"}
                className="text-[11px]"
                onClick={() => setState(s)}
              >
                {s}
              </DitherButton>
            ))}
          </div>
        </div>
      </header>

      <div className="flex-1 space-y-4 overflow-auto p-6">
        {err && (
          <p className="rounded-md border border-border bg-muted/40 px-3 py-2 text-xs text-muted-foreground">{err}</p>
        )}

        <div className="grid gap-3 sm:grid-cols-3">
          <Tile label="Estimated credits" value={money(credits?.total_estimated_tax_credits)} accent />
          <Tile label="Federal Section 41" value={money(credits?.federal_section_41_credit)} />
          <Tile label={`${state} state credit`} value={money(credits?.state_tax_credit)} />
        </div>

        <section className="rounded-lg border border-border bg-card/40 p-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-medium">Qualified research expenses</h2>
            <Badge variant="outline" className="rounded-sm font-mono text-[10px]">
              {credits?.compliance_status ?? "—"}
            </Badge>
          </div>
          <dl className="mt-3 grid gap-2 text-sm sm:grid-cols-2">
            <Row k="Engineering payroll" v={money(credits?.rd_payroll_qre)} />
            <Row k="Cloud compute" v={money(credits?.cloud_compute_qre)} />
            <Row k="Total QRE" v={money(credits?.total_qualified_research_expenses)} />
            <Row k="Section 174 amortization deduction" v={money(credits?.sec_174_annual_amortization_deduction)} />
          </dl>
          {refs.length > 0 && (
            <ul className="mt-3 list-disc space-y-1 pl-5 text-xs text-muted-foreground">
              {refs.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>
          )}
          <div className="mt-4">
            <DitherButton
              color="grey"
              variant="hatched"
              className="text-[11px]"
              disabled={!credits}
              onClick={() =>
                credits &&
                pushArtifact({
                  id: `credits_${state}`,
                  kind: "document",
                  title: `${state} research credit claim file`,
                  subtitle: money(credits.total_estimated_tax_credits),
                  payload: credits as unknown as Record<string, unknown>,
                })
              }
            >
              Preview claim file
            </DitherButton>
          </div>
        </section>

        <section className="rounded-lg border border-border bg-card/40 p-4">
          <h2 className="text-sm font-medium">Recent decisions</h2>
          {!approvals.length && (
            <p className="mt-2 text-sm text-muted-foreground">
              No approvals recorded yet. Decisions from the mobile app land here.
            </p>
          )}
          <ul className="mt-2 divide-y divide-border text-sm">
            {approvals.map((a) => (
              <li key={a.id} className="flex items-center justify-between gap-3 py-2">
                <span className="min-w-0 truncate">
                  <span className="font-mono text-[10px] uppercase text-muted-foreground">{a.kind}</span>{" "}
                  {a.subject ?? a.card_id}
                </span>
                <span className="flex shrink-0 items-center gap-2">
                  {a.amount != null && <span className="font-mono tabular-nums">{money(a.amount)}</span>}
                  <Badge variant="secondary" className="rounded-sm text-[10px]">
                    {a.decision}
                  </Badge>
                </span>
              </li>
            ))}
          </ul>
        </section>

        <p className="text-xs text-muted-foreground">
          Estimates only. Credits are claimed on the return by a tax professional; this view assembles the evidence.
        </p>
      </div>
    </div>
  );
}

function Tile({ label, value, accent }: { label: string; value: string; accent?: boolean }) {
  return (
    <div className="rounded-lg border border-border bg-card/40 p-4">
      <p className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">{label}</p>
      <p className={`mt-1 font-mono text-2xl tabular-nums ${accent ? "text-foreground" : "text-muted-foreground"}`}>
        {value}
      </p>
    </div>
  );
}

function Row({ k, v }: { k: string; v: string }) {
  return (
    <div className="flex items-center justify-between gap-3">
      <dt className="text-muted-foreground">{k}</dt>
      <dd className="font-mono tabular-nums">{v}</dd>
    </div>
  );
}
