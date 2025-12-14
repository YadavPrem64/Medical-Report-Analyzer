"""
Medical Report Analyzer - Streamlit Web Application
Main application file
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.preprocessing.pdf_extractor import PDFExtractor
import tempfile
import os

# Page Configuration
st.set_page_config(
    page_title="Medical Report Analyzer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    . sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
    }
    . info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border-left:  5px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🏥 Medical Report Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("##### AI-Powered Medical Report Analysis with Explainable Insights")
    
    # Sidebar
    with st.sidebar:
        st. image("https://img.icons8.com/fluency/96/000000/medical-heart.png", width=100)
        st.title("Navigation")
        
        page = st.radio(
            "Go to",
            ["📤 Upload Report", "ℹ️ About", "📊 Demo"]
        )
        
        st.markdown("---")
        st.markdown("### 🎓 Final Year Project")
        st.markdown("**Developer:** Prem Yadav")
        st.markdown("**Year:** 2025")
        st.markdown("**Tech:** Python, NLP, Deep Learning")
    
    # Main Content
    if page == "📤 Upload Report":
        upload_page()
    elif page == "ℹ️ About":
        about_page()
    else:
        demo_page()


def upload_page():
    """Upload and analyze medical reports"""
    
    st.markdown('<h2 class="sub-header">Upload Your Medical Report</h2>', unsafe_allow_html=True)
    
    col1, col2 = st. columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a medical report (PDF or Image)",
            type=['pdf', 'jpg', 'jpeg', 'png'],
            help="Upload your medical report in PDF or image format"
        )
    
    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("**Supported Formats:**")
        st.markdown("- PDF documents")
        st.markdown("- JPG/JPEG images")
        st.markdown("- PNG images")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # Display file info
        st.success(f"✅ File uploaded:  {uploaded_file.name}")
        
        file_details = {
            "Filename": uploaded_file.name,
            "File Size": f"{uploaded_file.size / 1024:.2f} KB",
            "File Type":  uploaded_file.type
        }
        
        with st.expander("📄 File Details"):
            for key, value in file_details. items():
                st.write(f"**{key}:** {value}")
        
        # Process button
        if st.button("🔍 Analyze Report", type="primary"):
            with st.spinner("Processing your report..."):
                
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                try:
                    # Extract text based on file type
                    if uploaded_file.type == "application/pdf":
                        extractor = PDFExtractor()
                        result = extractor.extract_with_metadata(tmp_path)
                        
                        if result: 
                            st.markdown("---")
                            st.markdown('<h3 class="sub-header">📊 Extraction Results</h3>', unsafe_allow_html=True)
                            
                            # Display metrics
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st. metric("Pages", result['num_pages'])
                            with col2:
                                st.metric("Words", result['word_count'])
                            with col3:
                                st.metric("Characters", result['char_count'])
                            with col4:
                                st.metric("Status", "✅ Success")
                            
                            # Display extracted text
                            st. markdown("---")
                            st.markdown("### 📝 Extracted Text")
                            st.text_area(
                                "Full Text",
                                result['text'],
                                height=300,
                                help="Complete extracted text from the report"
                            )
                            
                            # Download option
                            st.download_button(
                                label="⬇️ Download Extracted Text",
                                data=result['text'],
                                file_name=f"{Path(uploaded_file.name).stem}_extracted. txt",
                                mime="text/plain"
                            )
                            
                            # Next steps
                            st.markdown("---")
                            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                            st.markdown("### 🚧 Coming Soon:")
                            st.markdown("- 🧠 Entity Extraction (Patient details, test names, values)")
                            st.markdown("- ⚠️ Anomaly Detection (Abnormal values highlighting)")
                            st.markdown("- 💡 Explainable AI (Why values were flagged)")
                            st.markdown("- 📈 Trend Analysis (Compare with previous reports)")
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.error("❌ Failed to extract text from PDF")
                    
                    else:
                        st.info("🔄 Image OCR processing coming soon!")
                        st.markdown("Currently only PDF processing is implemented.")
                
                finally:
                    # Clean up temp file
                    os.unlink(tmp_path)


def about_page():
    """About page with project information"""
    
    st. markdown('<h2 class="sub-header">About This Project</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Project Overview
    
    The **Medical Report Analyzer** is an AI-powered application that helps patients and healthcare 
    professionals quickly understand medical reports through automated analysis and explainable insights.
    
    ### ✨ Key Features
    
    - **📄 Multi-Format Support**:  Process PDF and image medical reports
    - **🔍 Smart Extraction**: Advanced OCR and text extraction
    - **🧠 NLP Analysis**: Extract medical entities using BioBERT
    - **⚠️ Anomaly Detection**:  Automatically identify abnormal values
    - **💡 Explainable AI**:  Understand why values were flagged using SHAP
    - **📊 Visualization**: Clear charts and trend analysis
    - **🔒 Secure**:  Privacy-focused design
    
    ### 🛠️ Technology Stack
    
    - **Language**:  Python 3.8+
    - **Deep Learning**: PyTorch, Transformers (BioBERT)
    - **NLP**: SpaCy, Hugging Face
    - **OCR**: EasyOCR, Tesseract
    - **Web**:  Streamlit
    - **XAI**: SHAP, LIME
    
    ### 👨‍💻 Developer
    
    **Name:** Prem Yadav  
    **GitHub:** [@YadavPrem64](https://github.com/YadavPrem64)  
    **Project Type:** Final Year Project  
    **Year:** 2025
    
    ### 📚 References
    
    - BioBERT: Pre-trained biomedical language model
    - MIMIC-III: Medical Information Mart for Intensive Care
    - SHAP: SHapley Additive exPlanations
    
    ### 📧 Contact
    
    For questions or feedback, please open an issue on GitHub. 
    """)


def demo_page():
    """Demo page with sample analysis"""
    
    st.markdown('<h2 class="sub-header">📊 Demo Analysis</h2>', unsafe_allow_html=True)
    
    st.info("This page will show a demo analysis of a sample medical report once the full pipeline is ready!")
    
    # Sample visualization
    st.markdown("### Sample Blood Test Results")
    
    import pandas as pd
    import plotly.graph_objects as go
    
    # Sample data
    data = {
        'Test Name': ['Hemoglobin', 'WBC', 'RBC', 'Platelets', 'Glucose'],
        'Your Value': [14.5, 7.2, 4.8, 250, 95],
        'Normal Min': [13.5, 4.5, 4.5, 150, 70],
        'Normal Max': [17.5, 11.0, 5.9, 400, 100],
        'Unit': ['g/dL', '10^3/μL', '10^6/μL', '10^3/μL', 'mg/dL']
    }
    
    df = pd.DataFrame(data)
    
    # Create visualization
    fig = go.Figure()
    
    for idx, row in df.iterrows():
        color = 'green' if row['Normal Min'] <= row['Your Value'] <= row['Normal Max'] else 'red'
        
        fig.add_trace(go.Bar(
            name=row['Test Name'],
            x=[row['Test Name']],
            y=[row['Your Value']],
            marker_color=color,
            text=f"{row['Your Value']} {row['Unit']}",
            textposition='outside'
        ))
    
    fig.update_layout(
        title="Sample Blood Test Analysis",
        xaxis_title="Test Name",
        yaxis_title="Value",
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display table
    st.markdown("### Detailed Results")
    st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    main()