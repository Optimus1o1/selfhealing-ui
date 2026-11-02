import streamlit as st
import pandas as pd
import json
from pathlib import Path
from selfheal.database.connection import DatabaseManager
from selfheal.baseline.repository import BaselineRepository
from selfheal.config import SelfHealConfig

st.set_page_config(
    page_title="Self-Healing UI Automation Portal | Moon Sanctum Labs",
    page_icon="🛡️",
    layout="wide"
)

# Custom Moon Sanctum Labs Dark/Copper Theme styling
st.markdown("""
<style>
    .main { background-color: #0F1013; color: #F2EFE8; }
    h1, h2, h3, h4 { color: #F2EFE8 !important; }
    .stMetric { background-color: #17191E; border: 1px solid #2A2D35; border-radius: 8px; padding: 12px; }
    .stButton>button { background-color: #E0A45C; color: #0F1013; font-weight: bold; border-radius: 6px; }
    .score-badge-approved { background-color: #166534; color: #bbf7d0; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.85rem; }
    .score-badge-rejected { background-color: #991b1b; color: #fecaca; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.85rem; }
    .diff-table th, .diff-table td { padding: 8px 12px; border: 1px solid #2A2D35; text-align: left; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_repo():
    config = SelfHealConfig.load_from_yaml("configs/default.yaml")
    db_mgr = DatabaseManager(config.framework.database_path)
    return BaselineRepository(db_mgr)


repo = get_repo()

st.title("🛡️ Self-Healing UI Automation Portal")
st.caption("Moon Sanctum Labs — *Decode. Build. Evolve.* | Deterministic Locator Recovery & Academic Audit Dashboard")

stats = repo.get_run_statistics()
events = repo.get_healing_events()
test_runs = repo.get_test_runs()

# Top KPI Summary Cards
col1, col2, col3, col4, col5, col6 = st.columns(6)
total_runs = stats.get("total_runs") or 0
total_events = len(events)
approved_events = [e for e in events if e.get("decision") == "APPROVED"]
healing_rate = (len(approved_events) / max(1, total_events)) * 100 if total_events > 0 else 0.0
avg_score = (stats.get("avg_score") or 0.0) * 100
avg_latency = stats.get("avg_latency") or 0.0

col1.metric("Total Test Runs", total_runs)
col2.metric("Total Interceptions", total_events)
col3.metric("Approved Heals", len(approved_events))
col4.metric("Healing Success", f"{healing_rate:.1f}%")
col5.metric("Avg Confidence", f"{avg_score:.1f}%")
col6.metric("Avg Latency", f"{avg_latency:.1f} ms")

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Test Execution Overview",
    "📋 Healing Events & Score Inspector",
    "⚖️ Assisted Review & Promotion",
    "🧬 Baseline Version Comparison",
    "⚡ Performance & Latency Analytics"
])

# =============================================================================
# TAB 1: Test Execution Overview
# =============================================================================
with tab1:
    st.subheader("Test Execution Runs & Session History")
    if not test_runs:
        st.info("No test runs logged yet. Execute tests with `pytest` or `selfheal test` to record sessions.")
    else:
        df_runs = pd.DataFrame(test_runs)
        cols_runs = ["id", "run_uuid", "project_name", "policy", "status", "total_steps", "passed_count", "failed_count", "healed_count", "started_at", "completed_at"]
        available_cols = [c for c in cols_runs if c in df_runs.columns]
        st.dataframe(df_runs[available_cols], use_container_width=True)

        st.markdown("### Run-Level Healing Breakdown")
        col_r1, col_r2, col_r3 = st.columns(3)
        total_steps_all = sum(r.get("total_steps", 0) for r in test_runs)
        total_healed_all = sum(r.get("healed_count", 0) for r in test_runs)
        total_failed_all = sum(r.get("failed_count", 0) for r in test_runs)
        col_r1.metric("Aggregated Steps", total_steps_all)
        col_r2.metric("Healed Steps", total_healed_all)
        col_r3.metric("Unrecoverable Steps", total_failed_all)

# =============================================================================
# TAB 2: Healing Events & Score Inspector
# =============================================================================
with tab2:
    st.subheader("Runtime Interceptions, Diff & Score Breakdown")
    if not events:
        st.info("No healing events recorded. Run a test against a modified UI to populate events.")
    else:
        df_events = pd.DataFrame(events)
        cols_to_show = [
            "id", "target_key", "original_locator", "healed_locator",
            "similarity_score", "decision", "status", "retry_success", "latency_ms", "created_at"
        ]
        available_cols = [c for c in cols_to_show if c in df_events.columns]
        st.dataframe(df_events[available_cols], use_container_width=True)

        st.markdown("### Detailed Event Inspection & Similarity Breakdown")
        selected_id = st.selectbox("Select Event ID to inspect:", df_events["id"].tolist())
        selected_row = next((e for e in events if e["id"] == selected_id), None)

        if selected_row:
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.markdown("#### Locator Transformation")
                st.write("**Target Identity Key:**", f"`{selected_row['target_key']}`")
                st.write("**Original Failed Locator:**", f"`{selected_row['original_locator']}`")
                st.write("**Healed Replacement Locator:**", f"`{selected_row['healed_locator'] or 'N/A'}`")
                st.write("**Engine Decision:**", f"`{selected_row['decision']}`")
                st.write("**Safe Retry Executed:**", "✅ Succeeded" if selected_row.get("retry_success") else "❌ Failed / Skipped")
                st.write("**Reason / Diagnostics:**", selected_row.get("reason", ""))

            with col_d2:
                st.markdown("#### Execution Metrics")
                score_pct = (selected_row.get("similarity_score") or 0.0) * 100
                st.metric("Total Similarity Score", f"{score_pct:.1f}%")
                st.metric("Healing Latency", f"{selected_row.get('latency_ms', 0):.2f} ms")
                st.write("**Audit Timestamp:**", selected_row.get("created_at", ""))

            # Score Breakdown Visualizer
            if selected_row.get("score_breakdown_json"):
                st.markdown("#### Multi-Dimensional Similarity Breakdown")
                breakdown = json.loads(selected_row["score_breakdown_json"])
                b_cols = st.columns(6)
                b_cols[0].metric("Text (30%)", f"{breakdown.get('text_score', 0)*100:.1f}%")
                b_cols[1].metric("Type/Role (20%)", f"{breakdown.get('type_and_role_score', 0)*100:.1f}%")
                b_cols[2].metric("Attributes (20%)", f"{breakdown.get('attributes_score', 0)*100:.1f}%")
                b_cols[3].metric("Parent (15%)", f"{breakdown.get('parent_score', 0)*100:.1f}%")
                b_cols[4].metric("Children (10%)", f"{breakdown.get('children_score', 0)*100:.1f}%")
                b_cols[5].metric("Position (5%)", f"{breakdown.get('position_score', 0)*100:.1f}%")

                # Comparison with baseline fingerprint
                active_fp = repo.get_active_fingerprint(selected_row["target_key"])
                if active_fp:
                    st.markdown("#### Fingerprint Structural Diff")
                    diff_data = [
                        {"Dimension": "Target Key", "Baseline (v1)": active_fp.target_key, "Healed Event": selected_row["target_key"]},
                        {"Dimension": "Tag Name", "Baseline (v1)": active_fp.tag_name, "Healed Event": "(Preserved / Compatible)"},
                        {"Dimension": "Element ID", "Baseline (v1)": active_fp.element_id, "Healed Event": "(Refactored in DOM)"},
                        {"Dimension": "Original Selector", "Baseline (v1)": active_fp.original_selector, "Healed Event": selected_row["healed_locator"]},
                        {"Dimension": "Inner Text", "Baseline (v1)": active_fp.inner_text, "Healed Event": f"Score: {breakdown.get('text_score', 0)*100:.1f}%"},
                    ]
                    st.table(pd.DataFrame(diff_data))

# =============================================================================
# TAB 3: Assisted Review & Promotion Portal
# =============================================================================
with tab3:
    st.subheader("Assisted Review Portal: Pending Healed Locators")
    pending = [e for e in events if e.get("status") == "pending_review" and e.get("decision") == "APPROVED"]
    if not pending:
        st.success("All healed locators have been audited! No pending reviews awaiting promotion.")
    else:
        st.write(f"Found **{len(pending)}** healed locator(s) awaiting engineer approval.")
        for item in pending:
            score_val = (item.get("similarity_score") or 0.0) * 100
            with st.expander(f"Key: {item['target_key']} — Proposed: {item['healed_locator']} (Score: {score_val:.1f}%)", expanded=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**Target Key:**", f"`{item['target_key']}`")
                    st.write("**Original Failed Locator:**", f"`{item['original_locator']}`")
                    st.write("**Healed Discovered Locator:**", f"`{item['healed_locator']}`")
                with col_b:
                    st.write("**Confidence Score:**", f"{score_val:.1f}%")
                    st.write("**Repair Latency:**", f"{item.get('latency_ms', 0):.1f} ms")
                    st.write("**Recorded At:**", item.get("created_at", ""))

                btn_col1, btn_col2 = st.columns([1, 4])
                with btn_col1:
                    if st.button("✅ Approve & Promote to V2", key=f"app_{item['id']}"):
                        repo.promote_healed_locator(
                            target_key=item["target_key"],
                            new_locator=item["healed_locator"],
                            similarity_score=item["similarity_score"] or 0.0,
                            approved_by="qa_engineer_lead"
                        )
                        st.success(f"Promoted {item['target_key']} to active baseline v2!")
                        st.rerun()
                with btn_col2:
                    if st.button("❌ Reject Repair", key=f"rej_{item['id']}"):
                        repo.reject_healing_event(item["id"])
                        st.warning(f"Rejected healing event {item['id']}.")
                        st.rerun()

# =============================================================================
# TAB 4: Baseline Version Comparison
# =============================================================================
with tab4:
    st.subheader("Baseline Evolution & Version Comparison")
    all_fps = repo.get_all_active_fingerprints()
    if not all_fps:
        st.info("No active baseline fingerprints recorded.")
    else:
        target_keys = sorted(list(set(fp.target_key for fp in all_fps)))
        selected_key = st.selectbox("Select Target Key to inspect version evolution:", target_keys)

        versions = repo.get_fingerprint_versions(selected_key)
        if len(versions) == 1:
            st.write(f"Target key `{selected_key}` currently has **1 version** (Initial Baseline).")
            v1 = versions[0]
            st.json({
                "target_key": v1.target_key,
                "version": v1.version,
                "status": v1.status,
                "selector": v1.original_selector,
                "tag": v1.tag_name,
                "element_id": v1.element_id,
                "text": v1.inner_text,
                "classes": v1.class_list
            })
        else:
            st.write(f"Target key `{selected_key}` has **{len(versions)} versions** (Evolved over time).")
            v_cols = st.columns(len(versions))
            for i, ver in enumerate(versions):
                with v_cols[i]:
                    st.markdown(f"#### Version {ver.version} ({ver.status.upper()})")
                    st.write("**Selector:**", f"`{ver.original_selector}`")
                    st.write("**Tag:**", f"`{ver.tag_name}`")
                    st.write("**ID:**", f"`{ver.element_id or 'none'}`")
                    st.write("**Text:**", f"\"{ver.inner_text}\"")
                    st.write("**Classes:**", ver.class_list)

        st.markdown("### All Active Fingerprints in Repository")
        fp_rows = []
        for fp in all_fps:
            fp_rows.append({
                "Target Key": fp.target_key,
                "Version": fp.version,
                "Status": fp.status,
                "Tag": fp.tag_name,
                "ID": fp.element_id,
                "Text": fp.inner_text,
                "Active Selector": fp.original_selector,
                "Role": fp.aria_role,
            })
        st.dataframe(pd.DataFrame(fp_rows), use_container_width=True)

# =============================================================================
# TAB 5: Performance & Latency Analytics
# =============================================================================
with tab5:
    st.subheader("Performance Budget & Timeout Strategy Analytics")
    
    perf_file = Path("artifacts/reports/performance_profile.json")
    if perf_file.is_file():
        with open(perf_file, "r", encoding="utf-8") as f:
            profile_data = json.load(f)

        st.markdown("#### Multi-Tier Benchmark Latencies (500+ Iterations)")
        col_p1, col_p2, col_p3 = st.columns(3)
        algo_m = profile_data.get("pure_algorithm_scoring", {}).get("mean_ms", 0.69)
        dom_m = profile_data.get("dom_extraction", {}).get("mean_ms", 2.30)
        dec_m = profile_data.get("decision_engine", {}).get("mean_ms", 0.005)

        col_p1.metric("Pure Algorithm", f"{algo_m:.3f} ms", help="50 candidates scored across 6 dimensions")
        col_p2.metric("DOM Extraction", f"{dom_m:.3f} ms", help="In-browser JavaScript evaluation via page.evaluate")
        col_p3.metric("Decision Engine", f"{dec_m:.3f} ms", help="Confidence and margin gating")

        st.markdown("#### Browser Timeout Dominance Analysis")
        std_healing = profile_data.get("standard_healing_2500ms", {}).get("mean_ms", 3072.27)
        fast_healing = profile_data.get("fast_healing_1000ms", {}).get("mean_ms", 1572.06)

        col_t1, col_t2 = st.columns(2)
        col_t1.metric("Standard Healing (2500ms action timeout)", f"{std_healing:.1f} ms", "Default Safe Policy")
        col_t2.metric("Fast Healing (1000ms action timeout)", f"{fast_healing:.1f} ms", "-48.8% Latency Reduction")

        st.info("""
        **Latency Budget Takeaway**:
        The pure computation overhead (Algorithm + Decision + DOM scan) is only **~3.0 ms** (< 0.1% of total healing time).
        Playwright's action timeout (2,500 ms) and dynamic grace period (500 ms) account for **97.64%** of the full browser healing cycle.
        """)
    else:
        st.info("Run `python tests/evaluation/profile_performance.py` to generate detailed multi-tier latency benchmarks.")
