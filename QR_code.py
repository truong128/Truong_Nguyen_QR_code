import qrcode
from PIL import Image
import streamlit as st


st.title("Truong Nguyen QR Code Generator")

st.subheader("Choose how to generate your QR Code:")
content_input = st.text_input("1. Enter/Type/Copy any content to create YOUR QR code:")
uploaded_file = st.file_uploader("2. Or upload a file to generate a QR code:")


max_length = 10000000000000000000

def get_file_content(file):
    """Read file content with encoding handling."""
    try:
        return file.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        st.warning("Failed to decode with UTF-8. Trying ISO-8859-1...")
        try:
            return file.getvalue().decode("ISO-8859-1")
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return None

def is_valid_qr_data(data):
    """Check if the data is suitable for QR code generation."""
    return len(data) <= max_length

if st.button("Generate QR Code"):
    if content_input:
        qr_data = content_input
    elif uploaded_file:
        qr_data = get_file_content(uploaded_file)
        if qr_data is None:
            st.stop()
    else:
        st.warning("Please provide text or upload a file.")
        st.stop()

    if not is_valid_qr_data(qr_data):
        st.warning(f"The content exceeds the maximum allowed length for a QR code (currently set to {max_length} characters).")
    else:
        try:
            
            QR = qrcode.QRCode(version=None, box_size=10, border=4)
            QR.add_data(qr_data)
            QR.make(fit=True)

            
            img = QR.make_image(fill_color="black", back_color="cyan")
            img.save("QR_code.png")

            
            st.image("QR_code.png", caption="Your QR Code", use_column_width=True)
        except Exception as e:
            st.error(f"Failed to generate QR Code: {e}")
