import streamlit as st
from PIL import Image

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Accident Detection System",
    page_icon="🚗",
    layout="wide"
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("⚙️ Settings")

mode = st.sidebar.radio(
    "Select Detection Mode",
    (
        "📂 Upload Video",
        "📷 Live Webcam"
    )
)

confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.1,
    1.0,
    0.5,
    0.05
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    **Project**

    Accident Detection &
    Alert System

    Developed using:
    - YOLOv4-Tiny
    - OpenCV
    - Python
    - Streamlit
    """
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🚗 Accident Detection & Alert System")

st.markdown(
"""
This application detects **vehicles and road accidents**
using **YOLOv4-Tiny** and Computer Vision.
"""
)

st.markdown("---")

# -----------------------------
# MAIN AREA
# -----------------------------

left, right = st.columns([3,1])

with left:

    st.subheader("Detection Window")

    frame_placeholder = st.empty()

with right:

    st.subheader("System Status")

    status = st.empty()

    alert = st.empty()

    status.success("System Ready")

# -----------------------------
# UPLOAD VIDEO
# -----------------------------

if mode == "📂 Upload Video":

    uploaded_file = st.file_uploader(
        "Upload a Video",
        type=["mp4","avi","mov"]
    )

    if uploaded_file is not None:

        st.success("Video Uploaded Successfully ✅")

        if st.button("▶ Start Detection"):

            status.info("Processing Video...")

            # Add your detection code here

            alert.success("No Accident Detected")

# -----------------------------
# WEBCAM
# -----------------------------

else:

    st.write("### Webcam Detection")

    start = st.button("📷 Start Webcam")

    stop = st.button("⏹ Stop Webcam")

    if start:

        status.info("Starting Webcam...")

        # Add webcam detection code here

        alert.success("Monitoring Traffic...")

# -----------------------------
# FOOTER
# -----------------------------

st.markdown("---")

st.markdown(
"""
### Technologies Used

- Python
- OpenCV
- YOLOv4-Tiny
- Streamlit
- NumPy
"""
)