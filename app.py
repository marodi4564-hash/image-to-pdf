import streamlit as st
from PIL import Image
import io
import os

st.set_page_config(page_title="PDF Converter", page_icon="📄")

st.title("Image to PDF Converter (400KB-500KB)")
st.write("Apni photo upload karein, yeh automatic 400KB-500KB ke beech PDF bana dega.")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    # Binary search for quality to hit target size (400KB - 500KB)
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
        
        # Dynamic Filename Logic
        original_name = uploaded_file.name
        output_filename = os.path.splitext(original_name)[0] + ".pdf"
        
        st.download_button(
            label="Download PDF",
            data=best_pdf,
            file_name=output_filename,
            mime="application/pdf"
        )
    else:
        st.error("Photo ka size adjust nahi ho pa raha. Dusri photo try karein.")

