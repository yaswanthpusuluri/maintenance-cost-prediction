import streamlit as st
import requests
import pandas as pd
from pathlib import Path




# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Maintenance Cost Prediction",
    page_icon="🏭",
    layout="centered"
)

st.title("🏭 Maintenance Cost Prediction")

# -----------------------------
# Load Dataset
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed_data.csv"

df = pd.read_csv(DATA_PATH)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📊 Sample Dataset")

# Keep selected sample after rerun
if "sample" not in st.session_state:
    st.session_state.sample = None

# Sample rows
# High Repair Cost Samples (Top 10%)
high_samples = df.nlargest(
    max(1, int(len(df) * 0.10)),
    "estimated_repair_cost"
)

# Low Repair Cost Samples (Bottom 10%)
low_samples = df.nsmallest(
    max(1, int(len(df) * 0.10)),
    "estimated_repair_cost"
)

# Buttons
# -----------------------------
# Sidebar Buttons
# -----------------------------

if st.sidebar.button("🔴 High Repair Cost"):

    # Every click returns a different high-cost sample
    st.session_state.sample = high_samples.sample(n=1).iloc[0]

if st.sidebar.button("🟢 Low Repair Cost"):

    # Every click returns a different low-cost sample
    st.session_state.sample = low_samples.sample(n=1).iloc[0]

if st.sidebar.button("🎲 Random Sample"):

    # Every click returns a completely random sample
    st.session_state.sample = df.sample(n=1).iloc[0]

sample = st.session_state.sample

# Sidebar Preview
if sample is not None:

    st.sidebar.markdown("---")

    st.sidebar.write(
        f"**Expected Repair Cost:** ₹ {sample['estimated_repair_cost']:.2f}"
    )

    st.sidebar.write(
        f"**Machine Type:** {sample['machine_type']}"
    )

    st.sidebar.write(
        f"**Failure Type:** {sample['failure_type']}"
    )

# -----------------------------
# Input Fields
# -----------------------------

machine_types = [
    "CNC",
    "Pump",
    "Compressor",
    "Robotic Arm"
]

operating_modes = [
    "idle",
    "normal",
    "peak"
]

failure_types = sorted(
    df["failure_type"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

machine_type = st.selectbox(
    "Machine Type",
    machine_types,
    index=machine_types.index(sample["machine_type"])
    if sample is not None else 0
)

temperature_motor = st.number_input(
    "Motor Temperature",
    value=float(sample["temperature_motor"])
    if sample is not None else 45.0
)

rpm = st.number_input(
    "RPM",
    value=float(sample["rpm"])
    if sample is not None else 900.0
)

operating_mode = st.selectbox(
    "Operating Mode",
    operating_modes,
    index=operating_modes.index(sample["operating_mode"])
    if sample is not None else 0
)

hours_since_maintenance = st.number_input(
    "Hours Since Maintenance",
    value=float(sample["hours_since_maintenance"])
    if sample is not None else 250.0
)

rul_hours = st.number_input(
    "Remaining Useful Life (RUL Hours)",
    value=float(sample["rul_hours"])
    if sample is not None else 60.0
)

failure_index = 0

if sample is not None:
    value = str(sample["failure_type"])

    if value in failure_types:
        failure_index = failure_types.index(value)

failure_type = st.selectbox(
    "Failure Type",
    failure_types,
    index=failure_index
)

# -----------------------------
# Prediction
# -----------------------------

if st.button("Predict Repair Cost"):

    payload = {
        "machine_type": machine_type,
        "temperature_motor": temperature_motor,
        "rpm": rpm,
        "operating_mode": operating_mode,
        "hours_since_maintenance": hours_since_maintenance,
        "rul_hours": rul_hours,
        "failure_type": failure_type
    }

    try:

        response = requests.post(
            "http://backend:8000/predict",
            json=payload
        )

        if response.status_code == 200:

            prediction = response.json()

            st.success(
                f"💰 Estimated Repair Cost : ₹ {prediction['Estimated Repair Cost']:.2f}"
            )

        else:

            st.error("Prediction Failed.")

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Unable to connect to FastAPI.\n\nPlease start the backend server first."
        )


st.markdown("""
<style>

/* ===========================
   GOOGLE FONT
=========================== */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family: 'Poppins', sans-serif;
}

/* ===========================
   BACKGROUND
=========================== */

.stApp{
    background: linear-gradient(
        135deg,
        #07111f 0%,
        #102542 45%,
        #16345d 100%
    );
}


/* ===========================
   MAIN CONTENT
=========================== */

.main .block-container{

    background: rgba(255,255,255,0.06);

    backdrop-filter: blur(18px);

    border-radius:25px;

    padding:35px;

    margin-top:20px;

    border:1px solid rgba(255,255,255,.15);

}


/* ===========================
   TITLE
=========================== */

h1{

    color:white;

    text-align:center;

    font-size:45px;

    font-weight:800;

    margin-bottom:30px;

    letter-spacing:.5px;

}


/* ===========================
   LABELS
=========================== */

label{

    color:white !important;

    font-size:17px !important;

    font-weight:600 !important;

}


/* ===========================
   INPUT BOXES
=========================== */

.stNumberInput input{

    background:#23344d !important;

    color:white !important;

    border-radius:14px !important;

    border:2px solid #4ea8ff !important;

    height:50px;

    font-size:16px;

}


/* ===========================
   SELECT BOX
=========================== */

div[data-baseweb="select"]{

    background:#23344d !important;

    border-radius:14px !important;

    border:2px solid #4ea8ff !important;

}

div[data-baseweb="select"] *{

    color:white !important;

}


/* ===========================
   BUTTON
=========================== */

.stButton>button{

    width:100%;

    height:58px;

    border:none;

    border-radius:15px;

    background:linear-gradient(
        90deg,
        #1d4ed8,
        #2563eb,
        #3b82f6
    );

    color:white;

    font-size:19px;

    font-weight:700;

    transition:.35s;

    box-shadow:0 10px 25px rgba(59,130,246,.35);

}


.stButton>button:hover{

    transform:translateY(-2px);

    box-shadow:0 15px 30px rgba(59,130,246,.45);

}


/* ===========================
   SIDEBAR
=========================== */

[data-testid="stSidebar"]{

    background:linear-gradient(
        180deg,
        #071528,
        #102542,
        #16345d
    );

    border-right:1px solid rgba(255,255,255,.08);

}


[data-testid="stSidebar"] *{

    color:white;

}


/* ===========================
   SIDEBAR TITLE
=========================== */

[data-testid="stSidebar"] h2{

    font-size:30px;

    font-weight:700;

}


/* ===========================
   SIDEBAR BUTTONS
=========================== */

[data-testid="stSidebar"] .stButton>button{

    background:#274260;

    border:none;

    height:48px;

    border-radius:12px;

    color:white;

    font-weight:600;

    font-size:16px;

    transition:.3s;

}


[data-testid="stSidebar"] .stButton>button:hover{

    background:#3b82f6;

}


/* ===========================
   SUCCESS BOX
=========================== */

div[data-testid="stAlert"]{

    background:#0f5132 !important;

    color:white !important;

    border-radius:15px;

    border:none;

    font-size:18px;

    font-weight:700;

}


/* ===========================
   METRIC STYLE
=========================== */

[data-testid="metric-container"]{

    background:#23344d;

    border-radius:15px;

    padding:15px;

    border:1px solid rgba(255,255,255,.12);

}


/* ===========================
   HORIZONTAL LINE
=========================== */

hr{

    border-color:rgba(255,255,255,.15);

}


/* ===========================
   SCROLLBAR
=========================== */

::-webkit-scrollbar{

    width:8px;

}

::-webkit-scrollbar-thumb{

    background:#4ea8ff;

    border-radius:20px;

}


/* ===========================
   REMOVE STREAMLIT HEADER
=========================== */

header{

    background:transparent;

}


footer{

    visibility:hidden;

}

</style>
""", unsafe_allow_html=True)      