import streamlit as st
import pandas as pd
from datetime import datetime
from hybrid_agent import hybrid_agent

st.set_page_config(
    page_title="Agentic HR Operating System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if "messages" not in st.session_state:
    st.session_state.messages = []

if "employee_name" not in st.session_state:
    st.session_state.employee_name = ""

if "leave_balance" not in st.session_state:
    st.session_state.leave_balance = {"Casual": 12, "Sick": 10, "Earned": 15}

if "leaves_taken" not in st.session_state:
    st.session_state.leaves_taken = {"Casual": 0, "Sick": 0, "Earned": 0}

if "query_log" not in st.session_state:
    st.session_state.query_log = []


def log_query(name, query, response_type):
    st.session_state.query_log.append({
        "Employee": name if name else "Anonymous",
        "Query": query,
        "Type": response_type,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


dark = st.session_state.dark_mode

bg = "#0d1117" if dark else "#f7f7f8"
sidebar_bg = "#161b22" if dark else "#ffffff"
user_bg = "#2f81f7" if dark else "#2563eb"
bot_bg = "#21262d" if dark else "#ffffff"
bot_border = "#30363d" if dark else "#e5e7eb"
text_main = "#e6edf3" if dark else "#111827"
text_muted = "#8b949e" if dark else "#6b7280"
input_bg = "#161b22" if dark else "#ffffff"
input_border = "#30363d" if dark else "#d1d5db"

st.markdown(f"""
<style>
.stApp {{ background: {bg}; }}
section[data-testid="stSidebar"] {{ background: {sidebar_bg}; }}
section[data-testid="stSidebar"] * {{ color: {text_main} !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}

.chat-container {{
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem 1rem 6rem 1rem;
}}

.hero-card {{
    background: linear-gradient(135deg, rgba(47,129,247,0.16), rgba(167,139,250,0.12));
    border: 1px solid {bot_border};
    border-radius: 18px;
    padding: 30px;
    margin: 22px auto 24px;
    color: {text_main};
    text-align: center;
}}

.hero-card h1 {{
    font-size: 2.2rem;
    margin-bottom: 0.4rem;
}}

.hero-card p {{
    color: {text_muted};
    font-size: 1rem;
    line-height: 1.6;
}}

.agent-strip {{
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 16px;
}}

.agent-pill {{
    border: 1px solid {bot_border};
    background: {'#161b22' if dark else '#ffffff'};
    border-radius: 999px;
    padding: 7px 12px;
    font-size: 12px;
    color: {text_main};
}}

.msg-row {{
    display: flex;
    margin-bottom: 1.5rem;
    gap: 12px;
    align-items: flex-start;
}}

.msg-row.user {{
    flex-direction: row-reverse;
}}

.avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: 600;
    flex-shrink: 0;
}}

.avatar.user {{
    background: {user_bg};
    color: #fff;
}}

.avatar.bot {{
    background: {'#21262d' if dark else '#f3f4f6'};
    color: {text_main};
    border: 1px solid {bot_border};
}}

.bubble {{
    max-width: 78%;
    padding: 13px 16px;
    border-radius: 18px;
    font-size: 15px;
    line-height: 1.6;
    color: {text_main};
    white-space: pre-wrap;
}}

.bubble.user {{
    background: {user_bg};
    color: #fff;
    border-radius: 18px 4px 18px 18px;
}}

.bubble.bot {{
    background: {bot_bg};
    color: {text_main};
    border: 1px solid {bot_border};
    border-radius: 4px 18px 18px 18px;
}}

.badge {{
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 9px;
    border-radius: 20px;
    margin-bottom: 8px;
    letter-spacing: 0.4px;
}}

.badge.RAG {{ background: #1f6feb; color: #58a6ff; }}
.badge.MCP {{ background: #1a472a; color: #3fb950; }}
.badge.HYBRID {{ background: #4c1d95; color: #a78bfa; }}
.badge.ONBOARDING {{ background: #2d333b; color: #f0b429; }}
.badge.UNKNOWN {{ background: #3d1f00; color: #d29922; }}

.stChatInput > div {{
    background: {input_bg} !important;
    border: 1px solid {input_border} !important;
    border-radius: 12px !important;
}}

.stChatInput textarea {{
    color: {text_main} !important;
    background: transparent !important;
}}

.leave-card {{
    background: {'#21262d' if dark else '#f3f4f6'};
    border: 1px solid {bot_border};
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 8px;
}}

.leave-label {{
    font-size: 12px;
    color: {text_muted};
    margin-bottom: 4px;
}}

.leave-bar-bg {{
    background: {'#30363d' if dark else '#e5e7eb'};
    border-radius: 4px;
    height: 6px;
}}

.leave-bar-fill {{
    height: 6px;
    border-radius: 4px;
}}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🤖 Agentic HR OS")
    st.caption("RAG + MCP + Agent Router")
    st.divider()

    toggle_label = "☀️ Light Mode" if dark else "🌙 Dark Mode"
    if st.button(toggle_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.divider()

    st.markdown("**👤 Employee**")
    name_input = st.text_input(
        "Your name",
        value=st.session_state.employee_name,
        placeholder="e.g. Kshiti",
        label_visibility="collapsed"
    )

    if name_input:
        st.session_state.employee_name = name_input
        st.success(f"Hello, {name_input}! 👋")

    st.divider()

    st.markdown("**📅 Leave Balance**")
    for leave_type, total_leave in st.session_state.leave_balance.items():
        taken = st.session_state.leaves_taken[leave_type]
        remaining = total_leave - taken
        pct = int((remaining / total_leave) * 100)
        color = "#3fb950" if pct > 50 else "#d29922" if pct > 20 else "#f85149"

        st.markdown(f"""
        <div class="leave-card">
            <div class="leave-label">{leave_type} Leave — {remaining}/{total_leave} days left</div>
            <div class="leave-bar-bg">
                <div class="leave-bar-fill" style="width:{pct}%; background:{color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("**📊 Agent Analytics**")

    total = len(st.session_state.query_log)
    rag_count = sum(1 for q in st.session_state.query_log if q["Type"] == "RAG")
    mcp_count = sum(1 for q in st.session_state.query_log if q["Type"] == "MCP")
    hybrid_count = sum(1 for q in st.session_state.query_log if q["Type"] == "HYBRID")
    onboarding_count = sum(1 for q in st.session_state.query_log if q["Type"] == "ONBOARDING")
    unknown_count = sum(1 for q in st.session_state.query_log if q["Type"] == "UNKNOWN")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Total", total)
        st.metric("Policy", rag_count)
        st.metric("Onboarding", onboarding_count)
    with c2:
        st.metric("Actions", mcp_count)
        st.metric("Decision", hybrid_count)

    if unknown_count:
        st.caption(f"General support queries: {unknown_count}")

    st.divider()

    st.markdown("**📋 HR Query Log**")
    if st.session_state.query_log:
        df = pd.DataFrame(st.session_state.query_log)
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Log as CSV",
            data=csv,
            file_name=f"agentic_hr_query_log_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.caption("No queries yet. Employee interactions will appear here.")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.query_log = []
        st.rerun()

    st.divider()
    st.markdown(
        f"<span style='font-size:12px; color:{text_muted}'>FAISS · HuggingFace · FastMCP · LangChain · Streamlit</span>",
        unsafe_allow_html=True
    )

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

badge_icons = {
    "RAG": "📚 Policy Retrieval Agent",
    "MCP": "⚙️ Leave Action Agent",
    "HYBRID": "🧠 Compliance Decision Agent",
    "ONBOARDING": "📋 Employee Onboarding Agent",
    "UNKNOWN": "💬 HR Support Agent"
}

if not st.session_state.messages:
    total = len(st.session_state.query_log)
    rag_count = sum(1 for q in st.session_state.query_log if q["Type"] == "RAG")
    mcp_count = sum(1 for q in st.session_state.query_log if q["Type"] == "MCP")
    hybrid_count = sum(1 for q in st.session_state.query_log if q["Type"] == "HYBRID")
    onboarding_count = sum(1 for q in st.session_state.query_log if q["Type"] == "ONBOARDING")

    st.markdown("""
    <div class="hero-card">
        <h1>🤖 Agentic HR Operating System</h1>
        <p>
            Multi-Agent HR Automation using RAG, MCP Tool Calling,
            Compliance Intelligence, Employee Onboarding, and HR Analytics.
        </p>
        <div class="agent-strip">
            <span class="agent-pill">📚 Policy Retrieval Agent</span>
            <span class="agent-pill">⚙️ Leave Action Agent</span>
            <span class="agent-pill">🧠 Compliance Decision Agent</span>
            <span class="agent-pill">📋 Employee Onboarding Agent</span>
            <span class="agent-pill">📊 HR Analytics Layer</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Queries", total)
    col2.metric("Policy Agent", rag_count)
    col3.metric("Leave Actions", mcp_count)
    col4.metric("Compliance", hybrid_count)
    col5.metric("Onboarding", onboarding_count)

    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(2)

    suggestions = [
        "What is the leave policy?",
        "How many casual leaves do I get?",
        "Can I take emergency leave today?",
        "I am joining next Monday, what should I do?",
        f"Apply leave for {st.session_state.employee_name or 'Employee'}",
        "Should my leave be approved?",
    ]

    for i, s in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(s, use_container_width=True, key=f"chip_{i}"):
                st.session_state.messages.append({"role": "user", "content": s})

                result = hybrid_agent(s)
                rtype = result.get("type", "UNKNOWN")

                if rtype == "HYBRID":
                    reply = f"**Policy Info:**\n\n{result.get('rag', '')}\n\n💡 {result.get('action_suggestion', '')}"
                else:
                    reply = result.get(
                        "response",
                        "I can help with HR policy, onboarding, compliance, or leave management."
                    )

                st.session_state.messages.append({"role": "assistant", "content": reply, "type": rtype})
                log_query(st.session_state.employee_name, s, rtype)

                if rtype == "MCP" and "apply" in s.lower():
                    st.session_state.leaves_taken["Casual"] = min(
                        st.session_state.leaves_taken["Casual"] + 1,
                        st.session_state.leave_balance["Casual"]
                    )

                st.rerun()

else:
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        msg_type = msg.get("type", "")

        if role == "user":
            initials = st.session_state.employee_name[:1].upper() if st.session_state.employee_name else "U"

            st.markdown(f"""
            <div class="msg-row user">
                <div class="avatar user">{initials}</div>
                <div class="bubble user">{content}</div>
            </div>
            """, unsafe_allow_html=True)

        else:
            badge_text = badge_icons.get(msg_type, "")
            badge_html = f'<div class="badge {msg_type}">{badge_text}</div>' if badge_text else ""

            st.markdown(f"""
            <div class="msg-row bot">
                <div class="avatar bot">🤖</div>
                <div class="bubble bot">{badge_html}<div style="margin-top:6px;"></div>{content}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

if query := st.chat_input("Ask about HR policy, onboarding, compliance, or apply for leave..."):
    st.session_state.messages.append({"role": "user", "content": query})

    result = hybrid_agent(query)
    rtype = result.get("type", "UNKNOWN")

    if rtype == "HYBRID":
        reply = f"Policy Info:\n\n{result.get('rag', '')}\n\n💡 {result.get('action_suggestion', '')}"

    else:
        reply = result.get(
            "response",
            "I can help with HR policy, onboarding, compliance, or leave management."
        )

    st.session_state.messages.append({"role": "assistant", "content": reply, "type": rtype})
    log_query(st.session_state.employee_name, query, rtype)

    if rtype == "MCP" and "apply" in query.lower():
        st.session_state.leaves_taken["Casual"] = min(
            st.session_state.leaves_taken["Casual"] + 1,
            st.session_state.leave_balance["Casual"]
        )

    st.rerun()