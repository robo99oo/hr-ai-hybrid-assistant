import streamlit as st
from hybrid_agent import hybrid_agent

st.set_page_config(
    page_title="HR AI Hybrid Assistant",
    page_icon="🤖",
    layout="wide"
)

# ── Theme toggle ──────────────────────────────────────────────────────────────
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

dark = st.session_state.dark_mode

# ── CSS ───────────────────────────────────────────────────────────────────────
bg        = "#0d1117" if dark else "#f7f7f8"
sidebar_bg= "#161b22" if dark else "#ffffff"
user_bg   = "#2f81f7" if dark else "#2563eb"
bot_bg    = "#21262d" if dark else "#ffffff"
bot_border= "#30363d" if dark else "#e5e7eb"
text_main = "#e6edf3" if dark else "#111827"
text_muted= "#8b949e" if dark else "#6b7280"
input_bg  = "#161b22" if dark else "#ffffff"
input_border="#30363d" if dark else "#d1d5db"
badge_rag = ("#1f6feb","#58a6ff") if dark else ("#dbeafe","#1d4ed8")
badge_mcp = ("#1a472a","#3fb950") if dark else ("#dcfce7","#15803d")
badge_hyb = ("#4c1d95","#a78bfa") if dark else ("#ede9fe","#7c3aed")
badge_unk = ("#3d1f00","#d29922") if dark else ("#fef3c7","#b45309")

st.markdown(f"""
<style>
  /* Global */
  .stApp {{ background: {bg}; }}
  section[data-testid="stSidebar"] {{ background: {sidebar_bg}; }}
  section[data-testid="stSidebar"] * {{ color: {text_main} !important; }}

  /* Hide default streamlit elements */
  #MainMenu, footer, header {{ visibility: hidden; }}
  .block-container {{ padding: 0 !important; max-width: 100% !important; }}

  /* Chat area */
  .chat-container {{
    max-width: 780px;
    margin: 0 auto;
    padding: 2rem 1rem 6rem 1rem;
  }}

  /* Message bubbles */
  .msg-row {{ display: flex; margin-bottom: 1.5rem; gap: 12px; align-items: flex-start; }}
  .msg-row.user {{ flex-direction: row-reverse; }}

  .avatar {{
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; font-weight: 600; flex-shrink: 0;
  }}
  .avatar.user {{ background: {user_bg}; color: #fff; }}
  .avatar.bot  {{ background: {'#21262d' if dark else '#f3f4f6'}; color: {text_main}; border: 1px solid {bot_border}; }}

  .bubble {{
    max-width: 75%; padding: 12px 16px;
    border-radius: 18px; font-size: 15px; line-height: 1.6;
    color: {text_main};
  }}
  .bubble.user {{
    background: {user_bg}; color: #fff;
    border-radius: 18px 4px 18px 18px;
  }}
  .bubble.bot {{
    background: {bot_bg}; color: {text_main};
    border: 1px solid {bot_border};
    border-radius: 4px 18px 18px 18px;
  }}

  /* Badge */
  .badge {{
    display: inline-block; font-size: 11px; font-weight: 600;
    padding: 2px 8px; border-radius: 20px; margin-bottom: 6px; letter-spacing: 0.5px;
  }}
  .badge.RAG   {{ background: {badge_rag[0]}; color: {badge_rag[1]}; }}
  .badge.MCP   {{ background: {badge_mcp[0]}; color: {badge_mcp[1]}; }}
  .badge.HYBRID{{ background: {badge_hyb[0]}; color: {badge_hyb[1]}; }}
  .badge.UNKNOWN{{ background: {badge_unk[0]}; color: {badge_unk[1]}; }}

  /* Welcome screen */
  .welcome {{
    text-align: center; padding: 4rem 1rem 2rem;
    color: {text_muted};
  }}
  .welcome h1 {{ font-size: 2rem; font-weight: 700; color: {text_main}; margin-bottom: 0.5rem; }}
  .welcome p  {{ font-size: 1rem; margin-bottom: 2rem; }}

  /* Suggestion chips */
  .chips {{ display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 1rem; }}

  /* Input bar */
  .stChatInput > div {{ background: {input_bg} !important; border: 1px solid {input_border} !important; border-radius: 12px !important; }}
  .stChatInput textarea {{ color: {text_main} !important; background: transparent !important; }}

  /* Sidebar cards */
  .leave-card {{
    background: {'#21262d' if dark else '#f3f4f6'};
    border: 1px solid {bot_border};
    border-radius: 10px; padding: 10px 14px; margin-bottom: 8px;
  }}
  .leave-label {{ font-size: 12px; color: {text_muted}; margin-bottom: 4px; }}
  .leave-bar-bg {{ background: {'#30363d' if dark else '#e5e7eb'}; border-radius: 4px; height: 6px; }}
  .leave-bar-fill {{ height: 6px; border-radius: 4px; }}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 HR AI Assistant")
    st.divider()

    # Theme toggle
    toggle_label = "☀️ Light Mode" if dark else "🌙 Dark Mode"
    if st.button(toggle_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.divider()

    # Employee login
    st.markdown("**👤 Employee**")
    name_input = st.text_input("Your name", value=st.session_state.employee_name,
                                placeholder="e.g. Aman", label_visibility="collapsed")
    if name_input:
        st.session_state.employee_name = name_input
        st.success(f"Hello, {name_input}! 👋")

    st.divider()

    # Leave balance tracker
    st.markdown("**📅 Leave Balance**")
    total_taken = 0
    for leave_type, total in st.session_state.leave_balance.items():
        taken = st.session_state.leaves_taken[leave_type]
        remaining = total - taken
        total_taken += taken
        pct = int((remaining / total) * 100)
        color = "#3fb950" if pct > 50 else "#d29922" if pct > 20 else "#f85149"
        st.markdown(f"""
        <div class="leave-card">
          <div class="leave-label">{leave_type} Leave — {remaining}/{total} days left</div>
          <div class="leave-bar-bg">
            <div class="leave-bar-fill" style="width:{pct}%; background:{color};"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown(f"<span style='font-size:12px; color:{text_muted}'>FAISS · HuggingFace · FastMCP · LangChain</span>", unsafe_allow_html=True)

# ── Main chat area ─────────────────────────────────────────────────────────────
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

badge_icons = {"RAG": "🔍 Policy Retrieval", "MCP": "⚙️ Action", "HYBRID": "🔀 Hybrid", "UNKNOWN": "❓ General"}

if not st.session_state.messages:
    name_display = st.session_state.employee_name or "there"
    st.markdown(f"""
    <div class="welcome">
      <h1>Hi {name_display}! 👋</h1>
      <p>I'm your HR AI Assistant. Ask me anything about leave policies<br>or let me help you apply for leave.</p>
    </div>
    """, unsafe_allow_html=True)

    # Suggestion chips as buttons
    st.markdown("<div style='max-width:780px; margin:0 auto;'>", unsafe_allow_html=True)
    cols = st.columns(2)
    suggestions = [
        "What is the leave policy?",
        "How many casual leaves do I get?",
        f"Apply leave for {st.session_state.employee_name or 'Aman'}",
        "Can I take leave tomorrow?",
    ]
    for i, s in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(s, use_container_width=True, key=f"chip_{i}"):
                st.session_state.messages.append({"role": "user", "content": s})
                result = hybrid_agent(s)
                rtype = result.get("type", "UNKNOWN")
                if rtype == "HYBRID":
                    reply = f"**Policy Info:**\n\n{result['rag']}\n\n💡 {result['action_suggestion']}"
                else:
                    reply = result.get("response", "I can help with HR policy or leave management.")
                st.session_state.messages.append({"role": "assistant", "content": reply, "type": rtype})
                # Update leave balance if MCP action
                if rtype == "MCP" and "apply" in s.lower():
                    st.session_state.leaves_taken["Casual"] = min(
                        st.session_state.leaves_taken["Casual"] + 1,
                        st.session_state.leave_balance["Casual"]
                    )
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Render chat history
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        msg_type = msg.get("type", "")

        if role == "user":
            initials = (st.session_state.employee_name[:1].upper()
                        if st.session_state.employee_name else "U")
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
              <div class="bubble bot">{badge_html}{content}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────────
if query := st.chat_input("Ask about HR policy or apply for leave..."):
    st.session_state.messages.append({"role": "user", "content": query})

    result = hybrid_agent(query)
    rtype = result.get("type", "UNKNOWN")

    if rtype == "HYBRID":
        reply = f"**Policy Info:**\n\n{result['rag']}\n\n💡 {result['action_suggestion']}"
    else:
        reply = result.get("response", "I can help with HR policy or leave management.")

    st.session_state.messages.append({"role": "assistant", "content": reply, "type": rtype})

    # Update leave balance on apply
    if rtype == "MCP" and "apply" in query.lower():
        st.session_state.leaves_taken["Casual"] = min(
            st.session_state.leaves_taken["Casual"] + 1,
            st.session_state.leave_balance["Casual"]
        )

    st.rerun()