"""
Hospital & Patient Analysis - Core Analytics & Prediction Engine
Provides statistical aggregations, KPI computations, and predictive risk assessment.
"""

import pandas as pd
import numpy as np

def load_data(filepath="data/healthcare_dataset.csv"):
    """Loads and preprocesses the healthcare dataset."""
    df = pd.read_csv(filepath)
    df["Date_of_Admission"] = pd.to_datetime(df["Date_of_Admission"])
    df["Discharge_Date"] = pd.to_datetime(df["Discharge_Date"])
    
    # Age group categorization
    bins = [0, 18, 35, 50, 65, 100]
    labels = ["<18", "18-35", "36-50", "51-65", "65+"]
    df["Age_Group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)
    
    return df

def calculate_kpis(df):
    """Computes high-level clinical and operational Key Performance Indicators (KPIs)."""
    total_patients = len(df)
    if total_patients == 0:
        return {
            "total_patients": 0, "avg_los": 0, "total_revenue": 0,
            "avg_billing": 0, "readmission_rate": 0, "emergency_pct": 0,
            "abnormal_test_pct": 0
        }

    avg_los = round(float(df["Length_of_Stay"].mean()), 1)
    total_revenue = round(float(df["Billing_Amount"].sum()), 2)
    avg_billing = round(float(df["Billing_Amount"].mean()), 2)
    
    readmission_count = int((df["Readmission"] == "Yes").sum())
    readmission_rate = round(float((readmission_count / total_patients) * 100), 1)

    emergency_count = int((df["Admission_Type"] == "Emergency").sum())
    emergency_pct = round(float((emergency_count / total_patients) * 100), 1)

    abnormal_count = int((df["Test_Results"] == "Abnormal").sum())
    abnormal_test_pct = round(float((abnormal_count / total_patients) * 100), 1)

    return {
        "total_patients": total_patients,
        "avg_los": avg_los,
        "total_revenue": total_revenue,
        "avg_billing": avg_billing,
        "readmission_rate": readmission_rate,
        "emergency_pct": emergency_pct,
        "abnormal_test_pct": abnormal_test_pct
    }

def get_disease_distribution(df):
    """Returns frequency, avg stay, and avg billing grouped by medical condition."""
    grouped = df.groupby("Medical_Condition").agg(
        Patient_Count=("Patient_ID", "count"),
        Avg_Length_of_Stay=("Length_of_Stay", "mean"),
        Avg_Billing=("Billing_Amount", "mean"),
        Total_Billing=("Billing_Amount", "sum")
    ).reset_index()
    grouped["Avg_Length_of_Stay"] = grouped["Avg_Length_of_Stay"].round(1)
    grouped["Avg_Billing"] = grouped["Avg_Billing"].round(2)
    grouped.sort_values(by="Patient_Count", ascending=False, inplace=True)
    return grouped

def get_hospital_metrics(df):
    """Calculates operational and financial performance by hospital branch."""
    grouped = df.groupby("Hospital").agg(
        Total_Admissions=("Patient_ID", "count"),
        Avg_Stay_Days=("Length_of_Stay", "mean"),
        Total_Revenue=("Billing_Amount", "sum"),
        Readmission_Count=("Readmission", lambda x: (x == "Yes").sum())
    ).reset_index()
    grouped["Readmission_Rate"] = ((grouped["Readmission_Count"] / grouped["Total_Admissions"]) * 100).round(1)
    grouped["Avg_Stay_Days"] = grouped["Avg_Stay_Days"].round(1)
    grouped.sort_values(by="Total_Admissions", ascending=False, inplace=True)
    return grouped

def get_insurance_breakdown(df):
    """Returns revenue and patient distribution by insurance provider."""
    grouped = df.groupby("Insurance_Provider").agg(
        Patient_Count=("Patient_ID", "count"),
        Total_Covered=("Billing_Amount", "sum"),
        Avg_Claim=("Billing_Amount", "mean")
    ).reset_index()
    grouped["Avg_Claim"] = grouped["Avg_Claim"].round(2)
    grouped.sort_values(by="Total_Covered", ascending=False, inplace=True)
    return grouped

def predict_patient_risk(age, condition, admission_type, test_result, los_days=None):
    """
    Pure NumPy clinical risk prediction and triage score.
    Returns:
      - Risk Score (0 - 100)
      - Risk Category (Low, Moderate, High, Critical)
      - Estimated Length of Stay (days)
      - Clinical Care Recommendations
    """
    score = 20 # Baseline

    # Age impact
    if age >= 75:
        score += 25
    elif age >= 60:
        score += 15
    elif age >= 45:
        score += 8

    # Condition severity
    condition_weights = {
        "Cancer": 25,
        "Cardiovascular Disease": 22,
        "Chronic Kidney Disease": 20,
        "Pneumonia": 15,
        "Diabetes": 10,
        "Hypertension": 8,
        "Asthma": 6,
        "Arthritis": 4
    }
    score += condition_weights.get(condition, 10)

    # Admission type
    if admission_type == "Emergency":
        score += 20
    elif admission_type == "Urgent":
        score += 10
    else:
        score += 2

    # Test Results
    if test_result == "Abnormal":
        score += 18
    elif test_result == "Inconclusive":
        score += 8

    score = min(100, max(5, score))

    # Determine risk category
    if score >= 75:
        category = "Critical Risk"
        color = "#e53e3e"
        badge = "CRITICAL"
        stay_est = (10, 18)
        recommendations = [
            "Immediate ICU / Step-Down observation advised.",
            "Continuous vitals monitoring and specialist consult within 2 hours.",
            "Schedule follow-up pathology tests and multidisciplinary review.",
            "Flag for early readmission prevention protocol upon discharge."
        ]
    elif score >= 50:
        category = "High Risk"
        color = "#dd6b20"
        badge = "HIGH"
        stay_est = (6, 11)
        recommendations = [
            "Assign to designated inpatient monitoring ward.",
            "Daily lab reviews and vitals screening every 4 hours.",
            "Evaluate medication adjustment and secondary complications.",
            "Care coordinator assigned for post-discharge home care support."
        ]
    elif score >= 30:
        category = "Moderate Risk"
        color = "#d69e2e"
        badge = "MODERATE"
        stay_est = (3, 6)
        recommendations = [
            "Standard inpatient medical care protocol.",
            "Routine diagnostic testing and clinical checks every 8 hours.",
            "Prepare patient education regarding dietary and medical adherence."
        ]
    else:
        category = "Low Risk"
        color = "#38a169"
        badge = "LOW"
        stay_est = (1, 3)
        recommendations = [
            "Standard outpatient or short-stay observation.",
            "Discharge plan viable once vitals remain stable for 24h.",
            "Routine 2-week outpatient follow-up consultation."
        ]

    return {
        "score": score,
        "category": category,
        "badge": badge,
        "color": color,
        "estimated_stay_range": f"{stay_est[0]} - {stay_est[1]} days",
        "recommendations": recommendations
    }

if __name__ == "__main__":
    df = load_data()
    print("Dataset Loaded:", len(df), "rows")
    print("KPIs:", calculate_kpis(df))
    print("Risk test:", predict_patient_risk(68, "Cardiovascular Disease", "Emergency", "Abnormal"))
