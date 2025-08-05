import fitz  # PyMuPDF

input_path = 'na_step_guide.pdf'
output_path = 'cleaned_na_step_guide.pdf'

doc = fitz.open(input_path)

for page in doc:
    # ---- Remove all hyperlinks ----
    for link in page.get_links():
        page.delete_link(link)

    # ---- Smaller white box to hide footer ----
    rect = page.rect
    footer_height = 25  # Try 25 instead of 50
    white_box = fitz.Rect(rect.x0, rect.y1 - footer_height, rect.x1, rect.y1)
    page.draw_rect(white_box, color=(1, 1, 1), fill=(1, 1, 1))

doc.save(output_path)
doc.close()

print(f"Cleaned PDF saved as: {output_path}")

