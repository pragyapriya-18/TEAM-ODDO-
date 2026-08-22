# Run with:
   # py -m streamlit run dashboard.py

import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# --------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="TEAM ODDO HRMS - Dashboard",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# CUSTOM CSS (keeps the UI clean and professional)
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* General spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* KPI card */
        .kpi-card {
            background-color: #ffffff;
            border: 1px solid #e6e9ef;
            border-radius: 12px;
            padding: 1.1rem 1.3rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        .kpi-label {
            font-size: 0.85rem;
            color: #6b7280;
            font-weight: 500;
            margin-bottom: 0.35rem;
        }
        .kpi-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #111827;
        }
        .kpi-sub {
            font-size: 0.75rem;
            color: #16a34a;
            margin-top: 0.25rem;
        }

        /* Section card */
        .section-card {
            background-color: #ffffff;
            border: 1px solid #e6e9ef;
            border-radius: 12px;
            padding: 1.2rem 1.4rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            margin-bottom: 1rem;
        }
        .section-title {
            font-size: 1.05rem;
            font-weight: 600;
            color: #111827;
            margin-bottom: 0.8rem;
        }

        /* Top header */
        .greeting-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #111827;
            margin-bottom: 0.1rem;
        }
        .greeting-sub {
            font-size: 0.95rem;
            color: #6b7280;
        }

        /* Sidebar branding */
        .sidebar-brand {
            font-size: 1.25rem;
            font-weight: 700;
            color: #111827;
            padding: 0.5rem 0 0.2rem 0;
        }
        .sidebar-brand-sub {
            font-size: 0.75rem;
            color: #6b7280;
            padding-bottom: 1rem;
        }

        /* Activity item */
        .activity-item {
            padding: 0.55rem 0;
            border-bottom: 1px solid #f0f1f3;
            font-size: 0.88rem;
            color: #374151;
        }
        .activity-time {
            font-size: 0.75rem;
            color: #9ca3af;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# SAMPLE / MOCK DATA
# (This section will later be replaced with data pulled from database.py)
# --------------------------------------------------------------------------

kpi_data = {
    "Total Employees": {"value": 48, "sub": "+3 this month"},
    "Present Today": {"value": 41, "sub": "85% attendance"},
    "On Leave": {"value": 5, "sub": "2 pending approval"},
    "Pending Leave Requests": {"value": 3, "sub": "Needs review"},
}

attendance_data = pd.DataFrame(
    {
        "Status": ["Present", "Absent", "Half Day", "On Leave"],
        "Count": [41, 2, 2, 5],
    }
)

leave_data = pd.DataFrame(
    {
        "Leave Type": ["Paid Leave", "Sick Leave", "Unpaid Leave"],
        "Count": [12, 7, 3],
    }
)

recent_activity = [
    {"type": "Check-in", "message": "Aditi Sharma checked in at 09:12 AM", "time": "5 min ago"},
    {"type": "Leave Application", "message": "Rohan Mehta applied for Sick Leave (2 days)", "time": "22 min ago"},
    {"type": "Leave Approval", "message": "Leave request of Priya Nair was approved", "time": "1 hr ago"},
    {"type": "HR Alert", "message": "Payroll processing scheduled for 28th", "time": "2 hr ago"},
    {"type": "Check-in", "message": "Karan Patel checked in at 09:45 AM", "time": "3 hr ago"},
    {"type": "Leave Rejection", "message": "Leave request of Sneha Reddy was rejected", "time": "4 hr ago"},
]

employee_overview = pd.DataFrame(
    {
        "Employee Name": [
            "Aditi Sharma", "Rohan Mehta", "Priya Nair", "Karan Patel",
            "Sneha Reddy", "Arjun Singh", "Meera Iyer", "Vikram Rao",
        ],
        "Department": [
            "Engineering", "Sales", "Marketing", "Engineering",
            "HR", "Finance", "Marketing", "Engineering",
        ],
        "Attendance %": [96, 88, 92, 97, 79, 90, 94, 85],
        "Leave Status": [
            "Active", "On Leave", "Active", "Active",
            "On Leave", "Active", "Active", "Pending Approval",
        ],
    }
)

# --------------------------------------------------------------------------
# SIDEBAR
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-brand">TEAM ODDO HRMS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-brand-sub">Human Resource Management</div>', unsafe_allow_html=True)

    st.divider()

    nav_options = [
        "Dashboard",
        "Employees",
        "Attendance",
        "Leave",
        "Payroll",
    ]
    selected_nav = st.radio("Navigation", nav_options, index=0, label_visibility="collapsed")

    st.divider()
    st.button("Logout", use_container_width=True)

# If a module other than Dashboard is selected, show a placeholder note.
# (Those modules are being built separately by other team members.)
if selected_nav != "Dashboard":
    st.info(f"The **{selected_nav}** module is being built by another team member. "
            f"This app only contains the Dashboard + Analytics module.")
    st.stop()

# --------------------------------------------------------------------------
# TOP SECTION - GREETING + PROFILE AREA
# --------------------------------------------------------------------------
top_left, top_right = st.columns([4, 1])

with top_left:
    st.markdown('<div class="greeting-title">Good Morning, Admin</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="greeting-sub">Here is what is happening across your organization today.</div>',
        unsafe_allow_html=True,
    )

with top_right:
    st.markdown(
        f"""
        <div style="text-align:right; padding-top:0.6rem;">
            <div style="font-size:0.8rem; color:#6b7280;">{datetime.now().strftime('%A, %d %B %Y')}</div>
            <div style="font-size:0.8rem; color:#6b7280;">3 new notifications</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# --------------------------------------------------------------------------
# KPI CARDS
# --------------------------------------------------------------------------
kpi_cols = st.columns(4)

for col, (label, data) in zip(kpi_cols, kpi_data.items()):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{data['value']}</div>
                <div class="kpi-sub">{data['sub']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")

# --------------------------------------------------------------------------
# ATTENDANCE + LEAVE ANALYTICS
# --------------------------------------------------------------------------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Attendance Overview</div>', unsafe_allow_html=True)

    attendance_chart = (
        alt.Chart(attendance_data)
        .mark_arc(innerRadius=60)
        .encode(
            theta=alt.Theta("Count", type="quantitative"),
            color=alt.Color(
                "Status",
                type="nominal",
                scale=alt.Scale(
                    domain=["Present", "Absent", "Half Day", "On Leave"],
                    range=["#22c55e", "#ef4444", "#f59e0b", "#3b82f6"],
                ),
            ),
            tooltip=["Status", "Count"],
        )
        .properties(height=280)
    )
    st.altair_chart(attendance_chart, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with chart_col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Leave Distribution</div>', unsafe_allow_html=True)

    leave_chart = (
        alt.Chart(leave_data)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("Leave Type", type="nominal", sort=None, title=None),
            y=alt.Y("Count", type="quantitative", title="Requests"),
            color=alt.Color(
                "Leave Type",
                type="nominal",
                scale=alt.Scale(
                    domain=["Paid Leave", "Sick Leave", "Unpaid Leave"],
                    range=["#6366f1", "#06b6d4", "#f97316"],
                ),
                legend=None,
            ),
            tooltip=["Leave Type", "Count"],
        )
        .properties(height=280)
    )
    st.altair_chart(leave_chart, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------------------------------
# RECENT ACTIVITY + EMPLOYEE OVERVIEW
# --------------------------------------------------------------------------
activity_col, overview_col = st.columns([1, 2])

with activity_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recent Activity</div>', unsafe_allow_html=True)

    for item in recent_activity:
        st.markdown(
            f"""
            <div class="activity-item">
                <strong>{item['type']}</strong><br>
                {item['message']}<br>
                <span class="activity-time">{item['time']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

with overview_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Employee Overview</div>', unsafe_allow_html=True)

    st.dataframe(
        employee_overview,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Attendance %": st.column_config.ProgressColumn(
                "Attendance %",
                min_value=0,
                max_value=100,
                format="%d%%",
            ),
        },
    )
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------------------
st.write("")
st.caption("TEAM ODDO HRMS — Dashboard module.")
