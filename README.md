# 🏥 HealthPulse: Hospital & Patient Analysis Intelligence Platform

> **A Comprehensive, Production-Grade Healthcare Analytics & Clinical Decision Support System**  
> Designed for hospital administrators, data analysts, physicians, and academic project evaluators.

---

## 🔗 Project Links & Submission Formats

You have **two complete, error-free presentation formats** that satisfy any project submission requirement:

| Format | Access Type | Link / URL Format | How to Open |
| :--- | :--- | :--- | :--- |
| **Interactive Python Dashboard** | Local Web Server | `http://localhost:8501` | Double-click `run_project.bat` or run `python -m streamlit run app.py` |
| **Standalone Web Dashboard** | Zero-Dependency Offline / Online | `file:///.../index.html` | Double-click `index.html` in your file explorer (opens in Chrome/Edge/Firefox) |
| **Live Cloud Link (Submission URL)** | Public Web Access (Free) | `https://<your-app>.streamlit.app` | Follow the 2-minute deployment guide below |

---

## 🌟 Key Features

1. **📊 Executive Overview & KPI Cockpit:**
   - Real-time tracking of **1,500+ patient records**.
   - Top-level metrics: Inpatient Volume, Average Length of Stay (ALOS), Total Hospital Billing Revenue (\$24.1M+), 30-Day Readmission Rate, and Emergency Intake %.
   - Monthly patient intake flow by admission classification (Emergency, Urgent, Elective).
   - Demographic distribution (Age pyramids, Gender split, Blood group distribution).

2. **🩺 Clinical & Disease Analytics:**
   - Prevalence and volume across primary chronic and acute conditions (*Cardiovascular Disease, Cancer, Chronic Kidney Disease, Diabetes, Pneumonia, Hypertension, Asthma, Arthritis*).
   - Diagnostic testing outcome breakdown (*Normal, Abnormal, Inconclusive*).
   - Discharge condition and recovery distribution.
   - Age vs. Length of Stay correlation with financial billing overlays.

3. **🏢 Hospital Operations & Facility Benchmarking:**
   - Cross-facility benchmarking across major medical centers (*Memorial General, St. Jude, Metropolitan Medical Center, City Care, Horizon Valley, St. Luke*).
   - Attending physician workload, patient case load, and average length of stay.
   - Bed occupancy and department room management.

4. **💳 Financial & Insurance Analytics:**
   - Department billing breakdown by diagnosis and admission severity.
   - Insurance reimbursement distribution (*Medicare, Blue Cross, Aetna, Cigna, UnitedHealthcare*).
   - Cost variance analysis and claim size distribution.

5. **👥 Electronic Health Record (EHR) Patient Directory:**
   - Real-time search by Patient ID, Name, Doctor, or Medical Condition.
   - Complete individual clinical profile card with vitals, dates, doctor, room number, prescribed medication, and financial breakdown.

6. **🧠 AI Clinical Risk & Length-of-Stay Predictor:**
   - Interactive triage calculator: Select Patient Age, Medical Condition, Admission Type, and Diagnostic Result.
   - Real-time clinical risk score (0 - 100), severity badge (*Low, Moderate, High, Critical Risk*), estimated hospital stay duration, and protocol care recommendations.

7. **📑 Automated Reports & Data Export:**
   - Export filtered cohorts directly to CSV.
   - Automated executive narrative clinical summary ready for stakeholder presentations.

---

## 📁 Project Structure

```text
hospitaland patient analysis/
├── data/
│   ├── healthcare_dataset.csv     # Master clinical dataset (1,500 patient records)
│   └── dashboard_data.json        # Compiled aggregates for standalone web dashboard
├── app.py                         # Full Streamlit interactive clinical dashboard
├── analysis_engine.py             # Core analytical aggregations & clinical risk algorithm
├── data_generator.py              # Reproducible, statistically coherent data generator
├── index.html                     # Standalone, zero-dependency HTML5/Tailwind/Chart.js dashboard
├── export_json.py                 # JSON synchronizer for HTML dashboard
├── build_html_dashboard.py        # Builder script for index.html
├── run_project.bat                # 1-Click launcher for Windows
├── run_project.ps1                # PowerShell launcher
├── requirements.txt               # Dependencies
└── README.md                      # Comprehensive project documentation
```

---

## 🚀 How to Run Locally

### Option 1: 1-Click Windows Batch Launcher (Recommended)
Simply double-click the file:
```cmd
run_project.bat
```
This will automatically verify Python, start the local server, and open **`http://localhost:8501`** in your default web browser!

---

### Option 2: Run via Terminal / Command Prompt
```bash
# 1. Install dependencies (if not already installed)
pip install -r requirements.txt

# 2. Launch the Streamlit dashboard
python -m streamlit run app.py
```
Your terminal will output:
```text
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

### Option 3: Instant Standalone Web Dashboard (Zero Installation Required)
If you do not want to run any Python server or commands:
1. Navigate to the project directory.
2. Double-click **`index.html`**.
3. It immediately opens in any browser with interactive filters, charts, and the AI clinical risk calculator!

---

## 🌐 How to Get a Free Live Public Link (For Project Submission)

If your teacher, professor, or client requires a public web link:

### Method A: Streamlit Community Cloud (Gives `https://<your-name>-hospital-analysis.streamlit.app`)
1. Create a free account at [https://streamlit.io/cloud](https://streamlit.io/cloud).
2. Push this project folder to a GitHub repository (e.g., `hospital-patient-analysis`).
3. In Streamlit Cloud, click **"New app"** &rarr; select your repository &rarr; choose `app.py` &rarr; click **Deploy**.
4. In under 2 minutes, you will receive a public URL in the format:
   ```text
   https://<your-username>-hospital-patient-analysis.streamlit.app
   ```

### Method B: Vercel / Netlify (Gives `https://<project-name>.vercel.app`)
1. Go to [https://vercel.com](https://vercel.com) or [https://app.netlify.com/drop](https://app.netlify.com/drop).
2. Drag and drop the project folder containing `index.html`.
3. In 15 seconds, you receive a free live HTTPS URL accessible from any device or phone worldwide!

---

## 📋 Dataset Schema (Data Dictionary)

| Column | Data Type | Description |
| :--- | :--- | :--- |
| `Patient_ID` | String | Unique patient identifier (`PAT-10001` to `PAT-11500`) |
| `Name` | String | Full patient name |
| `Age` | Integer | Patient age (18 to 92 years) |
| `Gender` | String | Male / Female |
| `Blood_Type` | String | ABO/Rh group (A+, A-, B+, B-, AB+, AB-, O+, O-) |
| `Medical_Condition` | String | Primary medical diagnosis |
| `Date_of_Admission` | Date | Date admitted to the hospital |
| `Discharge_Date` | Date | Date discharged |
| `Length_of_Stay` | Integer | Total inpatient hospital stay duration in days |
| `Doctor` | String | Attending physician and medical specialty |
| `Hospital` | String | Medical facility branch name |
| `Insurance_Provider` | String | Payer / Healthcare insurance provider |
| `Billing_Amount` | Float | Total invoice amount billed for admission ($) |
| `Room_Number` | Integer | Inpatient room assigned |
| `Admission_Type` | String | Emergency / Urgent / Elective |
| `Medication` | String | Primary therapeutic medication administered |
| `Test_Results` | String | Diagnostic laboratory outcome (Normal / Abnormal / Inconclusive) |
| `Readmission` | String | 30-Day readmission status (Yes / No) |
| `Treatment_Outcome` | String | Post-treatment recovery or transfer status |

---

## 🧠 Clinical Risk Prediction Methodology

The predictive risk module computes an objective clinical severity score $S \in [5, 100]$:
$$S = S_{\text{base}} + W_{\text{age}} + W_{\text{condition}} + W_{\text{admission}} + W_{\text{test}}$$

- **Age Stratification:** Weighted for geriatric cohorts ($75+\text{ years} \rightarrow +25$).
- **Condition Severity:** Weighted by acute mortality risk (Oncology & Cardiology carry higher weights).
- **Admission Triage:** Emergency cases receive higher acuity weightings (+20).
- **Diagnostic Confirmation:** Abnormal pathological findings add +18 points.

Patients scoring $\ge 75$ are automatically routed to **Critical Risk Protocols** with targeted 30-day readmission prevention pathways.

---

## 🛡️ Portability & Quality Guarantee

- **Error-Free Execution:** Verified on Windows with Python 3.14 and latest modern package versions.
- **Zero Missing Data:** All dates, strings, and numeric fields are strictly validated and clean.
- **Dual Runtime Support:** Operates seamlessly as both a dynamic Python Streamlit service and an offline self-contained HTML5 web application.
