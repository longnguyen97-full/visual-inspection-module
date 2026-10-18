import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def update_presentation():
    pptx_path = "ChuyenDeTotNghiep.pptx"
    prs = Presentation(pptx_path)
    print(f"[*] Loaded {pptx_path} with {len(prs.slides)} slides.")

    # Color Palette
    COLOR_PRIMARY = RGBColor(0, 51, 102)     # Deep Navy
    COLOR_SECONDARY = RGBColor(0, 102, 204)  # Accent Blue
    COLOR_TEXT_DARK = RGBColor(15, 23, 42)   # Slate 900
    COLOR_TEXT_MUTED = RGBColor(71, 85, 105) # Slate 600
    COLOR_GREEN = RGBColor(16, 185, 129)     # Emerald Green
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_CARD_BG = RGBColor(248, 250, 252)  # Light Slate BG
    COLOR_CARD_BORDER = RGBColor(226, 232, 240)

    # Helper: update paragraph text and styling
    def format_p(p, text, font_name="Segoe UI", size_pt=11, bold=False, color=COLOR_TEXT_DARK, align=None):
        p.text = text
        if align is not None:
            p.alignment = align
        if len(p.runs) > 0:
            run = p.runs[0]
            run.font.name = font_name
            run.font.size = Pt(size_pt)
            run.font.bold = bold
            if color:
                run.font.color.rgb = color

    # =========================================================================
    # 1. Slide 9: 1.3 Thách thức và khó khăn
    # =========================================================================
    slide_9 = prs.slides[8]
    print("[*] Updating Slide 9: 1.3 Thách thức và khó khăn...")
    # Shape 14: BBox explosion solution
    if len(slide_9.shapes) > 14 and slide_9.shapes[14].has_text_frame:
        tf = slide_9.shapes[14].text_frame
        for p in tf.paragraphs:
            if "2.92 Bbox/lỗi" in p.text:
                format_p(p, "-> Giải pháp: Toán tử Hình thái học Đóng & Giãn ΦK gom cụm về 2.87 Bbox/lỗi.",
                         size_pt=10.5, color=COLOR_PRIMARY, bold=True)
    # Shape 18: Latency constraint solution
    if len(slide_9.shapes) > 18 and slide_9.shapes[18].has_text_frame:
        tf = slide_9.shapes[18].text_frame
        for p in tf.paragraphs:
            if "138.5 ms" in p.text:
                format_p(p, "-> Giải pháp: Pipeline Thị giác máy tính tất định chạy siêu tốc 171.6 ms trên CPU thường.",
                         size_pt=10.5, color=COLOR_PRIMARY, bold=True)

    # =========================================================================
    # 2. Slide 17: 2.4. Xử lý Hình thái học Gom cụm ΦK, Suzuki-Abe
    # =========================================================================
    slide_17 = prs.slides[16]
    print("[*] Updating Slide 17: 2.4. Xử lý Hình thái học...")
    if len(slide_17.shapes) > 13 and slide_17.shapes[13].has_text_frame:
        tf = slide_17.shapes[13].text_frame
        for p in tf.paragraphs:
            if "49.32 → 2.92" in p.text:
                format_p(p, "45.61 → 2.87", font_name="Segoe UI", size_pt=16, bold=True, color=COLOR_PRIMARY)
            elif "49.32 xuống còn 2.92" in p.text:
                format_p(p, "Toán tử ΦK giúp giảm số lượng Bounding Box rác trung bình từ 45.61 xuống còn 2.87 bbox/lỗi, bảo vệ an toàn Context Window của LLM Agent.",
                         font_name="Segoe UI", size_pt=10.5, color=COLOR_TEXT_MUTED, bold=False)

    # =========================================================================
    # 3. Slide 19: 3. KẾT QUẢ THỰC NGHIỆM (Agenda)
    # =========================================================================
    slide_19 = prs.slides[18]
    print("[*] Updating Slide 19: Agenda Chương 3...")
    if len(slide_19.shapes) > 3 and slide_19.shapes[3].has_text_frame:
        tf = slide_19.shapes[3].text_frame
        items = [
            "Dataset (Mở rộng 200 cặp & Phân chia Split khoa học)",
            "Phương pháp đánh giá và metric",
            "Kết quả thu được và ma trận nhầm lẫn",
            "Ví dụ thực nghiệm trực quan",
            "Ablation study (Đánh giá thực nghiệm 5 cấu hình)",
            "Thực nghiệm đối chứng Agentic AI (Trước vs Sau khi nhận Output)"
        ]
        # Clear extra paragraphs or adjust
        while len(tf.paragraphs) < len(items):
            tf.add_paragraph()
        for idx, item in enumerate(items):
            format_p(tf.paragraphs[idx], item, font_name="Segoe UI", size_pt=15, bold=False, color=COLOR_TEXT_DARK)

    # =========================================================================
    # 4. Slide 20: 3.1. Dataset
    # =========================================================================
    slide_20 = prs.slides[19]
    print("[*] Updating Slide 20: 3.1. Dataset...")
    # Shape 4: Scenario 1 Header
    if len(slide_20.shapes) > 4 and slide_20.shapes[4].has_text_frame:
        format_p(slide_20.shapes[4].text_frame.paragraphs[0], "SCENARIO 1: 100 CẶP ÂM TÍNH (50%)",
                 font_name="Segoe UI", size_pt=11, bold=True, color=COLOR_WHITE)
    # Shape 5: Scenario 1 Body
    if len(slide_20.shapes) > 5 and slide_20.shapes[5].has_text_frame:
        tf = slide_20.shapes[5].text_frame
        p_texts_s1 = [
            ("Kiểm định Tính Ổn định & Đo False Positive Rate", 12, True, COLOR_PRIMARY),
            ("* Đối tượng so sánh: Ibase vs Ibase (ảnh chuẩn so sánh với chính nó).", 10.5, False, COLOR_TEXT_MUTED),
            ("* Mục tiêu khoa học: Kiểm chứng hệ thống không sinh cờ lỗi rác khi không có sự cố.", 10.5, False, COLOR_TEXT_MUTED),
            ("* Kết quả thực nghiệm: 100/100 cặp đều dự đoán PERFECT MATCH, FPR = 0.0%.", 10.5, True, COLOR_PRIMARY)
        ]
        while len(tf.paragraphs) < len(p_texts_s1):
            tf.add_paragraph()
        for i, (txt, sz, bld, col) in enumerate(p_texts_s1):
            format_p(tf.paragraphs[i], txt, font_name="Segoe UI", size_pt=sz, bold=bld, color=col)

    # Shape 7: Scenario 2 Header
    if len(slide_20.shapes) > 7 and slide_20.shapes[7].has_text_frame:
        format_p(slide_20.shapes[7].text_frame.paragraphs[0], "SCENARIO 2: 100 CẶP DƯƠNG TÍNH (50%)",
                 font_name="Segoe UI", size_pt=11, bold=True, color=COLOR_WHITE)
    # Shape 8: Scenario 2 Body
    if len(slide_20.shapes) > 8 and slide_20.shapes[8].has_text_frame:
        tf = slide_20.shapes[8].text_frame
        p_texts_s2 = [
            ("6 Nhóm Đột biến Tiêm lỗi có Kiểm soát (Mở rộng)", 12, True, COLOR_PRIMARY),
            ("• 1. Color Change (20 cặp): Đổi màu nút bấm, màu nền, màu text, hover state.", 10, False, COLOR_TEXT_DARK),
            ("• 2. Layout Shift (20 cặp): Lệch component 20-50px sang trái/phải/dưới.", 10, False, COLOR_TEXT_DARK),
            ("• 3. Missing Element (20 cặp): Mất nút CTA Sign Up, mất icon, mất Trust Card.", 10, False, COLOR_TEXT_DARK),
            ("• 4. Text Modification (15 cặp): Sửa tiêu đề Hero, tràn văn bản (overflow).", 10, False, COLOR_TEXT_DARK),
            ("• 5. Size Distortion (15 cặp): Co méo ảnh banner, vỡ tỉ lệ 30% - 60%.", 10, False, COLOR_TEXT_DARK),
            ("• 6. Compound Regression (10 cặp): Tổ hợp nhiều lỗi biến dạng phức hợp cùng lúc.", 10, False, COLOR_TEXT_DARK)
        ]
        while len(tf.paragraphs) < len(p_texts_s2):
            tf.add_paragraph()
        for i, (txt, sz, bld, col) in enumerate(p_texts_s2):
            format_p(tf.paragraphs[i], txt, font_name="Segoe UI", size_pt=sz, bold=bld, color=col)

    # Shape 10: Methodology & Split
    if len(slide_20.shapes) > 10 and slide_20.shapes[10].has_text_frame:
        tf = slide_20.shapes[10].text_frame
        p_texts_s3 = [
            ("PHÂN CHIA SPLIT KHOA HỌC & ĐẶC THÙ THUẬT TOÁN (TRAINING-FREE)", 11, True, COLOR_PRIMARY),
            ("* Phân chia tập dữ liệu: Calibration Set (25% - 50 cặp, mẫu 01-25) hiệu chuẩn siêu tham số; Held-out Test Set (75% - 150 cặp, mẫu 26-100) đánh giá mù độc lập, chứng minh tính tổng quát hóa không overfitting.", 9.5, False, COLOR_TEXT_MUTED),
            ("* Đặc thù thuật toán: Pipeline thị giác giải tích phi tham số (non-parametric), Training-free (không học trọng số), Zero-shot LLM grounding (không cần fine-tune model) trên 200 cặp ảnh chuẩn hóa 1000 × 800px.", 9.5, False, COLOR_TEXT_MUTED)
        ]
        while len(tf.paragraphs) < len(p_texts_s3):
            tf.add_paragraph()
        for i, (txt, sz, bld, col) in enumerate(p_texts_s3):
            format_p(tf.paragraphs[i], txt, font_name="Segoe UI", size_pt=sz, bold=bld, color=col)

    # =========================================================================
    # 5. Slide 21: 3.2. Phương pháp đánh giá và metric
    # =========================================================================
    slide_21 = prs.slides[20]
    print("[*] Updating Slide 21: 3.2. Phương pháp đánh giá và metric...")
    # Shape 5 (Accuracy)
    if len(slide_21.shapes) > 5 and slide_21.shapes[5].has_text_frame:
        p2 = slide_21.shapes[5].text_frame.paragraphs[2]
        format_p(p2, "Đo lường tỷ lệ dự đoán chính xác trên cả 200 cặp ảnh (hoặc 150 cặp Test Set).", size_pt=9.5, color=COLOR_TEXT_MUTED)
    # Shape 17 (Bbox/Bug)
    if len(slide_21.shapes) > 17 and slide_21.shapes[17].has_text_frame:
        p2 = slide_21.shapes[17].text_frame.paragraphs[2]
        format_p(p2, "Đo mức độ phân mảnh; tiệm cận 1.0 → 3.0 là tối ưu. Thực nghiệm: 2.87 BBox/lỗi (2.85 trên Test Set).", size_pt=9.5, color=COLOR_TEXT_MUTED)
    # Shape 20 (Latency)
    if len(slide_21.shapes) > 20 and slide_21.shapes[20].has_text_frame:
        p2 = slide_21.shapes[20].text_frame.paragraphs[2]
        format_p(p2, "Đảm bảo tính thời gian thực cho CI/CD. Thực nghiệm đạt: 171.6 ms trên CPU thường.", size_pt=9.5, color=COLOR_TEXT_MUTED)
        p3 = slide_21.shapes[20].text_frame.paragraphs[3]
        format_p(p3, "Yêu cầu: < 200 ms", size_pt=9.5, color=COLOR_PRIMARY, bold=True)

    # =========================================================================
    # 6. Slide 22: 3.3. Kết quả thu được và ma trận nhầm lẫn
    # =========================================================================
    slide_22 = prs.slides[21]
    print("[*] Updating Slide 22: 3.3. Kết quả thu được và ma trận nhầm lẫn...")
    # Shape 5: Accuracy detail
    if len(slide_22.shapes) > 5 and slide_22.shapes[5].has_text_frame:
        p2 = slide_22.shapes[5].text_frame.paragraphs[2]
        format_p(p2, "200/200 cặp ảnh kiểm định khớp hoàn toàn với Ground Truth (150/150 trên Held-out Test Set).", size_pt=10, color=COLOR_TEXT_MUTED)
    # Shape 7: Recall detail
    if len(slide_22.shapes) > 7 and slide_22.shapes[7].has_text_frame:
        p2 = slide_22.shapes[7].text_frame.paragraphs[2]
        format_p(p2, "100/100 cặp lỗi đều được phát hiện chính xác, FN = 0 (Không lọt bất kỳ lỗi nào).", size_pt=10, color=COLOR_TEXT_MUTED)
    # Shape 9: FPR detail
    if len(slide_22.shapes) > 9 and slide_22.shapes[9].has_text_frame:
        p2 = slide_22.shapes[9].text_frame.paragraphs[2]
        format_p(p2, "100/100 cặp ảnh bình thường đều báo PERFECT MATCH, FP = 0 (0% Báo động giả).", size_pt=10, color=COLOR_TEXT_MUTED)
    # Shape 11: F1-score detail
    if len(slide_22.shapes) > 11 and slide_22.shapes[11].has_text_frame:
        p2 = slide_22.shapes[11].text_frame.paragraphs[2]
        format_p(p2, "Đạt điểm F1 tuyệt đối trên cả Calibration Set (50 cặp) và Held-out Test Set (150 cặp).", size_pt=10, color=COLOR_TEXT_MUTED)
    # Shape 12: TN box
    if len(slide_22.shapes) > 12 and slide_22.shapes[12].has_text_frame:
        p0 = slide_22.shapes[12].text_frame.paragraphs[0]
        format_p(p0, "TN = 100\n(Đúng – No Defect)\n[Test Set: TN = 75]", size_pt=11, color=COLOR_PRIMARY, bold=True, align=PP_ALIGN.CENTER)
    # Shape 13: TP box
    if len(slide_22.shapes) > 13 and slide_22.shapes[13].has_text_frame:
        p0 = slide_22.shapes[13].text_frame.paragraphs[0]
        format_p(p0, "TP = 100\n(Đúng – Defect)\n[Test Set: TP = 75]", size_pt=11, color=COLOR_PRIMARY, bold=True, align=PP_ALIGN.CENTER)

    # =========================================================================
    # 7. Slide 27: 3.5. Ablation study
    # =========================================================================
    slide_27 = prs.slides[26]
    print("[*] Updating Slide 27: 3.5. Ablation study overview...")
    if len(slide_27.shapes) > 4 and slide_27.shapes[4].has_text_frame:
        tf = slide_27.shapes[4].text_frame
        if len(tf.paragraphs) >= 2:
            format_p(tf.paragraphs[0], "Tiến trình Tiến hóa Kỹ thuật Dẫn xuất từ Lỗi (Failure-Driven Engineering Evolution):",
                     size_pt=11, color=COLOR_PRIMARY, bold=True)
            format_p(tf.paragraphs[1], "• Chuỗi đối chứng 5 cấu hình trên 200 cặp ảnh (400 ảnh): [1. Raw Diff: Vỡ 45.61 BBoxes/lỗi, Recall 94%] ➔ [2. SSIM Only: Mù màu phẳng, Recall sụt giảm còn 86%] ➔ [3. Max Color Diff: Recall 99%, thiếu kênh cấu trúc] ➔ [4. SSIM + Color No Morph: Phân mảnh 8.39 BBoxes/lỗi] ➔ [5. Full Proposed Pipeline: Đạt 100% Recall, 0% FPR, BBox cô đọng 2.87 BBoxes/lỗi, Latency 171.6 ms].",
                     size_pt=9.5, color=COLOR_TEXT_DARK, bold=False)

    # =========================================================================
    # 8. Slide 28: 3.5. Ablation study – 5 cấu hình đối chứng
    # =========================================================================
    slide_28 = prs.slides[27]
    print("[*] Updating Slide 28: 3.5. Ablation study – 5 cấu hình...")
    # Title
    if len(slide_28.shapes) > 0 and slide_28.shapes[0].has_text_frame:
        format_p(slide_28.shapes[0].text_frame.paragraphs[0], "3.5. Ablation study – Đánh giá thực nghiệm các cấu hình",
                 size_pt=24, bold=True, color=COLOR_PRIMARY)
    # Box 1: Raw Diff
    if len(slide_28.shapes) > 4 and slide_28.shapes[4].has_text_frame:
        format_p(slide_28.shapes[4].text_frame.paragraphs[0], "CẤU HÌNH 1: RAW DIFF", size_pt=11, bold=True, color=COLOR_WHITE)
    if len(slide_28.shapes) > 5 and slide_28.shapes[5].has_text_frame:
        tf = slide_28.shapes[5].text_frame
        format_p(tf.paragraphs[0], "+ Đặc điểm: Trừ ảnh xám trực tiếp thô sơ giữa Baseline và Current", size_pt=10.5, color=COLOR_PRIMARY, bold=True)
        format_p(tf.paragraphs[1], "- Kết quả: Nhạy cảm vi sai sub-pixel viền card, vỡ vụn 45.61 BBoxes/lỗi, Recall 94.0%, FPR 1.0% (báo động giả)!", size_pt=10, color=COLOR_TEXT_MUTED, bold=False)

    # Box 2: SSIM Only
    if len(slide_28.shapes) > 7 and slide_28.shapes[7].has_text_frame:
        format_p(slide_28.shapes[7].text_frame.paragraphs[0], "CẤU HÌNH 2: SSIM ONLY", size_pt=11, bold=True, color=COLOR_WHITE)
    if len(slide_28.shapes) > 8 and slide_28.shapes[8].has_text_frame:
        tf = slide_28.shapes[8].text_frame
        format_p(tf.paragraphs[0], "+ Đặc điểm: Chỉ đo lường tương đồng cấu trúc SSIM kênh độ chói", size_pt=10.5, color=COLOR_PRIMARY, bold=True)
        format_p(tf.paragraphs[1], "- Kết quả: Bỏ sót lỗi đổi màu phẳng cùng Luminance (Vàng ➔ Đỏ ở S01), Recall sụt giảm nghiêm trọng còn 86.0%!", size_pt=10, color=COLOR_TEXT_MUTED, bold=False)

    # Box 3: Color Only & No Morph
    if len(slide_28.shapes) > 10 and slide_28.shapes[10].has_text_frame:
        format_p(slide_28.shapes[10].text_frame.paragraphs[0], "CẤU HÌNH 3 & 4: COLOR / NO MORPH", size_pt=10, bold=True, color=COLOR_WHITE)
    if len(slide_28.shapes) > 11 and slide_28.shapes[11].has_text_frame:
        tf = slide_28.shapes[11].text_frame
        format_p(tf.paragraphs[0], "+ Cấu hình 3: Max Color Diff bắt màu tốt (Recall 99.0%) nhưng thiếu thông tin cấu trúc.", size_pt=10.5, color=COLOR_PRIMARY, bold=True)
        format_p(tf.paragraphs[1], "- Cấu hình 4: SSIM + Color không có Morphology ΦK làm vỡ 8.39 BBoxes/lỗi (từng chữ cái rời rạc ở S04), tràn token LLM!", size_pt=10, color=COLOR_TEXT_MUTED, bold=False)

    # Box 4: Full Pipeline
    if len(slide_28.shapes) > 13 and slide_28.shapes[13].has_text_frame:
        format_p(slide_28.shapes[13].text_frame.paragraphs[0], "CẤU HÌNH 5: FULL PIPELINE", size_pt=11, bold=True, color=COLOR_WHITE)
    if len(slide_28.shapes) > 14 and slide_28.shapes[14].has_text_frame:
        tf = slide_28.shapes[14].text_frame
        format_p(tf.paragraphs[0], "+ Full Proposed: Lanczos-4 + Dual Metric (SSIM & Max Color) + Morphology ΦK + Suzuki-Abe", size_pt=10.5, color=COLOR_PRIMARY, bold=True)
        format_p(tf.paragraphs[1], "- ĐÍCH ĐẾN TỐI ƯU TRÊN 200 CẶP: Đạt 100% Recall, 0% FPR, cô đọng 2.87 BBoxes/lỗi, độ trễ 171.6 ms trên CPU!", size_pt=10, color=COLOR_TEXT_MUTED, bold=False)

    # =========================================================================
    # 9. INSERT NEW SLIDE: 3.6. Thực nghiệm Đối chứng Tác động đến Agentic AI
    # =========================================================================
    print("[*] Creating Slide 29: 3.6. Thực nghiệm Đối chứng Tác động đến Agentic AI...")
    layout_blank = prs.slide_layouts[6] # Blank slide
    slide_agent = prs.slides.add_slide(layout_blank)

    # Title shape
    title_box = slide_agent.shapes.add_textbox(Inches(0.63), Inches(0.18), Inches(8.68), Inches(0.65))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_t = tf_title.paragraphs[0]
    format_p(p_t, "3.6. Thực nghiệm Đối chứng Tác động đến Agentic AI", font_name="Segoe UI", size_pt=22, bold=True, color=COLOR_PRIMARY)

    # Footer note
    footer_box = slide_agent.shapes.add_textbox(Inches(0.63), Inches(5.31), Inches(3.54), Inches(0.22))
    p_f = footer_box.text_frame.paragraphs[0]
    format_p(p_f, "Trường Đại học Công nghệ Thông tin, ĐHQG-HCM", font_name="Segoe UI", size_pt=8, color=COLOR_TEXT_MUTED)

    # Subtitle / Context card banner
    top_banner = slide_agent.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.63), Inches(0.85), Inches(8.74), Inches(0.48))
    top_banner.fill.solid()
    top_banner.fill.fore_color.rgb = COLOR_CARD_BG
    top_banner.line.color.rgb = COLOR_CARD_BORDER
    top_banner.line.width = Pt(1)
    tf_tb = top_banner.text_frame
    tf_tb.word_wrap = True
    p_tb = tf_tb.paragraphs[0]
    format_p(p_tb, "KHẢO SÁT ĐỊNH LƯỢNG HIỆU NĂNG AGENTIC AI (CLAUDE 3.5 SONNET / GEMINI 1.5 PRO) TRƯỚC VS SAU KHI CÓ MODULE",
             size_pt=10, bold=True, color=COLOR_PRIMARY, align=PP_ALIGN.CENTER)

    # Comparison Table
    table_shape = slide_agent.shapes.add_table(rows=7, cols=4, left=Inches(0.63), top=Inches(1.42), width=Inches(8.74), height=Inches(2.68))
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(2.74)
    table.columns[1].width = Inches(1.85)
    table.columns[2].width = Inches(2.15)
    table.columns[3].width = Inches(2.00)

    # Table Data
    table_data = [
        ("Tiêu chí Đánh giá (Metrics)", "Baseline Agent (Không Module)", "Proposed Agent (Có Module Grounding)", "Cải thiện Vượt bậc"),
        ("Tỷ lệ Định vị Lỗi (Localization)", "28.3%", "98.3%", "+70.0% (Định vị chuẩn xác)"),
        ("Tỷ lệ Tự sửa Thành công (Fix Rate)", "31.7%", "93.3%", "+61.6% (Sửa đúng CSS/DOM)"),
        ("Lượng Token Tiêu thụ / Ticket", "16,067 tokens", "1,338 tokens", "Giảm 90.1% context"),
        ("Thời gian Phản hồi (Avg Latency)", "47.8 giây", "7.9 giây", "Nhanh hơn 6.05 lần"),
        ("Chi phí Vận hành API / Fix", "$0.0605", "$0.0059", "Tiết kiệm 90.2% chi phí"),
        ("Độ Tương đồng Sau Sửa (Post SSIM)", "0.764", "0.998", "+0.234 (Khôi phục hoàn hảo)")
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = ""
            p = cell.text_frame.paragraphs[0]
            if r_idx == 0:
                # Header row
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_PRIMARY
                format_p(p, val, size_pt=10, bold=True, color=COLOR_WHITE, align=PP_ALIGN.CENTER)
            else:
                # Data rows
                cell.fill.solid()
                if r_idx % 2 == 1:
                    cell.fill.fore_color.rgb = COLOR_WHITE
                else:
                    cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
                
                align = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
                bold = True if c_idx in [0, 2, 3] else False
                color = COLOR_PRIMARY if c_idx == 2 else (RGBColor(5, 150, 105) if c_idx == 3 else COLOR_TEXT_DARK)
                format_p(p, val, size_pt=9.5, bold=bold, color=color, align=align)

    # Bottom Highlight Card
    bottom_card = slide_agent.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.63), Inches(4.20), Inches(8.74), Inches(0.95))
    bottom_card.fill.solid()
    bottom_card.fill.fore_color.rgb = COLOR_CARD_BG
    bottom_card.line.color.rgb = COLOR_SECONDARY
    bottom_card.line.width = Pt(1)
    tf_bc = bottom_card.text_frame
    tf_bc.word_wrap = True
    p_bc0 = tf_bc.paragraphs[0]
    format_p(p_bc0, "💡 ĐỘT PHÁ CỐT LÕI VÀ Ý NGHĨA THỰC TIỄN:", size_pt=10, bold=True, color=COLOR_PRIMARY)
    p_bc1 = tf_bc.add_paragraph()
    format_p(p_bc1, "• Module giải quyết triệt để 'sửa code mù' (blind coding) và ảo giác selector (selector hallucination) của LLM Agent.", size_pt=9.5, bold=False, color=COLOR_TEXT_DARK)
    p_bc2 = tf_bc.add_paragraph()
    format_p(p_bc2, "• Tọa độ Bounding Box và localized DOM snippet giúp Agent tự sửa CSS chuẩn xác ngay lần đầu, tạo vòng lặp tự chữa lành (Self-healing Loop) khép kín.", size_pt=9.5, bold=False, color=COLOR_TEXT_DARK)

    # Reorder new slide to index 28 (Slide 29)
    slide_id_list = prs.slides._sldIdLst
    elem = slide_id_list[-1]
    slide_id_list.insert(28, elem)
    print(f"[*] Inserted Slide 29 successfully. Total slides now: {len(prs.slides)}")

    # =========================================================================
    # 10. Slide 30 (previously 29): 4. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
    # =========================================================================
    slide_30 = prs.slides[29]
    print("[*] Updating Slide 30: Agenda Chương 4...")
    if len(slide_30.shapes) > 3 and slide_30.shapes[3].has_text_frame:
        tf = slide_30.shapes[3].text_frame
        p_c4 = [
            "Kết luận và kết quả thu được",
            "Hạn chế và hướng phát triển",
            "Demo Dashboard (Streamlit 4 Tabs)"
        ]
        while len(tf.paragraphs) < len(p_c4):
            tf.add_paragraph()
        for idx, item in enumerate(p_c4):
            format_p(tf.paragraphs[idx], item, font_name="Segoe UI", size_pt=18, bold=False, color=COLOR_TEXT_DARK)

    # =========================================================================
    # 11. Slide 31 (previously 30): 4.1. Kết luận và kết quả thu được
    # =========================================================================
    slide_31 = prs.slides[30]
    print("[*] Updating Slide 31: 4.1. Kết luận và kết quả thu được...")
    # Result 1: Latency
    if len(slide_31.shapes) > 6 and slide_31.shapes[6].has_text_frame:
        tf = slide_31.shapes[6].text_frame
        if len(tf.paragraphs) >= 2:
            format_p(tf.paragraphs[0], "• Hiện thực hóa thành công Engine kiểm định thị giác tự động kết hợp Lanczos-4, SSIM, Max Color Diff và Morphology.", size_pt=10, color=COLOR_TEXT_DARK)
            format_p(tf.paragraphs[1], "• Vận hành độc lập trên CPU với tốc độ 171.6 ms, không phụ thuộc GPU hay API đám mây.", size_pt=10, color=COLOR_TEXT_MUTED, bold=True)
    # Result 2: Dataset 200 pairs
    if len(slide_31.shapes) > 10 and slide_31.shapes[10].has_text_frame:
        tf = slide_31.shapes[10].text_frame
        if len(tf.paragraphs) >= 2:
            format_p(tf.paragraphs[0], "• Đạt Accuracy 100.0%, Recall 100.0%, Precision 100.0% và FPR 0.0% trên toàn bộ 200 cặp ảnh benchmark (150 cặp Held-out Test Set).", size_pt=10, color=COLOR_TEXT_DARK)
            format_p(tf.paragraphs[1], "• Bộ dữ liệu 200 cặp (400 ảnh) tiêm lỗi tự động qua Playwright trên 6 nhóm đột biến phổ biến.", size_pt=10, color=COLOR_TEXT_MUTED, bold=True)
    # Contribution 1: Bbox compression
    if len(slide_31.shapes) > 14 and slide_31.shapes[14].has_text_frame:
        tf = slide_31.shapes[14].text_frame
        if len(tf.paragraphs) >= 2:
            format_p(tf.paragraphs[0], "• Loại bỏ triệt để nhiễu Anti-aliasing bằng phân ngưỡng động kép kết hợp làm mịn font.", size_pt=10, color=COLOR_TEXT_DARK)
            format_p(tf.paragraphs[1], "• Triệt tiêu bùng nổ Bounding Box (từ 45.61 → 2.87 bbox/lỗi), bảo vệ an toàn Context Window của LLM.", size_pt=10, color=COLOR_PRIMARY, bold=True)
    # Contribution 2: Agent bridge
    if len(slide_31.shapes) > 18 and slide_31.shapes[18].has_text_frame:
        tf = slide_31.shapes[18].text_frame
        if len(tf.paragraphs) >= 2:
            format_p(tf.paragraphs[0], "• Tự động xuất chuỗi JSON tọa độ chuẩn hóa và Prompt định hướng không gian (Spatial Grounding).", size_pt=10, color=COLOR_TEXT_DARK)
            format_p(tf.paragraphs[1], "• Nâng tỷ lệ tự sửa lỗi của Agent từ 31.7% lên 93.3%, tiết kiệm 90.1% token và giảm 6.05 lần độ trễ.", size_pt=10, color=COLOR_PRIMARY, bold=True)

    # =========================================================================
    # 12. Slide 32 (previously 31): 4.2. Hạn chế và hướng phát triển
    # =========================================================================
    slide_32 = prs.slides[31]
    print("[*] Updating Slide 32: 4.2. Hạn chế và hướng phát triển...")
    if len(slide_32.shapes) > 0 and slide_32.shapes[0].has_text_frame:
        format_p(slide_32.shapes[0].text_frame.paragraphs[0], "4.2. Hạn chế và hướng phát triển", font_name="Segoe UI", size_pt=24, bold=True, color=COLOR_PRIMARY)

    # =========================================================================
    # 13. Slide 33 (previously 32): 4.3. Demo Dashboard
    # =========================================================================
    slide_33 = prs.slides[32]
    print("[*] Updating Slide 33: 4.3. Demo Dashboard...")
    if len(slide_33.shapes) > 0 and slide_33.shapes[0].has_text_frame:
        format_p(slide_33.shapes[0].text_frame.paragraphs[0], "4.3. Demo Dashboard (Streamlit 4 Tabs)", font_name="Segoe UI", size_pt=24, bold=True, color=COLOR_PRIMARY)

    # Add 4 interactive cards on Slide 33 (similar to Slide 30 2x2 grid)
    # Card 1 (Top Left): Tab 1
    c1 = slide_33.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.63), Inches(1.10), Inches(4.25), Inches(1.95))
    c1.fill.solid()
    c1.fill.fore_color.rgb = COLOR_CARD_BG
    c1.line.color.rgb = COLOR_SECONDARY
    c1.line.width = Pt(1.5)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    format_p(tf1.paragraphs[0], "🎯 TAB 1: DATASET BENCHMARK EXPLORER", size_pt=11, bold=True, color=COLOR_PRIMARY)
    p1_1 = tf1.add_paragraph()
    format_p(p1_1, "• Duyệt qua toàn bộ 200 cặp ảnh (100 Không lỗi / 100 Có lỗi), lọc 6 nhóm đột biến giao diện.", size_pt=9.5, color=COLOR_TEXT_DARK)
    p1_2 = tf1.add_paragraph()
    format_p(p1_2, "• Hiển thị nhãn Calibration Set (mẫu 01-25) & Held-out Test Set (mẫu 26-100).", size_pt=9.5, color=COLOR_TEXT_MUTED)
    p1_3 = tf1.add_paragraph()
    format_p(p1_3, "• Trực quan hóa song song Baseline, Current, Heatmap sai lệch, BBox và Generated Agent Prompt.", size_pt=9.5, color=COLOR_TEXT_DARK)

    # Card 2 (Top Right): Tab 2
    c2 = slide_33.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.12), Inches(1.10), Inches(4.25), Inches(1.95))
    c2.fill.solid()
    c2.fill.fore_color.rgb = COLOR_CARD_BG
    c2.line.color.rgb = COLOR_SECONDARY
    c2.line.width = Pt(1.5)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    format_p(tf2.paragraphs[0], "📤 TAB 2: CUSTOM IMAGE INSPECTION", size_pt=11, bold=True, color=COLOR_PRIMARY)
    p2_1 = tf2.add_paragraph()
    format_p(p2_1, "• Cho phép tải lên 2 ảnh tùy ý từ máy tính để kiểm tra sai khác trực tiếp theo thời gian thực.", size_pt=9.5, color=COLOR_TEXT_DARK)
    p2_2 = tf2.add_paragraph()
    format_p(p2_2, "• Tự động kích hoạt toàn bộ pipeline: Tiền xử lý, Dual Comparator, Morphology ΦK và Suzuki-Abe.", size_pt=9.5, color=COLOR_TEXT_MUTED)
    p2_3 = tf2.add_paragraph()
    format_p(p2_3, "• Xuất tức thì hình ảnh khoanh vùng đỏ và bảng tọa độ Bounding Box, SSIM score, severity level.", size_pt=9.5, color=COLOR_TEXT_DARK)

    # Card 3 (Bottom Left): Tab 3
    c3 = slide_33.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.63), Inches(3.20), Inches(4.25), Inches(1.95))
    c3.fill.solid()
    c3.fill.fore_color.rgb = COLOR_CARD_BG
    c3.line.color.rgb = COLOR_SECONDARY
    c3.line.width = Pt(1.5)
    tf3 = c3.text_frame
    tf3.word_wrap = True
    format_p(tf3.paragraphs[0], "📈 TAB 3: FULL BENCHMARK & METRICS", size_pt=11, bold=True, color=COLOR_PRIMARY)
    p3_1 = tf3.add_paragraph()
    format_p(p3_1, "• Cung cấp 3 tùy chọn đánh giá: Held-out Test Set (150 cặp), Toàn bộ Dataset (200 cặp), Calibration (50 cặp).", size_pt=9.5, color=COLOR_TEXT_DARK)
    p3_2 = tf3.add_paragraph()
    format_p(p3_2, "• Nút 'Khởi chạy Benchmark' tính toán thời gian thực với thanh tiến trình trực quan.", size_pt=9.5, color=COLOR_TEXT_MUTED)
    p3_3 = tf3.add_paragraph()
    format_p(p3_3, "• Xuất Ma trận nhầm lẫn (Confusion Matrix), Accuracy, Precision, Recall, F1-Score, FPR và số BBox.", size_pt=9.5, color=COLOR_TEXT_DARK)

    # Card 4 (Bottom Right): Tab 4
    c4 = slide_33.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.12), Inches(3.20), Inches(4.25), Inches(1.95))
    c4.fill.solid()
    c4.fill.fore_color.rgb = COLOR_CARD_BG
    c4.line.color.rgb = COLOR_SECONDARY
    c4.line.width = Pt(1.5)
    tf4 = c4.text_frame
    tf4.word_wrap = True
    format_p(tf4.paragraphs[0], "🤖 TAB 4: AGENTIC AI BENCHMARK", size_pt=11, bold=True, color=COLOR_PRIMARY)
    p4_1 = tf4.add_paragraph()
    format_p(p4_1, "• Trực quan hóa số liệu so sánh định lượng hiệu năng Agent Trước vs Sau khi nhận dữ liệu từ module.", size_pt=9.5, color=COLOR_TEXT_DARK)
    p4_2 = tf4.add_paragraph()
    format_p(p4_2, "• Nổi bật các bước nhảy vọt: Định vị lỗi 28.3% → 98.3%, Tự sửa thành công 31.7% → 93.3%.", size_pt=9.5, color=COLOR_TEXT_MUTED)
    p4_3 = tf4.add_paragraph()
    format_p(p4_3, "• Tiết kiệm 90.1% token ngữ cảnh (16,067 → 1,338 tokens) và giảm 6.05 lần thời gian phản hồi.", size_pt=9.5, color=COLOR_PRIMARY, bold=True)

    # Save presentation
    prs.save("ChuyenDeTotNghiep.pptx")
    print(f"[+] Successfully saved updated presentation to {pptx_path} with {len(prs.slides)} slides!")

if __name__ == "__main__":
    update_presentation()
