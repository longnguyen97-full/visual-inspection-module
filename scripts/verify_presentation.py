import sys
sys.stdout.reconfigure(encoding='utf-8')

from pptx import Presentation

prs = Presentation("ChuyenDeTotNghiep.pptx")
print(f"Total slides in updated presentation: {len(prs.slides)}")

check_slides = [9, 17, 19, 20, 21, 22, 27, 28, 29, 30, 31, 32, 33]

for sn in check_slides:
    slide = prs.slides[sn - 1]
    title = ""
    for s in slide.shapes:
        if s.has_text_frame and s.text_frame.text:
            first_line = s.text_frame.text.split("\n")[0].strip()
            if first_line and not "Trường Đại học" in first_line:
                title = first_line
                break
    print(f"\n==================== SLIDE {sn}: {title} ====================")
    for idx, shape in enumerate(slide.shapes):
        if shape.has_text_frame:
            txt = shape.text_frame.text.strip()
            if txt:
                print(f"  Shape {idx} [{shape.name}]:")
                for p_idx, p in enumerate(shape.text_frame.paragraphs):
                    p_txt = p.text.strip()
                    if p_txt:
                        print(f"    P{p_idx}: {p_txt}")
        elif shape.has_table:
            print(f"  Shape {idx} [TABLE {shape.name}]: {len(shape.table.rows)} rows x {len(shape.table.columns)} cols")
            for r_idx, row in enumerate(shape.table.rows):
                row_txt = [c.text.strip().replace('\n', ' ') for c in row.cells]
                print(f"    R{r_idx}: {' | '.join(row_txt)}")
