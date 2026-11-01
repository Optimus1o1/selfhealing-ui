import streamlit as st
import pandas as pd
import json
from pathlib import Path
from selfheal.database.connection import DatabaseManager
from selfheal.baseline.repository import BaselineRepository
from selfheal.config import SelfHealConfig

st.set_page_config(
    page_title="Self-Healing UI Automation Portal",
    page_icon="🛡️",
    layout="wide"
)

# Custom Moon Sanctum Labs Dark/Copper Theme styling
st.markdown("""
<style>
    .main { background-color: #0F1013; color: #F2EFE8; }
    h1, h2, h3 { color: #F2EFE8 !important; }
    .stMetric { background-color: #17191E; border: 1px solid #2A2D35; border-radius: 8px; padding: 12px; }
    .stButton>button { background-color: #E0A45C; color: #0F1013; font-weight: bold; border-radius: 6px; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_repo():
    config = SelfHealConfig.load_from_yaml("configs/default.yaml")
    db_mgr = DatabaseManager(config.framework.database_path)
    return BaselineRepository(db_mgr)


repo = get_repo()

st.title("🛡️ Self-Healing UI Automation Dashboard")
st.caption("Moon Sanctum Labs — *Decode. Build. Evolve.* | Deterministic Locator Recovery & Audit Portal")

stats = repo.get_run_statistics()
events = repo.get_healing_events()

# Top KPI Summary Cards
col1, col2, col3, col4, col5 = st.columns(5)
total_runs = stats.get("total_runs") or 0
total_events = len(events)
approved_events = [e for e in events if e.get("decision") == "APPROVED"]
healing_rate = (len(approved_events) / max(1, total_events)) * 100 if total_events > 0 else 0.0
avg_score = (stats.get("avg_score") or 0.0) * 100
avg_latency = stats.get("avg_latency") or 0.0

col1.metric("Total Test Runs", total_runs)
col2.metric("Healing Interceptions", total_events)
col3.metric("Healing Success Rate", f"{healing_rate:.1f}%")
col4.metric("Avg Confidence", f"{avg_score:.1f}%")
col5.metric("Avg Healing Latency", f"{avg_latency:.1f} ms")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Healing Events Feed",
    "⚖️ Audit & Review Portal",
    "🧬 Baseline Fingerprints",
    "📜 Locator Evolution History"
])

# Tab 1: Healing Events Feed
with tab1:
    st.subheader("Runtime Interceptions & Similarity Breakdown")
    if not events:
        st.info("No healing events recorded yet. Run a test against a modified UI to populate this feed.")
    else:
        df_events = pd.DataFrame(events)
        cols_to_show = [
            "id", "target_key", "original_locator", "healed_locator",
            "similarity_score", "decision", "status", "retry_success", "latency_ms", "created_at"
        ]
        available_cols = [c for c in cols_to_show if c in df_events.columns]
        st.dataframe(df_events[available_cols], use_container_width=True)

        st.markdown("### Selected Event Detail & Score Analysis")
        selected_id = st.selectbox("Select Event ID to inspect score breakdown:", df_events["id"].tolist())
        selected_row = next((e for e in events if e["id"] == selected_id), None)
        if selected_row and selected_row.get("score_breakdown_json"):
            breakdown = json.loads(selected_row["score_breakdown_json"])
            st.json(breakdown)

# Tab 2: Audit & Review Portal
with tab2:
    st.subheader("Assisted Mode: Pending Healed Locators")
    pending = [e for e in events if e.get("status") == "pending_review" and e.get("decision") == "APPROVED"]
    if not pending:
        st.success("All healed locators have been audited! No pending reviews.")
    else:
        st.write(f"Found **{len(pending)}** healed locator(s) awaiting engineer approval.")
        for item in pending:
            with st.expander(f"Key: {item['target_key']} (Score: {(item['similarity_score'] or 0)*100:.1f}%)", expanded=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**Original Locator:**", f"`{item['original_locator']}`")
                    st.write("**Healed Locator:**", f"`{item['healed_locator']}`")
                    st.write("**Reason:**", item.get("reason", ""))
                with col_b:
                    st.write("**Latency:**", f"{item.get('latency_ms', 0):.1f} ms")
                    st.write("**Timestamp:**", item.get("created_at", ""))

                btn_col1, btn_col2 = st.columns([1, 4])
                with btn_col1:
                    if st.button("✅ Approve & Promote", key=f"app_{item['id']}"):
                        repo.promote_healed_locator(
                            target_key=item["target_key"],
                            new_locator=item["healed_locator"],
                            similarity_score=item["similarity_score"] or 0.0,
                            approved_by="qa_engineer"
                        )
                        st.success(f"Promoted {item['target_key']} to active baseline!")
                        st.rerun()
                with btn_col2:
                    if st.button("❌ Reject Repair", key=f"rej_{item['id']}"):
                        repo.reject_healing_event(item["id"])
                        st.warning(f"Rejected healing event {item['id']}.")
                        st.rerun()

# Tab 3: Baseline Fingerprints
with tab3:
    st.subheader("Active Baseline Element Repository")
    fps = repo.get_all_active_fingerprints()
    if not fps:
        st.info("No active baseline fingerprints recorded. Execute a baseline run to record fingerprints.")
    else:
        fp_rows = []
        for fp in fps:
            fp_rows.append({
                "Target Key": fp.target_key,
                "Version": fp.version,
                "Status": fp.status,
                "Tag": fp.tag_name,
                "ID": fp.element_id,
                "Text": fp.inner_text,
                "Original Selector": fp.original_selector,
                "Role": fp.aria_role,
                "Page URL": fp.page_url
            })
        st.dataframe(pd.DataFrame(fp_rows), use_container_width=True)

# Tab 4: Locator History
with tab4:
    st.subheader("Historical Locator Evolution & Promotions")
    history = repo.get_locator_history()
    if not history:
        st.info("No promotions or manual overrides recorded yet.")
    else:
        st.dataframe(pd.DataFrame(history), use_container_width=True)
