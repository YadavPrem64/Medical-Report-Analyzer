"""
Generate a sample medical report PDF for testing
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_sample_report(filename="sample_medical_report.pdf"):
    """Generate a realistic sample blood test report"""
    
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 1*inch, "CITY GENERAL HOSPITAL")
    
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, height - 1.3*inch, "123 Medical Street, City, State 12345")
    c.drawString(1*inch, height - 1.5*inch, "Phone: (555) 123-4567")
    
    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 2*inch, "LABORATORY REPORT")
    
    # Patient Info
    c.setFont("Helvetica", 10)
    y = height - 2.5*inch
    c.drawString(1*inch, y, "Patient Name: John Doe")
    c.drawString(4.5*inch, y, "Age: 45 Years")
    
    y -= 0.25*inch
    c.drawString(1*inch, y, "Patient ID: PAT123456")
    c.drawString(4.5*inch, y, "Gender: Male")
    
    y -= 0.25*inch
    c.drawString(1*inch, y, "Date of Collection: 2025-12-10")
    c.drawString(4.5*inch, y, "Report Date: 2025-12-14")
    
    # Test Results Table
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y, "COMPLETE BLOOD COUNT (CBC)")
    
    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1*inch, y, "Test Name")
    c.drawString(3*inch, y, "Result")
    c.drawString(4*inch, y, "Normal Range")
    c.drawString(5.5*inch, y, "Unit")
    
    c.setFont("Helvetica", 9)
    
    # Test data
    tests = [
        ("Hemoglobin", "14.5", "13.5-17.5", "g/dL"),
        ("RBC Count", "4.8", "4.5-5.9", "10^6/microL"),
        ("WBC Count", "7.2", "4.5-11.0", "10^3/microL"),
        ("Platelets", "250", "150-400", "10^3/microL"),
        ("Hematocrit", "42", "38-50", "%"),
        ("MCV", "88", "80-100", "fL"),
        ("MCH", "30", "27-33", "pg"),
        ("MCHC", "34", "32-36", "g/dL"),
    ]
    
    y -= 0.05*inch
    c.line(1*inch, y, 7*inch, y)
    y -= 0.2*inch
    
    for test in tests:
        c.drawString(1*inch, y, test[0])
        c.drawString(3*inch, y, test[1])
        c.drawString(4*inch, y, test[2])
        c.drawString(5.5*inch, y, test[3])
        y -= 0.2*inch
    
    # Biochemistry
    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y, "BIOCHEMISTRY")
    
    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1*inch, y, "Test Name")
    c.drawString(3*inch, y, "Result")
    c.drawString(4*inch, y, "Normal Range")
    c.drawString(5.5*inch, y, "Unit")
    
    c.setFont("Helvetica", 9)
    
    bio_tests = [
        ("Glucose (Fasting)", "95", "70-100", "mg/dL"),
        ("Cholesterol Total", "180", "< 200", "mg/dL"),
        ("HDL Cholesterol", "55", "> 40", "mg/dL"),
        ("LDL Cholesterol", "110", "< 100", "mg/dL"),
        ("Triglycerides", "140", "< 150", "mg/dL"),
        ("Creatinine", "1.0", "0.7-1.3", "mg/dL"),
    ]
    
    y -= 0.05*inch
    c.line(1*inch, y, 7*inch, y)
    y -= 0.2*inch
    
    for test in bio_tests:
        c.drawString(1*inch, y, test[0])
        c.drawString(3*inch, y, test[1])
        c.drawString(4*inch, y, test[2])
        c.drawString(5.5*inch, y, test[3])
        y -= 0.2*inch
    
    # Footer
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "Remarks:")
    c.setFont("Helvetica", 9)
    y -= 0.2*inch
    c.drawString(1*inch, y, "All parameters are within normal limits.")
    
    y -= 0.5*inch
    c.setFont("Helvetica", 8)
    c.drawString(1*inch, y, "Verified by: Dr. Jane Smith, MD")
    c.drawString(5*inch, y, "Signature: __________")
    
    c.save()
    print(f"✅ Sample report generated: {filename}")

if __name__ == "__main__":
    generate_sample_report()
