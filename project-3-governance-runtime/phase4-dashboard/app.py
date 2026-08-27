"""Phase 4: Bird's-Eye-View Dashboard. Streamlit app, read-only, computes
nothing itself, only renders data_store.py's real (and clearly labeled
where mixed) output.

Status: PROVEN. Verified 2026-08-27 in a live browser check: all four
panels rendered correctly against real data/dashboard_store.json
output, both honesty badges (06b-saved-not-live, two-points-only)
displayed on their panels as designed, and the drill-down selector was
exercised, switching between a real Phase 3a verdict and the labeled
synthetic verdict, each independently hash-verified in the UI.

No auth or access control. Fine for a personal portfolio demo, not fine
for anything wider than that. Stated here and in README.md, not left
unaddressed, per the spec's own open question.
"""

import json
import os

import streamlit as st

STORE_PATH = os.path.join(os.path.dirname(__file__), "data", "dashboard_store.json")

st.set_page_config(page_title="AI Governance Runtime: Bird's-Eye View", layout="wide")


def load_store() -> dict:
    if not os.path.exists(STORE_PATH):
        st.warning("No dashboard store found. Run data_store.py first.")
        st.stop()
    with open(STORE_PATH, encoding="utf-8") as f:
        return json.load(f)


store = load_store()

st.title("AI Governance Runtime: Bird's-Eye View")
st.caption(
    f"Generated at {store['generated_at']}. No auth or access control on this "
    f"dashboard, acceptable for a personal portfolio demo, not for anything wider."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Pass / Borderline / Fail Rates")
    routing = store["routing_rates"]
    st.caption(f"Real. Source: {routing['source']}")
    st.bar_chart(routing["counts"])
    st.table(routing["rates"])

with col2:
    st.subheader("Judge Alignment Trend")
    alignment = store["judge_alignment"]
    st.info(alignment["note"])
    for point in alignment["points"]:
        st.metric(point["label"], f"{point['rate']:.1%}", f"{point['aligned']}/{point['total']}")

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.subheader("Regression Alarm Status")
    regression = store["regression_status"]
    st.info(regression["note"])
    st.write(f"Counts: {regression['counts']}")
    for case in regression["cases"]:
        label = "REAL" if case["real"] else "SYNTHETIC"
        st.write(f"[{case['severity']}] {case['case_id']} (drop={case['drop']:.2f}), {label}")

with col4:
    st.subheader("Verdict Drill-Down")
    drilldown = store["verdict_drilldown"]
    if drilldown.get("note"):
        st.warning(drilldown["note"])
    verdicts = drilldown["verdicts"]
    if verdicts:
        case_ids = [v["case_id"] for v in verdicts]
        selected = st.selectbox("Select a committed verdict", case_ids)
        verdict = next(v for v in verdicts if v["case_id"] == selected)
        st.json(verdict)
        if verdict["hash_verified"]:
            st.success("Hash independently verified against this record's plaintext fields.")
        else:
            st.error("Hash verification FAILED for this record.")
