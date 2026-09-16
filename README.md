# Tên đề tài
Xây dựng module kiểm tra thị giác tự động làm công cụ phản hồi trực quan cho hệ thống Agentic AI

# Kiến trúc & Pipeline Xử lý Ảnh (Core Engine)
```text
[Baseline Image] + [Current Captured Image]
       │
       ▼
 1. Tiền xử lý (Preprocessing)
    ├── Đồng bộ kích thước & Cắt vùng quan tâm (ROI / Cropping)
    └── Khử nhiễu & Lọc Anti-aliasing (Bilateral / Gaussian Blur / Median Filter)
       │
       ▼
 2. Đo lường biến dạng & Sai khác (Diff Analysis)
    ├── Pixel-by-Pixel Absolute Difference (|I_current - I_baseline|)
    └── Đo tương đồng cấu trúc thị giác (SSIM Index)
       │
       ▼
 3. Xử lý hình thái học (Morphological Operations)
    ├── Phân đoạn nhị phân (Otsu's / Adaptive Thresholding)
    └── Dilation & Closing (Gom các cụm pixel rời rạc thành khối component)
       │
       ▼
 4. Định vị & Trích xuất đặc trưng (Feature Extraction)
    ├── Tìm đường bao (cv2.findContours) & Tạo khung (cv2.boundingRect)
    └── Phân loại vùng giao diện (Header, Footer, Main Content) & Mức độ (Critical / Warning)
       │
       ▼
 5. Đóng gói đa mục đích
    ├── Xuất JSON có trường `agent_prompt_summary` (Dành cho Agentic AI)
    └── Xuất Ảnh Heatmap Overlay (Dành cho Báo cáo Chuyên đề & Đồ án)
```

# Cấu trúc Thư mục Dự án
```text
visual-inspection-module/
├── pyproject.toml
├── README.md
├── src/
│   └── visual_checker/
│       ├── __init__.py
│       ├── core/
│       │   ├── preprocessor.py   # Lọc nhiễu, căn chỉnh kích thước (Geometric & Spatial Filter)
│       │   ├── comparator.py     # Tính toán SSIM, Pixel Diff & Color Distance
│       │   ├── morphology.py     # Phép giãn (Dilation), đóng (Closing), Thresholding
│       │   └── detector.py       # Trích xuất Contours, Bounding Boxes & phân loại layout
│       ├── schemas/
│       │   └── report.py         # Pydantic Model (Bbox, AffectedComponent, VisualInspectionResult)
│       ├── formatters/
│       │   └── prompt_builder.py # Sinh agent_prompt_summary súc tích cho LLM
│       ├── engine.py             # Interface chính kết nối toàn bộ pipeline (Facade Pattern)
│       └── api/
│           └── server.py         # REST API FastAPI (Phục vụ gọi từ Agent Loop)
├── demo/
│   └── app.py                    # Giao diện UI tương tác bằng Streamlit
├── tests/
│   └── test_comparison.py
└── data/
    ├── baselines/
    ├── current/
    └── diffs/
```

# Kế hoạch Triển khai Chi tiết
# visual-inspection-module
