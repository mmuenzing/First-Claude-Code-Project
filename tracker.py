import streamlit as st
from data import (
    load_data, save_data, update_initiative,
    add_goal, update_goal, delete_goal,
)

st.set_page_config(page_title="MentorMike — AI Resolution Tracker", layout="wide", page_icon="🔴")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

    :root {
        --ace-red:      #CC0000;
        --ace-red-glow: rgba(204, 0, 0, 0.45);
        --ace-red-dim:  rgba(204, 0, 0, 0.15);
        --glass-bg:     rgba(255, 255, 255, 0.10);
        --glass-border: rgba(255, 255, 255, 0.22);
        --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        --text-primary: #ffffff;
        --text-muted:   rgba(255, 255, 255, 0.65);
    }

    /* ── Deep space gradient background ── */
    .stApp, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0d0d0d 0%, #1a0000 40%, #0a0a1a 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stMain"], [data-testid="block-container"] {
        background: transparent !important;
    }

    /* ── Sidebar — frosted glass on dark red ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(140,0,0,0.85) 0%, rgba(80,0,0,0.95) 100%) !important;
        backdrop-filter: blur(18px) !important;
        -webkit-backdrop-filter: blur(18px) !important;
        border-right: 1px solid rgba(204,0,0,0.3) !important;
        box-shadow: 4px 0 24px rgba(204,0,0,0.2) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text-primary) !important; }
    [data-testid="stSidebar"] .stRadio label {
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        transition: color 0.2s ease !important;
    }

    /* ── Text white on dark bg — specific containers only ── */
    .stApp p,
    .stApp label,
    .stApp li,
    .stApp td,
    .stApp th,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stText"] p,
    [data-testid="stCaptionContainer"] p {
        color: rgba(255,255,255,0.88) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Selectbox trigger ── */
    [data-testid="stSelectbox"] > div > div,
    [data-baseweb="select"] > div {
        background: rgba(15, 0, 0, 0.80) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
        color: white !important;
    }

    /* ── Dropdown popover ── */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [role="listbox"] {
        background: #1c0000 !important;
        border: 1px solid rgba(204,0,0,0.35) !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.6) !important;
    }

    /* ── Dropdown options ── */
    [role="option"],
    [role="option"] * {
        color: rgba(255,255,255,0.88) !important;
        background: transparent !important;
        visibility: visible !important;
    }
    [role="option"]:hover,
    [aria-selected="true"][role="option"] {
        background: rgba(204,0,0,0.25) !important;
        color: white !important;
    }

    [data-baseweb="tag"] { background: rgba(204,0,0,0.3) !important; }
    [data-baseweb="tag"] span { color: white !important; }

    /* ── Number input — fix internal button text ── */
    [data-testid="stNumberInput"] button {
        background: rgba(255,255,255,0.08) !important;
        border-color: rgba(255,255,255,0.18) !important;
        color: white !important;
    }
    [data-testid="stNumberInput"] button:hover {
        background: rgba(204,0,0,0.25) !important;
    }

    /* ── Headings with red glow ── */
    h1 {
        color: #ffffff !important;
        font-weight: 900 !important;
        letter-spacing: -0.5px !important;
        text-shadow: 0 0 30px var(--ace-red-glow), 0 0 60px rgba(204,0,0,0.2) !important;
    }
    h2, h3 {
        color: rgba(255,255,255,0.95) !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px !important;
    }

    /* ── Glass metric cards ── */
    [data-testid="stMetric"] {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        box-shadow: var(--glass-shadow), inset 0 1px 0 rgba(255,255,255,0.1) !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease !important;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.45), 0 0 20px var(--ace-red-dim) !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--ace-red) !important;
        font-weight: 900 !important;
        font-size: 2rem !important;
        text-shadow: 0 0 20px var(--ace-red-glow) !important;
    }
    [data-testid="stMetricLabel"] { color: var(--text-muted) !important; }

    /* ── Progress bar — glowing red ── */
    [data-testid="stProgressBar"] > div {
        background: rgba(255,255,255,0.08) !important;
        border-radius: 99px !important;
    }
    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #990000, #CC0000, #ff3333) !important;
        border-radius: 99px !important;
        box-shadow: 0 0 12px var(--ace-red-glow) !important;
    }

    /* ── Glass expander headers ── */
    [data-testid="stExpander"] {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 14px !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        box-shadow: var(--glass-shadow) !important;
        margin-bottom: 10px !important;
        transition: box-shadow 0.25s ease !important;
        overflow: hidden !important;
    }
    [data-testid="stExpander"]:hover {
        box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(204,0,0,0.3) !important;
    }
    [data-testid="stExpander"] summary {
        background: transparent !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 14px 18px !important;
        border-radius: 14px !important;
        letter-spacing: 0.3px !important;
    }

    /* ── Glass form cards ── */
    [data-testid="stForm"] {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.14) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important;
    }

    /* ── Widget labels (text above each input) ── */
    [data-testid="stWidgetLabel"] *,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p {
        color: rgba(255,255,255,0.75) !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    /* ── Text inputs — solid dark bg so white text is always visible ── */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stNumberInput"] input {
        background: rgba(15, 0, 0, 0.80) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        caret-color: var(--ace-red) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stNumberInput"] input:focus {
        border-color: var(--ace-red) !important;
        box-shadow: 0 0 0 3px var(--ace-red-dim), 0 0 16px rgba(204,0,0,0.2) !important;
        outline: none !important;
    }
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stTextArea"] textarea::placeholder {
        color: rgba(255,255,255,0.35) !important;
    }


    /* ── Number input stepper container ── */
    [data-testid="stNumberInput"] > div {
        background: transparent !important;
        border: none !important;
    }

    /* ── Buttons — glowing red pill ── */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(135deg, #CC0000, #990000) !important;
        color: white !important;
        border: 1px solid rgba(255,80,80,0.3) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 15px rgba(204,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.15) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #e60000, #CC0000) !important;
        box-shadow: 0 6px 24px rgba(204,0,0,0.6), 0 0 20px rgba(204,0,0,0.3) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active, .stFormSubmitButton > button:active {
        transform: translateY(0px) !important;
    }

    /* ── Info / success / warning alerts — glass ── */
    [data-testid="stAlert"] {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(8px) !important;
    }

    /* ── Dividers ── */
    hr { border-color: rgba(255,255,255,0.1) !important; }

    /* ── Caption text ── */
    [data-testid="stCaptionContainer"] p { color: var(--text-muted) !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
    ::-webkit-scrollbar-thumb {
        background: rgba(204,0,0,0.5);
        border-radius: 99px;
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--ace-red); }
</style>
""", unsafe_allow_html=True)

# Sidebar branding
st.sidebar.markdown("""
<div style="text-align:center; padding: 20px 0 28px 0;">
    <div style="
        display:inline-block;
        width:54px; height:54px; line-height:54px;
        background: linear-gradient(135deg,#CC0000,#660000);
        border-radius:14px;
        font-size:1.6rem;
        box-shadow: 0 0 24px rgba(204,0,0,0.6), inset 0 1px 0 rgba(255,120,120,0.3);
        margin-bottom:12px;
    ">🔧</div>
    <div style="font-size:1.1rem; font-weight:900; color:white; letter-spacing:2px; text-transform:uppercase;">MentorMike</div>
    <div style="font-size:0.7rem; color:rgba(255,255,255,0.55); margin-top:4px; letter-spacing:1.5px; text-transform:uppercase;">AI Resolution Tracker</div>
    <div style="height:1px; background:rgba(255,255,255,0.12); margin:16px 12px 0 12px;"></div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio("", ["Dashboard", "Initiatives", "Goals"])

STATUS_OPTIONS = ["not_started", "in_progress", "completed"]
STATUS_LABELS = {"not_started": "Not Started", "in_progress": "In Progress", "completed": "Complete"}
STATUS_ICONS = {"not_started": "⬜", "in_progress": "🔵", "completed": "✅"}
PRIORITY_LABELS = {1: "1 — Critical", 2: "2 — High", 3: "3 — Medium", 4: "4 — Low", 5: "5 — Optional"}

data = load_data()

# ── Dashboard ──────────────────────────────────────────────────────────────────
if page == "Dashboard":
    st.title("Resolution Tracker — Dashboard")

    initiatives = data["initiatives"]
    goals = data["goals"]

    completed = sum(1 for i in initiatives if i["status"] == "completed")
    in_progress = sum(1 for i in initiatives if i["status"] == "in_progress")
    total_hours = sum(i["time_spent_hours"] for i in initiatives)
    active_goals = sum(1 for g in goals if g["status"] == "active")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Weeks Completed", f"{completed} / 10")
    c2.metric("In Progress", in_progress)
    c3.metric("Total Hours", f"{total_hours:.1f}")
    c4.metric("Active Goals", active_goals)

    st.progress(completed / 10)
    st.caption(f"{completed} of 10 initiatives completed — MentorMike 10-Week Program")

    st.subheader("All Initiatives")
    header = st.columns([1, 3, 2, 2, 2, 2])
    for col, label in zip(header, ["Week", "Title", "Status", "Started", "Completed", "Hours"]):
        col.markdown(f"**{label}**")

    for init in initiatives:
        row = st.columns([1, 3, 2, 2, 2, 2])
        row[0].write(f"Week {init['week']}")
        row[1].write(init["title"])
        row[2].write(f"{STATUS_ICONS[init['status']]} {STATUS_LABELS[init['status']]}")
        row[3].write(init["start_date"] or "—")
        row[4].write(init["end_date"] or "—")
        row[5].write(f"{init['time_spent_hours']:.1f}h")

# ── Initiatives ────────────────────────────────────────────────────────────────
elif page == "Initiatives":
    st.title("10-Week Initiatives")

    for init in data["initiatives"]:
        label = f"{STATUS_ICONS[init['status']]}  Week {init['week']}: {init['title']}"
        with st.expander(label, expanded=init["status"] == "in_progress"):
            with st.form(key=f"init_{init['id']}"):
                title = st.text_input("Title", value=init["title"])
                status = st.radio(
                    "Status",
                    STATUS_OPTIONS,
                    index=STATUS_OPTIONS.index(init["status"]),
                    format_func=lambda s: STATUS_LABELS[s],
                    horizontal=True,
                    key=f"status_{init['id']}",
                )
                col1, col2 = st.columns(2)
                start_date = col1.text_input("Date Started (YYYY-MM-DD)", value=init["start_date"])
                end_date = col2.text_input("Date Completed (YYYY-MM-DD)", value=init["end_date"])
                time_spent = st.number_input(
                    "Time Spent (hours)", min_value=0.0, step=0.5,
                    value=float(init["time_spent_hours"]),
                )
                summary = st.text_area("Summary / Results", value=init["summary"], height=150)

                if st.form_submit_button("Save"):
                    update_initiative(
                        data, init["id"],
                        title=title, status=status,
                        start_date=start_date, end_date=end_date,
                        time_spent_hours=time_spent, summary=summary,
                    )
                    save_data(data)
                    st.success("Saved!")
                    st.rerun()

# ── Goals ──────────────────────────────────────────────────────────────────────
elif page == "Goals":
    st.title("Goals")

    with st.expander("Add New Goal", expanded=len(data["goals"]) == 0):
        with st.form("add_goal"):
            title = st.text_input("Goal Title")
            description = st.text_area("Description")
            priority = st.selectbox("Priority", [1, 2, 3, 4, 5], format_func=lambda p: PRIORITY_LABELS[p])
            if st.form_submit_button("Add Goal"):
                if title.strip():
                    add_goal(data, title.strip(), description.strip(), priority)
                    save_data(data)
                    st.success("Goal added!")
                    st.rerun()
                else:
                    st.warning("Please enter a goal title.")

    goals = sorted(data["goals"], key=lambda g: g["priority"])

    if not goals:
        st.info("No goals yet. Add your first goal above.")
    else:
        st.subheader("Goals by Priority")
        for goal in goals:
            cols = st.columns([4, 2, 1, 1])
            desc = f"\n_{goal['description']}_" if goal["description"] else ""
            cols[0].markdown(f"**{goal['title']}**{desc}")
            cols[1].write(PRIORITY_LABELS[goal["priority"]])
            cols[2].write("✅ Done" if goal["status"] == "completed" else "🔵 Active")

            toggle_label = "Mark Done" if goal["status"] == "active" else "Reopen"
            if cols[3].button(toggle_label, key=f"toggle_{goal['id']}"):
                new_status = "completed" if goal["status"] == "active" else "active"
                update_goal(data, goal["id"], status=new_status)
                save_data(data)
                st.rerun()

            with st.expander(f"Edit / Delete — {goal['title']}"):
                with st.form(key=f"edit_{goal['id']}"):
                    new_title = st.text_input("Title", value=goal["title"])
                    new_desc = st.text_area("Description", value=goal["description"])
                    new_priority = st.selectbox(
                        "Priority", [1, 2, 3, 4, 5],
                        index=goal["priority"] - 1,
                        format_func=lambda p: PRIORITY_LABELS[p],
                    )
                    save_col, del_col = st.columns(2)
                    if save_col.form_submit_button("Save Changes"):
                        update_goal(data, goal["id"], title=new_title, description=new_desc, priority=new_priority)
                        save_data(data)
                        st.success("Updated!")
                        st.rerun()
                    if del_col.form_submit_button("Delete Goal"):
                        delete_goal(data, goal["id"])
                        save_data(data)
                        st.rerun()
