import fitz  # PyMuPDF

doc = fitz.open("NA_Basic_Text_6th.pdf")

word_to_find = "god"
occurrence_target = 92
occurrence_count = 0

for page_num in range(len(doc)):
    text = doc[page_num].get_text()
    words = text.lower().split()
    
    for word in words:
        if word == word_to_find:
            occurrence_count += 1
            if occurrence_count == occurrence_target:
                print(f"The {occurrence_target}th occurrence of 'God' is on PDF page {page_num + 1}.")
                break  # Stop checking this page once we’ve found it
    if occurrence_count == occurrence_target:
        break



