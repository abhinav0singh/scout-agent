"""
pages/settings.py  —  Application settings page.
"""

import streamlit as st
from components.agent_reasoning_panel import html

C = {"t1": "#E2EDFF", "t2": "#7A92B0", "t3": "#3D5270",
     "s1": "#09101C", "s2": "#0D1525", "b1": "#192437",
     "green": "#00E87D", "amber": "#FF8C00"}


def render_settings() -> None:
    st.markdown("""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
      padding:16px;margin-bottom:14px;">
      <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
        color:#E2EDFF;margin-bottom:16px;">⚙ Application Settings</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div style="font-size:10px;color:#3D5270;text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px;">Backend API URL</div>', unsafe_allow_html=True)
        api_url = st.text_input("API URL", value=st.session_state.get("settings_api_url", "http://localhost:8000"), label_visibility="collapsed", key="set_api_url")
        st.session_state.settings_api_url = api_url

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:10px;color:#3D5270;text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px;">Data Source</div>', unsafe_allow_html=True)
        use_mock = st.toggle("Use Mock Data (Demo Mode)", value=st.session_state.get("settings_use_mock", True), key="set_mock")
        st.session_state.settings_use_mock = use_mock

        if use_mock:
            st.markdown('<div style="padding:8px 10px;background:#09101C;border-radius:6px;border-left:2px solid #00E87D;margin-top:8px;font-size:11px;color:#3D5270;">Mock data active — all pages show realistic sample data. Toggle off to connect to live backend.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="font-size:10px;color:#3D5270;text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px;">Show Agent Traces</div>', unsafe_allow_html=True)
        show_traces = st.toggle("Show agent reasoning in Scout & Dashboard", value=True, key="set_traces")
        st.session_state.settings_show_traces = show_traces

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:10px;color:#3D5270;text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px;">Club Profile</div>', unsafe_allow_html=True)
        club = st.session_state.get("club_profile", {})
        new_club = st.text_input("Club Name", value=club.get("name", "FC Southampton"), key="set_club")
        if new_club != club.get("name"):
            st.session_state.club_profile["name"] = new_club

    st.markdown("</div>", unsafe_allow_html=True)

    # System status
    st.markdown("""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:16px;">
      <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:#E2EDFF;margin-bottom:12px;">System Status</div>
    """, unsafe_allow_html=True)

    statuses = [
        ("Streamlit Frontend", "Running", "green"),
        ("Backend API",        "Mock Mode" if st.session_state.get("settings_use_mock", True) else "Connected", "amber" if st.session_state.get("settings_use_mock", True) else "green"),
        ("MongoDB",            "Not Connected", "t3"),
        ("Vector Store",       "Not Connected", "t3"),
        ("StatsBomb API",      "Mock", "amber"),
        ("Transfermarkt API",  "Mock", "amber"),
        ("LLM (Claude 3.5)",   "Ready", "green"),
    ]

    for name, status, color_key in statuses:
        c = C.get(color_key, C["t3"])
        dot_color = c if color_key not in ("t3",) else C["t3"]
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #192437;">
          <span style="font-size:12px;color:#7A92B0;">{name}</span>
          <div style="display:flex;align-items:center;gap:6px;">
            <div style="width:6px;height:6px;border-radius:50%;background:{dot_color};"></div>
            <span style="font-size:11px;font-weight:600;color:{c};">{status}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)