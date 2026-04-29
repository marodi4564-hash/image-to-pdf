import streamlit as st
from PIL import Image
import io

st.title("Image to PDF Converter (400-500KB)")

uploaded_file = st.file_uploader("Apni Photo Upload Karein", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    # Binary search for quality
    low = 1
    high = 100
    best_pdf = None
    
    with st.spinner('Convert ho raha hai...'):
        while low <= high:
            mid = (low + high) // 2
            pdf_bytes = io.BytesIO()
            img.save(pdf_bytes, "PDF", quality=mid)
            size_kb = pdf_bytes.tell() / 1024
            
            if 400 <= size_kb <= 500:
                best_pdf = pdf_bytes.getvalue()
                break
            elif size_kb < 400:
                low = mid + 1
            else:
                high = mid - 1
                best_pdf = pdf_bytes.getvalue()
        
    if best_pdf:
        st.success(f"PDF tayyar hai!")
        st.download_button("Download PDF", best_pdf, "document.pdf", "application/pdf")
    else:
        st.error("Photo ka size adjust nahi ho pa raha. Dusri photo try karein.")
