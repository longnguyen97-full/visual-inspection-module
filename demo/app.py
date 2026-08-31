import sys
import json
import time
from pathlib import Path
import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Ensure src is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

WORKSPACE_DIR = ROOT_DIR.parent
DATASET_DIR = WORKSPACE_DIR / "dataset"

from visual_checker.engine import VisualInspectionEngine

# Configure page
st.set_page_config(
    page_title="Visual Inspection Module | Demo",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
    }
    .metric-box {
        background-color: #1E293B;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #334155;
        text-align: center;
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #38BDF8;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-pass {
        background-color: #065F46;
        color: #34D399;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .badge-fail {
        background-color: #7F1D1D;
        color: #F87171;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Load ground truth if exists
@st.cache_data
def load_ground_truth():
    gt_file = DATASET_DIR / "ground_truth.json"
    if gt_file.exists():
        with open(gt_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

gt_data = load_ground_truth()

# Initialize Engine
@st.cache_resource
def get_engine():
    return VisualInspectionEngine(
        ssim_threshold=0.995,
        diff_threshold_val=25,
        min_defect_area=40,
        filter_noise=True
    )

engine = get_engine()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/visible--v2.png", width=70)
    st.markdown("### ⚙️ Engine Parameters")
    
    ssim_thresh = st.slider("SSIM Threshold", min_value=0.90, max_value=1.00, value=0.995, step=0.005)
    diff_thresh = st.slider("Pixel Diff Threshold", min_value=10, max_value=80, value=25, step=5)
    min_area = st.slider("Min Defect Area (px)", min_value=10, max_value=200, value=40, step=5)
    filter_noise = st.checkbox("Anti-Aliasing Filter", value=True)
    
    engine.ssim_threshold = ssim_thresh
    engine.diff_threshold_val = diff_thresh
    engine.min_defect_area = min_area
    engine.filter_noise = filter_noise
    
    st.divider()
    st.markdown("#### 📊 Dataset Info")
    st.markdown("• **Total Samples:** 50 Image Pairs (100 images)")
    st.markdown("• **Scenario 1:** 25 Baseline Identical Pairs")
    st.markdown("• **Scenario 2:** 25 Injected Bug Pairs")
    st.markdown("• **Resolution:** 1000 x 800 px")

# Header
st.markdown('<div class="main-header">Visual Inspection & UI Regression Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated UI Defect Localization via OpenCV, SSIM & Morphological Operations for Agentic AI</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🎯 1. Dataset Benchmark Explorer", "📤 2. Custom Image Inspection", "📈 3. Full Benchmark & Metrics"])

# ==========================================
# TAB 1: DATASET BENCHMARK EXPLORER
# ==========================================
with tab1:
    col_sel1, col_sel2 = st.columns([1, 2])
    with col_sel1:
        scenario = st.selectbox(
            "Select Scenario",
            options=["Scenario 2 (25 Injected UI Bugs)", "Scenario 1 (25 Identical Pairs / No Bug)"]
        )
    with col_sel2:
        sample_idx = st.selectbox(
            "Select Sample",
            options=list(range(1, 26)),
            format_func=lambda x: f"Sample {x:02d} - {gt_data['scenario_2_mutations'][x-1]['name']} [{gt_data['scenario_2_mutations'][x-1]['category']}]" if gt_data and scenario.startswith("Scenario 2") else f"Sample {x:02d} (Baseline vs Baseline)"
        )

    sc_folder = "scenario_2" if scenario.startswith("Scenario 2") else "scenario_1"
    filename = f"sample_{sample_idx:02d}.png"
    base_path = DATASET_DIR / sc_folder / "baseline" / filename
    curr_path = DATASET_DIR / sc_folder / "current" / filename

    # Metadata card for Scenario 2
    if scenario.startswith("Scenario 2") and gt_data:
        meta = gt_data["scenario_2_mutations"][sample_idx - 1]
        st.info(f"**🏷️ Ground Truth Mutation:** `{meta['name']}` | **Category:** `{meta['category']}` | **Vị trí/Mô tả:** {meta['description_vi']}")

    if base_path.exists() and curr_path.exists():
        # Run inspection
        res, annotated_img, heatmap_img = engine.compare(base_path, curr_path)
        
        # Display Metrics
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Status</div>
                <div style="margin-top: 6px;">{'<span class="badge-fail">DEFECT FOUND</span>' if res.has_defect else '<span class="badge-pass">PERFECT MATCH</span>'}</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">SSIM Index</div>
                <div class="metric-val">{res.ssim_score:.4f}</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Defects Detected</div>
                <div class="metric-val">{res.defect_count}</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Pixel Diff Ratio</div>
                <div class="metric-val">{res.diff_pixel_ratio*100:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        with m5:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Latency</div>
                <div class="metric-val">{res.execution_time_ms:.1f}ms</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Image Comparison Grid
        col_img1, col_img2, col_img3 = st.columns(3)
        with col_img1:
            st.markdown("#### 1. Baseline Image (Chuẩn)")
            st.image(str(base_path), use_container_width=True)
        with col_img2:
            st.markdown("#### 2. Difference Heatmap")
            heatmap_rgb = cv2.cvtColor(heatmap_img, cv2.COLOR_BGR2RGB)
            st.image(heatmap_rgb, use_container_width=True)
        with col_img3:
            st.markdown("#### 3. Detected Defect Localization")
            annotated_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
            st.image(annotated_rgb, use_container_width=True)

        # LLM Agent Section
        st.divider()
        st.markdown("### 🤖 Agentic AI Integration Output")
        st.code(res.agent_prompt_summary, language="markdown")
        
        with st.expander("🔍 View Raw JSON Structured Payload"):
            st.json(res.model_dump())
    else:
        st.error(f"Images not found at `{base_path}` or `{curr_path}`. Please ensure dataset is generated.")

# ==========================================
# TAB 2: CUSTOM IMAGE INSPECTION
# ==========================================
with tab2:
    st.markdown("### Tải lên 2 ảnh bất kỳ để kiểm định trực tiếp")
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        up_base = st.file_uploader("Upload Baseline Image (Ảnh gốc)", type=["png", "jpg", "jpeg", "webp"])
    with col_up2:
        up_curr = st.file_uploader("Upload Current Image (Ảnh cần kiểm tra)", type=["png", "jpg", "jpeg", "webp"])

    if up_base and up_curr:
        bytes_base = up_base.read()
        bytes_curr = up_curr.read()
        
        res, annotated_img, heatmap_img = engine.compare(bytes_base, bytes_curr)
        
        # Display Metrics
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Visual Status", "DEFECT DETECTED" if res.has_defect else "MATCH / PASS")
        with m2:
            st.metric("SSIM Score", f"{res.ssim_score:.4f}")
        with m3:
            st.metric("Defects Located", res.defect_count)
        with m4:
            st.metric("Processing Time", f"{res.execution_time_ms:.1f} ms")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("#### Baseline")
            st.image(Image.open(up_base), use_container_width=True)
        with col2:
            st.markdown("#### Heatmap")
            st.image(cv2.cvtColor(heatmap_img, cv2.COLOR_BGR2RGB), use_container_width=True)
        with col3:
            st.markdown("#### Localized Defect")
            st.image(cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB), use_container_width=True)

        st.markdown("#### 🤖 LLM Prompt Summary")
        st.info(res.agent_prompt_summary)

# ==========================================
# TAB 3: FULL DATASET BENCHMARK & METRICS
# ==========================================
with tab3:
    st.markdown("### 📊 Đánh giá định lượng trên toàn bộ 50 cặp ảnh Dataset")
    st.markdown("Chạy kiểm thử hàng loạt để đo lường các chỉ số thị giác máy tính: **Accuracy, Precision, Recall, F1-Score, False Positive Rate (FPR)**.")

    if st.button("🚀 Run Full 50-Pair Benchmark", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results_s1 = []
        results_s2 = []
        total_time = 0.0

        # Scenario 1 (Expected: NO DEFECT)
        for i in range(1, 26):
            fn = f"sample_{i:02d}.png"
            b = DATASET_DIR / "scenario_1" / "baseline" / fn
            c = DATASET_DIR / "scenario_1" / "current" / fn
            res, _, _ = engine.compare(b, c)
            results_s1.append(res)
            total_time += res.execution_time_ms
            progress_bar.progress(i / 50)
            status_text.text(f"Processing Scenario 1: Sample {i}/25...")

        # Scenario 2 (Expected: HAS DEFECT)
        for i in range(1, 26):
            fn = f"sample_{i:02d}.png"
            b = DATASET_DIR / "scenario_2" / "baseline" / fn
            c = DATASET_DIR / "scenario_2" / "current" / fn
            res, _, _ = engine.compare(b, c)
            results_s2.append(res)
            total_time += res.execution_time_ms
            progress_bar.progress((25 + i) / 50)
            status_text.text(f"Processing Scenario 2: Sample {i}/25...")

        progress_bar.progress(100)
        status_text.text("Benchmark Finished!")

        # Metrics calculation
        # TP: S2 predicted defect
        # FN: S2 predicted no defect
        # TN: S1 predicted no defect
        # FP: S1 predicted defect
        tp = sum(1 for r in results_s2 if r.has_defect)
        fn = sum(1 for r in results_s2 if not r.has_defect)
        tn = sum(1 for r in results_s1 if not r.has_defect)
        fp = sum(1 for r in results_s1 if r.has_defect)

        total = tp + tn + fp + fn
        accuracy = (tp + tn) / total if total else 0
        precision = tp / (tp + fp) if (tp + fp) else 0
        recall = tp / (tp + fn) if (tp + fn) else 0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0
        avg_latency = total_time / 50

        # Display Metrics
        st.markdown("#### 🏆 Benchmark Summary Results")
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Accuracy", f"{accuracy*100:.1f}%")
        k2.metric("Precision", f"{precision*100:.1f}%")
        k3.metric("Recall", f"{recall*100:.1f}%")
        k4.metric("F1-Score", f"{f1*100:.1f}%")
        k5.metric("Avg Latency", f"{avg_latency:.1f} ms")

        # Confusion Matrix Table
        st.markdown("#### 🔢 Confusion Matrix")
        st.table({
            "Actual / Predicted": ["Actual Defect (Scenario 2)", "Actual Identical (Scenario 1)"],
            "Predicted Defect": [f"True Positive (TP) = {tp}", f"False Positive (FP) = {fp}"],
            "Predicted No Defect": [f"False Negative (FN) = {fn}", f"True Negative (TN) = {tn}"]
        })
