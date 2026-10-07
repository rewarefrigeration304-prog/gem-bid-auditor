import streamlit as st
from google import genai
from google.genai import types

# Page setup
st.set_page_config(page_title="GeM Bid Verifier", page_icon="📄", layout="centered")

st.title("📄 GeM Bid Document Auditor")
st.write("Apni GeM Bid PDF upload karein aur required documents ki audit report paayein.")

# Secrets se Gemini API key uthayega
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# Client ki Master Profile
CLIENT_PROFILE = """
Business Type: Proprietary / Private Limited
GST: Available & Active
MSME (Udyam): Available (Micro/Small Enterprise)
PAN: Available
Past 3 Years CA Certified Average Turnover: Rs 30 Lakhs
Past Experience: 2 years experience in similar government supplies
General Undertakings: Available (Non-blacklisting, Local Content declaration ready on stamp paper)
"""

uploaded_file = st.file_uploader("Upload GeM Bid PDF", type=["pdf"])

if uploaded_file is not None:
    if st.button("Audit Bid Requirements", type="primary"):
        with st.spinner("Bid document ko scan kiya ja raha hai..."):
            try:
                pdf_bytes = uploaded_file.read()
                
                system_prompt = f"""
                Tum ek expert GeM (Government e-Marketplace) Bid Auditor ho.
                Di gayi Bid PDF ko dhyan se padho aur buyer ki Eligibility, Technical Specifications, aur Buyer Added Bid Specific ATC ko scan karo.
                
                Client ki Master Profile yeh hai:
                {CLIENT_PROFILE}
                
                Mujhe structured audit report do:
                1. **Bid Summary:** Bid No, Department, Item Name, Quantity, EMD amount aur kya MSME exemption applicable hai.
                2. **Available Documents (Match):** Jo client ke paas pehle se hain aur bid criteria ko meet kar rahe hain.
                3. **Required / To Arrange (Missing):** Wo specific certificates, lab test reports, OEM authorizations, ya stamp paper undertakings jo banwane padenge.
                4. **Critical Flags / Risks:** Kya koi aisi condition hai jo client meet nahi kar sakta (Turnover, Experience, etc.)?
                """

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        types.Part.from_bytes(
                            data=pdf_bytes,
                            mime_type='application/pdf',
                        ),
                        system_prompt
                    ]
                )

                st.success("Audit Complete!")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error: {e}")
