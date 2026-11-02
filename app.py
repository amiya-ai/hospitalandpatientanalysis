"""
Hospital & Patient Analysis - Interactive Clinical Intelligence Dashboard
Built with Streamlit and Plotly.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

from analysis_engine import load_data, calculate_kpis, get_disease_distribution, get_hospital_metrics, get_insurance_breakdown, predict_patient_risk

# Set page configuration
st.set_page_config(
    page_title="HealthPulse | Hospital & Patient Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 20px;
    }
    .metric-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07);
        border: 1px solid #e2e8f0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 4px;
    }
    .badge-emergency {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-elective {
        background-color: #e0e7ff;
        color: #3730a3;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-urgent {
        background-color: #fef3c7;
        color: #92400e;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Load dataset
@st.cache_data
def get_cached_data():
    dataset_path = "data/healthcare_dataset.csv"
    if not os.path.exists(dataset_path):
        from data_generator import generate_healthcare_data
        generate_healthcare_data(1500, dataset_path)
    return load_data(dataset_path)

df_raw = get_cached_data()

# Sidebar: Filters & Controls
st.sidebar.image("https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=300&q=80", use_container_width=True)
st.sidebar.title("🏥 Analytics Filter")
st.sidebar.caption("Filter clinical & patient records")

# Hospital filter
hospital_options = ["All Hospitals"] + sorted(list(df_raw["Hospital"].unique()))
selected_hospital = st.sidebar.selectbox("Hospital Facility", hospital_options)

# Condition filter
condition_options = sorted(list(df_raw["Medical_Condition"].unique()))
selected_conditions = st.sidebar.multiselect("Medical Condition(s)", condition_options, default=condition_options)

# Admission Type filter
admission_options = ["All Types"] + sorted(list(df_raw["Admission_Type"].unique()))
selected_admission = st.sidebar.selectbox("Admission Type", admission_options)

# Gender filter
gender_options = ["All Genders"] + sorted(list(df_raw["Gender"].unique()))
selected_gender = st.sidebar.selectbox("Gender", gender_options)

# Age Slider
min_age = int(df_raw["Age"].min())
max_age = int(df_raw["Age"].max())
selected_age_range = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))

# Apply Filters
df = df_raw.copy()
if selected_hospital != "All Hospitals":
    df = df[df["Hospital"] == selected_hospital]
if selected_conditions:
    df = df[df["Medical_Condition"].isin(selected_conditions)]
if selected_admission != "All Types":
    df = df[df["Admission_Type"] == selected_admission]
if selected_gender != "All Genders":
    df = df[df["Gender"] == selected_gender]
df = df[(df["Age"] >= selected_age_range[0]) & (df["Age"] <= selected_age_range[1])]

# Top Banner
col_head, col_badge = st.columns([3, 1])
with col_head:
    st.markdown('<div class="main-header">HealthPulse Clinical & Hospital Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Comprehensive Inpatient Healthcare Analytics, Resource Tracking & Risk Modeling</div>', unsafe_allow_html=True)
with col_badge:
    st.info(f"Showing **{len(df):,}** of **{len(df_raw):,}** Patient Records")

# Compute KPIs
kpis = calculate_kpis(df)

# KPI Cards Row
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Patients", f"{kpis['total_patients']:,}", delta=f"{len(df)-len(df_raw)} filtered" if len(df) != len(df_raw) else "100% active")
with col2:
    st.metric("Avg Length of Stay", f"{kpis['avg_los']} days", delta="Benchmark: 6.5d")
with col3:
    st.metric("Total Hospital Revenue", f"${kpis['total_revenue']:,.0f}", delta=f"Avg: ${kpis['avg_billing']:,.0f}")
with col4:
    st.metric("Readmission Rate", f"{kpis['readmission_rate']}%", delta="-2.1% target", delta_color="inverse")
with col5:
    st.metric("Emergency Intake", f"{kpis['emergency_pct']}%", delta=f"{kpis['abnormal_test_pct']}% abnormal tests")

st.markdown("---")

# Main Navigation Tabs
tab_overview, tab_clinical, tab_hospital, tab_financial, tab_patients, tab_predictor, tab_export = st.tabs([
    "📈 Executive Overview",
    "🩺 Clinical & Diseases",
    "🏢 Hospital Operations",
    "💳 Financials & Insurance",
    "👥 Patient Directory",
    "🧠 Clinical Risk Predictor",
    "📑 Reports & Export"
])

# ----------------- TAB 1: EXECUTIVE OVERVIEW -----------------
with tab_overview:
    st.subheader("Hospital Admissions & Operational Flow")
    
    col_t1_1, col_t1_2 = st.columns([2, 1])
    
    with col_t1_1:
        # Admissions trend over time
        df_time = df.copy()
        df_time["Month_Year"] = df_time["Date_of_Admission"].dt.to_period("M").astype(str)
        monthly_trend = df_time.groupby(["Month_Year", "Admission_Type"]).size().reset_index(name="Admissions")
        
        fig_trend = px.area(
            monthly_trend,
            x="Month_Year",
            y="Admissions",
            color="Admission_Type",
            title="Monthly Patient Admissions Flow by Admission Type",
            color_discrete_map={"Emergency": "#ef4444", "Urgent": "#f59e0b", "Elective": "#3b82f6"}
        )
        fig_trend.update_layout(xaxis_title="Month", yaxis_title="Number of Patients", hovermode="x unified")
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_t1_2:
        # Admission Type Pie
        adm_counts = df["Admission_Type"].value_counts().reset_index()
        adm_counts.columns = ["Admission_Type", "Count"]
        fig_pie = px.pie(
            adm_counts,
            values="Count",
            names="Admission_Type",
            title="Admissions Distribution",
            hole=0.45,
            color="Admission_Type",
            color_discrete_map={"Emergency": "#ef4444", "Urgent": "#f59e0b", "Elective": "#3b82f6"}
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    col_t1_3, col_t1_4 = st.columns(2)
    with col_t1_3:
        # Age distribution
        fig_age = px.histogram(
            df,
            x="Age",
            nbins=20,
            color="Gender",
            title="Patient Age & Demographics Profile",
            color_discrete_map={"Male": "#2563eb", "Female": "#ec4899"},
            marginal="box"
        )
        st.plotly_chart(fig_age, use_container_width=True)

    with col_t1_4:
        # Blood Type distribution
        blood_counts = df["Blood_Type"].value_counts().reset_index()
        blood_counts.columns = ["Blood_Type", "Count"]
        fig_blood = px.bar(
            blood_counts,
            x="Blood_Type",
            y="Count",
            title="Patient Blood Type Breakdown",
            color="Count",
            color_continuous_scale="Teal"
        )
        st.plotly_chart(fig_blood, use_container_width=True)

# ----------------- TAB 2: CLINICAL & DISEASES -----------------
with tab_clinical:
    st.subheader("Medical Diagnoses, Test Results & Treatment Pathways")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        # Disease Prevalence
        disease_df = get_disease_distribution(df)
        fig_dis = px.bar(
            disease_df,
            x="Patient_Count",
            y="Medical_Condition",
            orientation="h",
            title="Prevalence of Medical Diagnoses",
            color="Avg_Length_of_Stay",
            color_continuous_scale="Purples",
            labels={"Avg_Length_of_Stay": "Avg Stay (Days)"}
        )
        fig_dis.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_dis, use_container_width=True)

    with col_c2:
        # Test Results by Condition
        test_cond = df.groupby(["Medical_Condition", "Test_Results"]).size().reset_index(name="Count")
        fig_test = px.bar(
            test_cond,
            x="Medical_Condition",
            y="Count",
            color="Test_Results",
            title="Clinical Diagnostic Test Outcomes by Condition",
            barmode="stack",
            color_discrete_map={"Normal": "#10b981", "Inconclusive": "#f59e0b", "Abnormal": "#ef4444"}
        )
        fig_test.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(fig_test, use_container_width=True)

    # Treatment outcomes
    col_c3, col_c4 = st.columns(2)
    with col_c3:
        outcome_df = df.groupby(["Medical_Condition", "Treatment_Outcome"]).size().reset_index(name="Count")
        fig_outcome = px.bar(
            outcome_df,
            x="Medical_Condition",
            y="Count",
            color="Treatment_Outcome",
            title="Post-Treatment Discharge Outcomes by Diagnosis",
            barmode="group",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_outcome.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(fig_outcome, use_container_width=True)

    with col_c4:
        # Scatter: Age vs Length of stay
        fig_scatter = px.scatter(
            df,
            x="Age",
            y="Length_of_Stay",
            color="Medical_Condition",
            size="Billing_Amount",
            hover_data=["Patient_ID", "Doctor", "Admission_Type"],
            title="Length of Stay vs Patient Age (Bubble Size = Billing Cost)"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

# ----------------- TAB 3: HOSPITAL OPERATIONS -----------------
with tab_hospital:
    st.subheader("Facility Benchmarking & Capacity Management")

    hosp_df = get_hospital_metrics(df)
    col_h1, col_h2 = st.columns([3, 2])
    
    with col_h1:
        fig_hosp = px.bar(
            hosp_df,
            x="Hospital",
            y="Total_Admissions",
            color="Avg_Stay_Days",
            title="Hospital Facility Admissions & Mean Length of Stay",
            color_continuous_scale="Blues",
            labels={"Avg_Stay_Days": "Mean Stay (d)"}
        )
        fig_hosp.update_layout(xaxis_tickangle=-25)
        st.plotly_chart(fig_hosp, use_container_width=True)

    with col_h2:
        # Readmission rate by hospital
        fig_readmit = px.bar(
            hosp_df,
            x="Hospital",
            y="Readmission_Rate",
            title="30-Day Readmission Rate (%) by Hospital",
            color="Readmission_Rate",
            color_continuous_scale="Reds"
        )
        fig_readmit.update_layout(xaxis_tickangle=-25)
        st.plotly_chart(fig_readmit, use_container_width=True)

    # Doctor Performance Table
    st.write("#### 👨‍⚕️ Attending Physician Caseload & Performance")
    doc_df = df.groupby("Doctor").agg(
        Total_Patients=("Patient_ID", "count"),
        Avg_Stay=("Length_of_Stay", "mean"),
        Total_Billed=("Billing_Amount", "sum"),
        Emergency_Cases=("Admission_Type", lambda x: (x == "Emergency").sum())
    ).reset_index()
    doc_df["Avg_Stay"] = doc_df["Avg_Stay"].round(1)
    doc_df["Total_Billed"] = doc_df["Total_Billed"].apply(lambda x: f"${x:,.2f}")
    doc_df.sort_values(by="Total_Patients", ascending=False, inplace=True)
    st.dataframe(doc_df, use_container_width=True, hide_index=True)

# ----------------- TAB 4: FINANCIALS & INSURANCE -----------------
with tab_financial:
    st.subheader("Revenue Cycles, Claim Analytics & Department Billing")

    ins_df = get_insurance_breakdown(df)
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        fig_ins_pie = px.pie(
            ins_df,
            values="Total_Covered",
            names="Insurance_Provider",
            title="Hospital Billing Share by Insurance Carrier",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_ins_pie, use_container_width=True)

    with col_f2:
        fig_ins_bar = px.bar(
            ins_df,
            x="Insurance_Provider",
            y="Avg_Claim",
            title="Average Claim Amount ($) per Insurance Carrier",
            color="Avg_Claim",
            color_continuous_scale="Greens"
        )
        st.plotly_chart(fig_ins_bar, use_container_width=True)

    # Box plot of billing across conditions
    fig_box = px.box(
        df,
        x="Medical_Condition",
        y="Billing_Amount",
        color="Admission_Type",
        title="Billing Distribution by Medical Condition & Admission Classification",
        color_discrete_map={"Emergency": "#ef4444", "Urgent": "#f59e0b", "Elective": "#3b82f6"}
    )
    fig_box.update_layout(xaxis_tickangle=-25)
    st.plotly_chart(fig_box, use_container_width=True)

# ----------------- TAB 5: PATIENT DIRECTORY & EHR -----------------
with tab_patients:
    st.subheader("Patient Electronic Health Record (EHR) Lookup")

    search_query = st.text_input("🔍 Search Patient by Name, ID, or Doctor:", placeholder="e.g., PAT-10042, James, or Dr. Harris")
    
    df_search = df.copy()
    if search_query:
        mask = (
            df_search["Patient_ID"].str.contains(search_query, case=False, na=False) |
            df_search["Name"].str.contains(search_query, case=False, na=False) |
            df_search["Doctor"].str.contains(search_query, case=False, na=False) |
            df_search["Medical_Condition"].str.contains(search_query, case=False, na=False)
        )
        df_search = df_search[mask]

    st.write(f"Showing **{len(df_search)}** matching patient records:")
    
    # Selection of specific patient
    if len(df_search) > 0:
        patient_list = [f"{row['Patient_ID']} - {row['Name']} ({row['Medical_Condition']})" for _, row in df_search.head(100).iterrows()]
        selected_patient_str = st.selectbox("Select Patient to view complete Clinical Record:", patient_list)
        
        selected_pid = selected_patient_str.split(" - ")[0]
        p_row = df_raw[df_raw["Patient_ID"] == selected_pid].iloc[0]

        # Clinical Profile Card
        st.markdown(f"""
        <div style="background:#f8fafc; border-radius:12px; padding:24px; border:1px solid #cbd5e1; margin-top:15px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h2 style="margin:0; color:#1e293b;">{p_row['Name']}</h2>
                    <span style="color:#64748b; font-weight:600;">ID: {p_row['Patient_ID']} | Age: {p_row['Age']} yrs | Gender: {p_row['Gender']} | Blood: {p_row['Blood_Type']}</span>
                </div>
                <div>
                    <span style="background:{'#ef4444' if p_row['Admission_Type']=='Emergency' else '#3b82f6'}; color:white; padding:6px 14px; border-radius:20px; font-weight:bold; font-size:0.85rem;">
                        {p_row['Admission_Type']}
                    </span>
                </div>
            </div>
            <hr style="margin:16px 0; border:0; border-top:1px solid #e2e8f0;"/>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:16px;">
                <div><strong>Condition:</strong><br/><span style="color:#0284c7; font-size:1.1rem; font-weight:600;">{p_row['Medical_Condition']}</span></div>
                <div><strong>Attending Doctor:</strong><br/>{p_row['Doctor']}</div>
                <div><strong>Facility:</strong><br/>{p_row['Hospital']} (Room #{p_row['Room_Number']})</div>
                <div><strong>Admission:</strong><br/>{str(p_row['Date_of_Admission'])[:10]}</div>
                <div><strong>Discharge:</strong><br/>{str(p_row['Discharge_Date'])[:10]} ({p_row['Length_of_Stay']} days)</div>
                <div><strong>Prescribed Med:</strong><br/>{p_row['Medication']}</div>
                <div><strong>Diagnostic Test:</strong><br/><span style="color:{'#dc2626' if p_row['Test_Results']=='Abnormal' else '#16a34a'}; font-weight:bold;">{p_row['Test_Results']}</span></div>
                <div><strong>Discharge Outcome:</strong><br/>{p_row['Treatment_Outcome']}</div>
                <div><strong>Readmission Status:</strong><br/>{'⚠️ Yes (Within 30 Days)' if p_row['Readmission']=='Yes' else '✅ No Readmission'}</div>
                <div><strong>Billing Amount:</strong><br/><span style="font-size:1.15rem; font-weight:700; color:#0f766e;">${p_row['Billing_Amount']:,.2f}</span> ({p_row['Insurance_Provider']})</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No patients match your search criteria.")

    # Table view
    st.write("#### 📋 Complete Patient Roster")
    st.dataframe(
        df_search[[
            "Patient_ID", "Name", "Age", "Gender", "Medical_Condition",
            "Admission_Type", "Hospital", "Doctor", "Length_of_Stay",
            "Billing_Amount", "Test_Results", "Readmission"
        ]],
        use_container_width=True,
        hide_index=True
    )

# ----------------- TAB 6: CLINICAL RISK & LOS PREDICTOR -----------------
with tab_predictor:
    st.subheader("🧠 Predictive Clinical Risk & Length-of-Stay Assessment")
    st.markdown("Use this clinical decision support tool to evaluate patient admission risk, estimate hospital stay duration, and generate triage care pathways.")

    col_p1, col_p2 = st.columns([1, 1])

    with col_p1:
        st.write("#### 📝 Patient Intake Parameters")
        pred_age = st.slider("Patient Age", 18, 95, 58)
        pred_condition = st.selectbox("Primary Diagnosis / Condition", sorted(list(df_raw["Medical_Condition"].unique())), index=3)
        pred_adm = st.selectbox("Admission Priority", ["Emergency", "Urgent", "Elective"], index=0)
        pred_test = st.selectbox("Diagnostic / Lab Test Result", ["Abnormal", "Inconclusive", "Normal"], index=0)
        
        calc_btn = st.button("⚡ Compute Clinical Risk & Prognosis", type="primary", use_container_width=True)

    with col_p2:
        st.write("#### 📋 Risk Prognosis & Care Protocol")
        risk_result = predict_patient_risk(pred_age, pred_condition, pred_adm, pred_test)

        score = risk_result["score"]
        category = risk_result["category"]
        badge_color = risk_result["color"]

        # Gauge chart for risk score
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"Clinical Risk Score: <b>{category}</b>", 'font': {'size': 18}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': badge_color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 30], 'color': '#d1fae5'},
                    {'range': [30, 50], 'color': '#fef3c7'},
                    {'range': [50, 75], 'color': '#fed7aa'},
                    {'range': [75, 100], 'color': '#fee2e2'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown(f"""
        **Estimated Length of Stay:** `{risk_result['estimated_stay_range']}`  
        **Recommended Protocol Actions:**
        """)
        for rec in risk_result["recommendations"]:
            st.markdown(f"- {rec}")

# ----------------- TAB 7: REPORTS & EXPORT -----------------
with tab_export:
    st.subheader("📑 Automated Clinical Summary & Data Export")
    
    col_e1, col_e2 = st.columns([2, 1])

    with col_e1:
        st.write("#### 📊 Clinical Executive Summary Report")
        summary_text = f"""
### Executive Clinical & Operational Review
- **Evaluation Period:** 2023 - 2024
- **Active Filtered Cohort:** {kpis['total_patients']:,} patients evaluated across {len(selected_conditions)} disease categories.
- **Bed Utilization & Stay:** Mean Length of Stay (ALOS) is recorded at **{kpis['avg_los']} days**.
- **Financial Performance:** Total accrued hospital billing represents **${kpis['total_revenue']:,.2f}** with an average invoice of **${kpis['avg_billing']:,.2f}** per patient.
- **Clinical Quality Indicator:** 30-Day Readmission stands at **{kpis['readmission_rate']}%**.
- **Emergency Department Load:** Emergency admissions account for **{kpis['emergency_pct']}%** of all intake traffic, with **{kpis['abnormal_test_pct']}%** of diagnostic tests demonstrating abnormal clinical markers.

#### Strategic Recommendations:
1. **Targeted Readmission Interventions:** Implement enhanced follow-up pathways for cardiovascular and oncological cases with abnormal discharge labs.
2. **Resource Optimization:** Reallocate emergency surge beds during peak intake cycles to reduce elective admission delays.
3. **Payer Contracting:** Realign negotiated fee schedules with high-volume insurance carriers (e.g., Medicare and Blue Cross) to reflect disease severity.
        """
        st.markdown(summary_text)

    with col_e2:
        st.write("#### 📥 Export Data Files")
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Filtered Dataset (CSV)",
            data=csv_data,
            file_name=f"hospital_patient_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.download_button(
            label="⬇️ Download Executive Summary (Markdown)",
            data=summary_text,
            file_name=f"clinical_summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#94a3b8; font-size:0.85rem; padding:10px 0;">
    🏥 <strong>HealthPulse Analytics Platform</strong> | Hospital & Patient Analysis System | Built with Python, Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
