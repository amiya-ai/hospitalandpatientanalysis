"""
Builder script to generate index.html with embedded data for 100% offline & online portability.
"""
import json

def build():
    with open("data/dashboard_data.json", "r") as f:
        data_json = f.read()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HealthPulse | Hospital & Patient Analytics Dashboard</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #f8fafc;
        }}
        .metric-card {{
            transition: all 0.25s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
        }}
        .custom-scrollbar::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{
            background: #cbd5e1;
            border-radius: 4px;
        }}
    </style>
</head>
<body class="text-slate-800 antialiased min-h-screen flex flex-col">

    <!-- Top Navigation Bar -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
                    <i data-lucide="activity" class="w-6 h-6"></i>
                </div>
                <div>
                    <h1 class="text-xl font-bold text-slate-900 leading-tight flex items-center gap-2">
                        HealthPulse <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">Analytics Pro</span>
                    </h1>
                    <p class="text-xs text-slate-500">Hospital Inpatient Operations & Clinical Intelligence Platform</p>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <button onclick="openModal('shareModal')" class="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold text-blue-700 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-lg transition-colors">
                    <i data-lucide="share-2" class="w-4 h-4"></i>
                    Get Shareable Link
                </button>
                <button onclick="downloadCSV()" class="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-lg shadow-sm transition-colors">
                    <i data-lucide="download" class="w-4 h-4"></i>
                    Export CSV
                </button>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">

        <!-- Filter Bar -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div class="flex items-center gap-2 text-slate-700 font-semibold text-sm">
                    <i data-lucide="filter" class="w-4 h-4 text-blue-600"></i>
                    <span>Interactive Filters</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 w-full md:w-auto flex-1 max-w-4xl">
                    <select id="filterHospital" onchange="applyFilters()" class="text-xs bg-slate-50 border border-slate-300 text-slate-700 rounded-lg p-2.5 focus:ring-blue-500 focus:border-blue-500">
                        <option value="ALL">All Hospital Facilities</option>
                    </select>

                    <select id="filterCondition" onchange="applyFilters()" class="text-xs bg-slate-50 border border-slate-300 text-slate-700 rounded-lg p-2.5 focus:ring-blue-500 focus:border-blue-500">
                        <option value="ALL">All Medical Conditions</option>
                    </select>

                    <select id="filterAdmission" onchange="applyFilters()" class="text-xs bg-slate-50 border border-slate-300 text-slate-700 rounded-lg p-2.5 focus:ring-blue-500 focus:border-blue-500">
                        <option value="ALL">All Admission Types</option>
                        <option value="Emergency">Emergency Only</option>
                        <option value="Urgent">Urgent Only</option>
                        <option value="Elective">Elective Only</option>
                    </select>

                    <input type="text" id="filterSearch" oninput="applyFilters()" placeholder="Search patient ID, name, doctor..." class="text-xs bg-slate-50 border border-slate-300 text-slate-700 rounded-lg p-2.5 focus:ring-blue-500 focus:border-blue-500">
                </div>
                <button onclick="resetFilters()" class="text-xs text-slate-500 hover:text-slate-800 underline self-center">Reset</button>
            </div>
        </div>

        <!-- KPI Summary Cards -->
        <div class="grid grid-cols-2 lg:grid-cols-5 gap-4">
            <div class="metric-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase tracking-wider">
                    <span>Total Patients</span>
                    <i data-lucide="users" class="w-4 h-4 text-blue-600"></i>
                </div>
                <div id="kpiPatients" class="text-2xl font-bold text-slate-900 mt-2">1,500</div>
                <div class="text-xs text-slate-500 mt-1">Inpatient Admissions</div>
            </div>

            <div class="metric-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase tracking-wider">
                    <span>Avg Length of Stay</span>
                    <i data-lucide="clock" class="w-4 h-4 text-emerald-600"></i>
                </div>
                <div id="kpiStay" class="text-2xl font-bold text-slate-900 mt-2">7.2 days</div>
                <div class="text-xs text-emerald-600 font-medium mt-1">Benchmark: 6.5d</div>
            </div>

            <div class="metric-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase tracking-wider">
                    <span>Total Revenue</span>
                    <i data-lucide="dollar-sign" class="w-4 h-4 text-indigo-600"></i>
                </div>
                <div id="kpiRevenue" class="text-2xl font-bold text-slate-900 mt-2">$24.1M</div>
                <div id="kpiAvgBill" class="text-xs text-slate-500 mt-1">Avg: $16,087 / patient</div>
            </div>

            <div class="metric-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase tracking-wider">
                    <span>Readmission Rate</span>
                    <i data-lucide="refresh-cw" class="w-4 h-4 text-amber-600"></i>
                </div>
                <div id="kpiReadmission" class="text-2xl font-bold text-slate-900 mt-2">18.9%</div>
                <div class="text-xs text-amber-600 font-medium mt-1">30-Day Follow-up</div>
            </div>

            <div class="metric-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm col-span-2 lg:col-span-1">
                <div class="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase tracking-wider">
                    <span>Emergency Intake</span>
                    <i data-lucide="alert-triangle" class="w-4 h-4 text-rose-600"></i>
                </div>
                <div id="kpiEmergency" class="text-2xl font-bold text-slate-900 mt-2">34.1%</div>
                <div class="text-xs text-rose-600 font-medium mt-1">Critical Triage Cases</div>
            </div>
        </div>

        <!-- Section 1: Visual Analytics Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Disease Distribution -->
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm lg:col-span-2 flex flex-col justify-between">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-sm font-bold text-slate-800 flex items-center gap-2">
                        <i data-lucide="stethoscope" class="w-4 h-4 text-blue-600"></i>
                        Clinical Diagnoses Prevalence & Patient Volume
                    </h3>
                    <span class="text-xs text-slate-500">By Medical Condition</span>
                </div>
                <div class="relative h-64">
                    <canvas id="diseaseChart"></canvas>
                </div>
            </div>

            <!-- Admission Type Donut -->
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-sm font-bold text-slate-800 flex items-center gap-2">
                        <i data-lucide="pie-chart" class="w-4 h-4 text-blue-600"></i>
                        Admission Priority Share
                    </h3>
                </div>
                <div class="relative h-64">
                    <canvas id="admissionChart"></canvas>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Hospital Facility Benchmark -->
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-sm font-bold text-slate-800 flex items-center gap-2">
                        <i data-lucide="building-2" class="w-4 h-4 text-blue-600"></i>
                        Facility Admissions Comparison
                    </h3>
                    <span class="text-xs text-slate-500">Inpatient Traffic</span>
                </div>
                <div class="relative h-64">
                    <canvas id="hospitalChart"></canvas>
                </div>
            </div>

            <!-- Insurance Reimbursement -->
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-sm font-bold text-slate-800 flex items-center gap-2">
                        <i data-lucide="credit-card" class="w-4 h-4 text-blue-600"></i>
                        Insurance Carrier Claims Distribution
                    </h3>
                    <span class="text-xs text-slate-500">Coverage Breakdown</span>
                </div>
                <div class="relative h-64">
                    <canvas id="insuranceChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Section 2: Clinical Risk & LOS Predictor Tool -->
        <div class="bg-gradient-to-r from-slate-900 to-blue-950 text-white p-6 rounded-2xl shadow-lg border border-slate-800">
            <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-800 gap-2">
                <div>
                    <h2 class="text-lg font-bold flex items-center gap-2">
                        <i data-lucide="brain-circuit" class="w-5 h-5 text-cyan-400"></i>
                        AI Clinical Risk & Stay Predictor
                    </h2>
                    <p class="text-xs text-slate-300">Evaluate inpatient severity score, predict hospital stay length, and generate care pathway guidance</p>
                </div>
                <span class="text-xs px-3 py-1 bg-cyan-500/20 text-cyan-300 border border-cyan-400/30 rounded-full font-medium">Interactive Clinical Decision Support</span>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 pt-6">
                <!-- Inputs -->
                <div class="space-y-4">
                    <div>
                        <label class="block text-xs font-medium text-slate-300 mb-1">Patient Age: <span id="ageDisplay" class="font-bold text-cyan-400">58</span> yrs</label>
                        <input type="range" id="predAge" min="18" max="95" value="58" oninput="updatePrediction()" class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-cyan-400">
                    </div>

                    <div>
                        <label class="block text-xs font-medium text-slate-300 mb-1">Primary Diagnosis</label>
                        <select id="predCondition" onchange="updatePrediction()" class="w-full text-xs bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 focus:ring-cyan-400">
                            <option value="Cardiovascular Disease">Cardiovascular Disease</option>
                            <option value="Cancer">Cancer</option>
                            <option value="Chronic Kidney Disease">Chronic Kidney Disease</option>
                            <option value="Diabetes">Diabetes</option>
                            <option value="Pneumonia">Pneumonia</option>
                            <option value="Hypertension">Hypertension</option>
                            <option value="Asthma">Asthma</option>
                            <option value="Arthritis">Arthritis</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-medium text-slate-300 mb-1">Admission Type</label>
                        <select id="predAdmission" onchange="updatePrediction()" class="w-full text-xs bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 focus:ring-cyan-400">
                            <option value="Emergency">Emergency</option>
                            <option value="Urgent">Urgent</option>
                            <option value="Elective">Elective</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-medium text-slate-300 mb-1">Diagnostic Test Result</label>
                        <select id="predTest" onchange="updatePrediction()" class="w-full text-xs bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 focus:ring-cyan-400">
                            <option value="Abnormal">Abnormal</option>
                            <option value="Inconclusive">Inconclusive</option>
                            <option value="Normal">Normal</option>
                        </select>
                    </div>
                </div>

                <!-- Result Score Display -->
                <div class="bg-slate-800/80 p-5 rounded-xl border border-slate-700 flex flex-col items-center justify-center text-center">
                    <span class="text-xs uppercase tracking-wider text-slate-400 font-semibold">Calculated Clinical Risk</span>
                    <div id="riskScoreNumber" class="text-5xl font-black my-2 text-rose-400">75</div>
                    <div id="riskBadge" class="px-3 py-1 rounded-full text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">CRITICAL RISK</div>
                    
                    <div class="w-full border-t border-slate-700 mt-4 pt-3 text-left">
                        <span class="text-xs text-slate-400">Estimated Length of Stay:</span>
                        <div id="stayEst" class="text-sm font-bold text-cyan-300">10 - 18 days</div>
                    </div>
                </div>

                <!-- Recommended Care Actions -->
                <div class="bg-slate-800/80 p-5 rounded-xl border border-slate-700 flex flex-col justify-between">
                    <div>
                        <span class="text-xs uppercase tracking-wider text-slate-400 font-semibold mb-2 block flex items-center gap-1.5">
                            <i data-lucide="clipboard-check" class="w-4 h-4 text-emerald-400"></i>
                            Protocol & Action Steps
                        </span>
                        <ul id="recommendationsList" class="text-xs text-slate-300 space-y-2 list-disc pl-4 mt-2">
                            <li>Immediate ICU / Step-Down observation advised.</li>
                            <li>Continuous vitals monitoring and specialist consult within 2 hours.</li>
                            <li>Schedule follow-up pathology tests and multidisciplinary review.</li>
                        </ul>
                    </div>
                    <div class="text-[11px] text-slate-400 mt-3 pt-2 border-t border-slate-700">
                        Based on standardized Inpatient Clinical Severity Matrix.
                    </div>
                </div>
            </div>
        </div>

        <!-- Section 3: Patient Records Table -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div class="p-4 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                    <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2">
                        <i data-lucide="table" class="w-4 h-4 text-blue-600"></i>
                        Electronic Health Record (EHR) Patient Directory
                    </h3>
                    <p class="text-xs text-slate-500">Showing active cohort with clinical outcomes and billing records</p>
                </div>
                <div class="text-xs text-slate-500">
                    <span id="tableRecordCount" class="font-bold text-slate-800">0</span> Records Found
                </div>
            </div>

            <div class="overflow-x-auto custom-scrollbar max-h-96">
                <table class="min-w-full divide-y divide-slate-200 text-left text-xs">
                    <thead class="bg-slate-50 sticky top-0 z-10 text-slate-500 uppercase tracking-wider font-semibold">
                        <tr>
                            <th class="px-4 py-3">Patient ID</th>
                            <th class="px-4 py-3">Name</th>
                            <th class="px-4 py-3">Age / Gen</th>
                            <th class="px-4 py-3">Condition</th>
                            <th class="px-4 py-3">Facility</th>
                            <th class="px-4 py-3">Doctor</th>
                            <th class="px-4 py-3">Admission</th>
                            <th class="px-4 py-3">Stay</th>
                            <th class="px-4 py-3">Test Result</th>
                            <th class="px-4 py-3">Readmit</th>
                            <th class="px-4 py-3">Billing</th>
                        </tr>
                    </thead>
                    <tbody id="patientTableBody" class="divide-y divide-slate-200 text-slate-700">
                        <!-- Populated by JavaScript -->
                    </tbody>
                </table>
            </div>
        </div>

    </main>

    <!-- Share / Deploy Modal -->
    <div id="shareModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-100">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                    <i data-lucide="link" class="w-5 h-5 text-blue-600"></i>
                    Project Access & Live Links
                </h3>
                <button onclick="closeModal('shareModal')" class="text-slate-400 hover:text-slate-700">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>
            
            <div class="py-4 space-y-4 text-xs">
                <div class="p-3.5 bg-blue-50 border border-blue-200 rounded-xl">
                    <span class="font-bold text-blue-900 block mb-1">🔗 1. Local Interactive Streamlit Dashboard Link:</span>
                    <code class="bg-white px-2 py-1 rounded text-blue-800 font-mono text-xs select-all block border border-blue-200 mt-1">http://localhost:8501</code>
                    <p class="text-slate-600 mt-1">Run <code class="bg-white px-1 rounded text-slate-800">run_project.bat</code> to spin up the local server and open this link automatically.</p>
                </div>

                <div class="p-3.5 bg-emerald-50 border border-emerald-200 rounded-xl">
                    <span class="font-bold text-emerald-900 block mb-1">🌐 2. Standalone Portable Web Link:</span>
                    <code class="bg-white px-2 py-1 rounded text-emerald-800 font-mono text-xs select-all block border border-emerald-200 mt-1">file:///.../index.html</code>
                    <p class="text-slate-600 mt-1">This dashboard requires zero server or dependencies. Double-click <code class="bg-white px-1 rounded text-slate-800">index.html</code> to open immediately in any browser!</p>
                </div>

                <div class="p-3.5 bg-purple-50 border border-purple-200 rounded-xl">
                    <span class="font-bold text-purple-900 block mb-1">🚀 3. Free Permanent Public Web URL (For Submission):</span>
                    <p class="text-slate-600">To host and get a public <code class="bg-white px-1 rounded text-purple-800 font-mono">https://...</code> submission link:</p>
                    <ul class="list-disc pl-4 text-slate-600 mt-1 space-y-1">
                        <li><strong>Streamlit Cloud:</strong> Push folder to GitHub & connect to <a href="https://streamlit.io/cloud" target="_blank" class="text-blue-600 underline">streamlit.io/cloud</a> &rarr; get <code class="font-mono text-purple-700">https://your-name-hospital.streamlit.app</code></li>
                        <li><strong>GitHub Pages / Vercel:</strong> Drag <code class="font-mono">index.html</code> to Vercel/Netlify for a 10-second instant link.</li>
                    </ul>
                </div>
            </div>

            <div class="pt-2 flex justify-end">
                <button onclick="closeModal('shareModal')" class="px-4 py-2 bg-slate-900 text-white rounded-lg text-xs font-semibold hover:bg-slate-800">Got it</button>
            </div>
        </div>
    </div>

    <!-- Embedded Data Payload -->
    <script id="embeddedData" type="application/json">
{data_json}
    </script>

    <!-- Dashboard Logic Script -->
    <script>
        // Load data safely
        let rawData = {{}};
        try {{
            rawData = JSON.parse(document.getElementById('embeddedData').textContent);
        }} catch(e) {{
            console.error("Failed to parse embedded data", e);
        }}

        let allPatients = rawData.patients || [];
        let filteredPatients = [...allPatients];

        // Chart instances
        let diseaseChartInst = null;
        let admissionChartInst = null;
        let hospitalChartInst = null;
        let insuranceChartInst = null;

        // Initialize icons and UI
        document.addEventListener('DOMContentLoaded', () => {{
            lucide.createIcons();
            populateFilters();
            renderCharts();
            renderTable();
            updatePrediction();
        }});

        function populateFilters() {{
            const hospSelect = document.getElementById('filterHospital');
            const condSelect = document.getElementById('filterCondition');

            const hospitals = [...new Set(allPatients.map(p => p.Hospital))].sort();
            const conditions = [...new Set(allPatients.map(p => p.Medical_Condition))].sort();

            hospitals.forEach(h => {{
                const opt = document.createElement('option');
                opt.value = h;
                opt.textContent = h;
                hospSelect.appendChild(opt);
            }});

            conditions.forEach(c => {{
                const opt = document.createElement('option');
                opt.value = c;
                opt.textContent = c;
                condSelect.appendChild(opt);
            }});
        }}

        function applyFilters() {{
            const hosp = document.getElementById('filterHospital').value;
            const cond = document.getElementById('filterCondition').value;
            const adm = document.getElementById('filterAdmission').value;
            const q = document.getElementById('filterSearch').value.toLowerCase().trim();

            filteredPatients = allPatients.filter(p => {{
                if (hosp !== 'ALL' && p.Hospital !== hosp) return false;
                if (cond !== 'ALL' && p.Medical_Condition !== cond) return false;
                if (adm !== 'ALL' && p.Admission_Type !== adm) return false;
                if (q) {{
                    const matchId = p.Patient_ID.toLowerCase().includes(q);
                    const matchName = p.Name.toLowerCase().includes(q);
                    const matchDoc = p.Doctor.toLowerCase().includes(q);
                    const matchCond = p.Medical_Condition.toLowerCase().includes(q);
                    if (!matchId && !matchName && !matchDoc && !matchCond) return false;
                }}
                return true;
            }});

            updateKPIs();
            renderTable();
        }}

        function resetFilters() {{
            document.getElementById('filterHospital').value = 'ALL';
            document.getElementById('filterCondition').value = 'ALL';
            document.getElementById('filterAdmission').value = 'ALL';
            document.getElementById('filterSearch').value = '';
            filteredPatients = [...allPatients];
            updateKPIs();
            renderTable();
        }}

        function updateKPIs() {{
            const n = filteredPatients.length;
            if (n === 0) {{
                document.getElementById('kpiPatients').textContent = '0';
                document.getElementById('kpiStay').textContent = '0d';
                document.getElementById('kpiRevenue').textContent = '$0';
                document.getElementById('kpiAvgBill').textContent = 'Avg: $0';
                document.getElementById('kpiReadmission').textContent = '0%';
                document.getElementById('kpiEmergency').textContent = '0%';
                return;
            }}

            const totalStay = filteredPatients.reduce((acc, p) => acc + p.Length_of_Stay, 0);
            const totalRev = filteredPatients.reduce((acc, p) => acc + p.Billing_Amount, 0);
            const readmits = filteredPatients.filter(p => p.Readmission === 'Yes').length;
            const emergencies = filteredPatients.filter(p => p.Admission_Type === 'Emergency').length;

            const avgStay = (totalStay / n).toFixed(1);
            const avgBill = (totalRev / n).toFixed(0);
            const readmitPct = ((readmits / n) * 100).toFixed(1);
            const emergPct = ((emergencies / n) * 100).toFixed(1);

            document.getElementById('kpiPatients').textContent = n.toLocaleString();
            document.getElementById('kpiStay').textContent = avgStay + ' days';
            document.getElementById('kpiRevenue').textContent = '$' + (totalRev / 1000000).toFixed(1) + 'M';
            document.getElementById('kpiAvgBill').textContent = 'Avg: $' + parseInt(avgBill).toLocaleString();
            document.getElementById('kpiReadmission').textContent = readmitPct + '%';
            document.getElementById('kpiEmergency').textContent = emergPct + '%';
        }}

        function renderCharts() {{
            // 1. Disease Distribution Chart
            const diseaseData = rawData.diseases || [];
            const ctxDisease = document.getElementById('diseaseChart').getContext('2d');
            diseaseChartInst = new Chart(ctxDisease, {{
                type: 'bar',
                data: {{
                    labels: diseaseData.map(d => d.Medical_Condition),
                    datasets: [{{
                        label: 'Patient Count',
                        data: diseaseData.map(d => d.Patient_Count),
                        backgroundColor: '#3b82f6',
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }},
                        x: {{ grid: {{ display: false }} }}
                    }}
                }}
            }});

            // 2. Admission Type Donut
            const ctxAdm = document.getElementById('admissionChart').getContext('2d');
            const admCounts = {{ Emergency: 0, Urgent: 0, Elective: 0 }};
            allPatients.forEach(p => {{ if(admCounts[p.Admission_Type] !== undefined) admCounts[p.Admission_Type]++; }});

            admissionChartInst = new Chart(ctxAdm, {{
                type: 'doughnut',
                data: {{
                    labels: ['Emergency', 'Urgent', 'Elective'],
                    datasets: [{{
                        data: [admCounts.Emergency, admCounts.Urgent, admCounts.Elective],
                        backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6'],
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom' }}
                    }}
                }}
            }});

            // 3. Hospital Facility Admissions
            const hospData = rawData.hospitals || [];
            const ctxHosp = document.getElementById('hospitalChart').getContext('2d');
            hospitalChartInst = new Chart(ctxHosp, {{
                type: 'bar',
                data: {{
                    labels: hospData.map(h => h.Hospital.replace("Hospital", "").replace("Medical Center", "MC")),
                    datasets: [{{
                        label: 'Admissions',
                        data: hospData.map(h => h.Total_Admissions),
                        backgroundColor: '#6366f1',
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }},
                        x: {{ grid: {{ display: false }} }}
                    }}
                }}
            }});

            // 4. Insurance Chart
            const insData = rawData.insurance || [];
            const ctxIns = document.getElementById('insuranceChart').getContext('2d');
            insuranceChartInst = new Chart(ctxIns, {{
                type: 'bar',
                data: {{
                    labels: insData.map(i => i.Insurance_Provider),
                    datasets: [{{
                        label: 'Covered Patients',
                        data: insData.map(i => i.Patient_Count),
                        backgroundColor: '#10b981',
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }},
                        x: {{ grid: {{ display: false }} }}
                    }}
                }}
            }});
        }}

        function renderTable() {{
            const tbody = document.getElementById('patientTableBody');
            const countLabel = document.getElementById('tableRecordCount');
            tbody.innerHTML = '';
            countLabel.textContent = filteredPatients.length;

            const displayList = filteredPatients.slice(0, 100);

            if (displayList.length === 0) {{
                tbody.innerHTML = `<tr><td colspan="11" class="px-4 py-8 text-center text-slate-400">No patient records match the selected filters.</td></tr>`;
                return;
            }}

            displayList.forEach(p => {{
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-50 transition-colors";

                const admBadge = p.Admission_Type === 'Emergency' 
                    ? '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-rose-100 text-rose-700">Emergency</span>'
                    : p.Admission_Type === 'Urgent'
                    ? '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-100 text-amber-700">Urgent</span>'
                    : '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-100 text-blue-700">Elective</span>';

                const testBadge = p.Test_Results === 'Abnormal'
                    ? '<span class="text-rose-600 font-semibold">Abnormal</span>'
                    : p.Test_Results === 'Inconclusive'
                    ? '<span class="text-amber-600 font-semibold">Inconclusive</span>'
                    : '<span class="text-emerald-600 font-semibold">Normal</span>';

                tr.innerHTML = `
                    <td class="px-4 py-2.5 font-mono text-slate-900 font-medium">${{p.Patient_ID}}</td>
                    <td class="px-4 py-2.5 font-medium text-slate-900">${{p.Name}}</td>
                    <td class="px-4 py-2.5 text-slate-500">${{p.Age}} / ${{p.Gender[0]}}</td>
                    <td class="px-4 py-2.5 font-medium text-blue-700">${{p.Medical_Condition}}</td>
                    <td class="px-4 py-2.5 text-slate-600">${{p.Hospital.replace("Hospital", "").trim()}}</td>
                    <td class="px-4 py-2.5 text-slate-600">${{p.Doctor.split("(")[0].trim()}}</td>
                    <td class="px-4 py-2.5">${{admBadge}}</td>
                    <td class="px-4 py-2.5 font-semibold text-slate-700">${{p.Length_of_Stay}}d</td>
                    <td class="px-4 py-2.5">${{testBadge}}</td>
                    <td class="px-4 py-2.5">${{p.Readmission === 'Yes' ? '⚠️ Yes' : 'No'}}</td>
                    <td class="px-4 py-2.5 font-bold text-slate-900 font-mono">$${{p.Billing_Amount.toLocaleString()}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // Clinical Risk Predictor Logic
        function updatePrediction() {{
            const age = parseInt(document.getElementById('predAge').value);
            document.getElementById('ageDisplay').textContent = age;

            const condition = document.getElementById('predCondition').value;
            const adm = document.getElementById('predAdmission').value;
            const test = document.getElementById('predTest').value;

            let score = 20;
            if (age >= 75) score += 25;
            else if (age >= 60) score += 15;
            else if (age >= 45) score += 8;

            const condWeights = {{
                "Cancer": 25, "Cardiovascular Disease": 22, "Chronic Kidney Disease": 20,
                "Pneumonia": 15, "Diabetes": 10, "Hypertension": 8, "Asthma": 6, "Arthritis": 4
            }};
            score += condWeights[condition] || 10;

            if (adm === 'Emergency') score += 20;
            else if (adm === 'Urgent') score += 10;
            else score += 2;

            if (test === 'Abnormal') score += 18;
            else if (test === 'Inconclusive') score += 8;

            score = Math.min(100, Math.max(5, score));

            document.getElementById('riskScoreNumber').textContent = score;

            let cat = "", badgeClass = "", stay = "", recs = [];
            if (score >= 75) {{
                cat = "CRITICAL RISK";
                badgeClass = "bg-rose-500/20 text-rose-300 border-rose-500/40";
                stay = "10 - 18 days";
                recs = [
                    "Immediate ICU / Step-Down observation advised.",
                    "Continuous vitals monitoring & specialist consult within 2 hours.",
                    "Schedule follow-up pathology tests and multidisciplinary review.",
                    "Flag for early readmission prevention protocol."
                ];
            }} else if (score >= 50) {{
                cat = "HIGH RISK";
                badgeClass = "bg-amber-500/20 text-amber-300 border-amber-500/40";
                stay = "6 - 11 days";
                recs = [
                    "Assign to designated inpatient monitoring ward.",
                    "Daily lab reviews and vitals screening every 4 hours.",
                    "Evaluate medication adjustment and secondary complications.",
                    "Care coordinator assigned for post-discharge home care."
                ];
            }} else if (score >= 30) {{
                cat = "MODERATE RISK";
                badgeClass = "bg-yellow-500/20 text-yellow-300 border-yellow-500/40";
                stay = "3 - 6 days";
                recs = [
                    "Standard inpatient medical care protocol.",
                    "Routine diagnostic testing and clinical checks every 8 hours.",
                    "Prepare patient education on dietary and medication adherence."
                ];
            }} else {{
                cat = "LOW RISK";
                badgeClass = "bg-emerald-500/20 text-emerald-300 border-emerald-500/40";
                stay = "1 - 3 days";
                recs = [
                    "Standard outpatient or short-stay observation.",
                    "Discharge plan viable once vitals remain stable for 24h.",
                    "Routine 2-week outpatient follow-up consultation."
                ];
            }}

            const badgeElem = document.getElementById('riskBadge');
            badgeElem.textContent = cat;
            badgeElem.className = `px-3 py-1 rounded-full text-xs font-bold border ${{badgeClass}}`;
            document.getElementById('stayEst').textContent = stay;

            const recList = document.getElementById('recommendationsList');
            recList.innerHTML = '';
            recs.forEach(r => {{
                const li = document.createElement('li');
                li.textContent = r;
                recList.appendChild(li);
            }});
        }}

        // Modal Helpers
        function openModal(id) {{
            document.getElementById(id).classList.remove('hidden');
        }}
        function closeModal(id) {{
            document.getElementById(id).classList.add('hidden');
        }}

        // CSV Export
        function downloadCSV() {{
            if (filteredPatients.length === 0) return;
            const headers = Object.keys(filteredPatients[0]).join(",");
            const rows = filteredPatients.map(p => Object.values(p).map(v => `"${{v}}"`).join(","));
            const csvContent = "data:text/csv;charset=utf-8," + [headers, ...rows].join("\\n");
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", `patient_analytics_data_${{Date.now()}}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}
    </script>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("index.html built successfully!")

if __name__ == "__main__":
    build()
