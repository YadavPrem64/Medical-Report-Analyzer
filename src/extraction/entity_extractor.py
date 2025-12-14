"""
Medical Entity Extraction Module
Extracts patient information, test names, values, and ranges from medical reports
"""

import re
import logging
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalEntityExtractor:
    """Extract medical entities from report text"""
    
    def __init__(self):
        self.test_patterns = {
            'hemoglobin': r'hemoglobin|hb|hgb',
            'rbc': r'rbc\s+count|red\s+blood\s+cell',
            'wbc': r'wbc\s+count|white\s+blood\s+cell',
            'platelets': r'platelet',
            'glucose': r'glucose|blood\s+sugar',
            'cholesterol': r'cholesterol',
            'hdl': r'hdl',
            'ldl': r'ldl',
            'triglycerides': r'triglyceride',
            'creatinine': r'creatinine',
            'hematocrit': r'hematocrit|hct',
            'mcv': r'mcv',
            'mch': r'mch(?!\s*c)',
            'mchc': r'mchc',
        }
        
    def extract_patient_info(self, text):
        """Extract patient information from report"""
        patient_info = {}
        
        name_match = re.search(r'patient\s+name[:\s]+([a-z\s]+)', text, re.IGNORECASE)
        if name_match:
            patient_info['name'] = name_match.group(1).strip().title()
        
        id_match = re.search(r'patient\s+id[:\s]+([a-z0-9]+)', text, re.IGNORECASE)
        if id_match:
            patient_info['id'] = id_match.group(1).strip().upper()
        
        age_match = re.search(r'age[:\s]+(\d+)', text, re.IGNORECASE)
        if age_match:
            patient_info['age'] = age_match.group(1)
        
        gender_match = re.search(r'gender[:\s]+(male|female)', text, re.IGNORECASE)
        if gender_match:
            patient_info['gender'] = gender_match.group(1).capitalize()
        
        date_match = re.search(r'date\s+of\s+collection[:\s]+(\d{4}-\d{2}-\d{2})', text, re.IGNORECASE)
        if date_match:
            patient_info['collection_date'] = date_match.group(1)
            
        report_date_match = re.search(r'report\s+date[:\s]+(\d{4}-\d{2}-\d{2})', text, re.IGNORECASE)
        if report_date_match:
            patient_info['report_date'] = report_date_match.group(1)
        
        return patient_info
    
    def extract_test_results(self, text):
        """Extract test results from report"""
        test_results = []
        lines = text.split('\n')
        
        for line in lines:
            if not line.strip():
                continue
            if any(header in line.lower() for header in ['test name', 'result', 'normal range', '===', '---']):
                continue
            
            test_data = self._parse_test_line(line)
            if test_data:
                test_results.append(test_data)
        
        return test_results
    
    def _parse_test_line(self, line):
        """Parse a single line to extract test information"""
        line = ' '.join(line.split())
        
        if len(line) < 10:
            return None
        
        test_name = None
        for test_key, pattern in self.test_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                name_match = re.match(r'^([a-z\s\(\)]+)', line, re.IGNORECASE)
                if name_match:
                    test_name = name_match.group(1).strip()
                break
        
        if not test_name:
            return None
        
        value_match = re.search(r'(\d+\.?\d*)\s+', line)
        if not value_match:
            return None
        
        value = float(value_match.group(1))
        
        range_match = re.search(r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)', line)
        if range_match:
            min_val = float(range_match.group(1))
            max_val = float(range_match.group(2))
            normal_range = f"{min_val} - {max_val}"
        else:
            less_match = re.search(r'less than\s+(\d+\.?\d*)', line, re.IGNORECASE)
            greater_match = re.search(r'greater than\s+(\d+\.?\d*)', line, re.IGNORECASE)
            
            if less_match:
                normal_range = f"< {less_match.group(1)}"
                min_val = 0
                max_val = float(less_match.group(1))
            elif greater_match:
                normal_range = f"> {greater_match.group(1)}"
                min_val = float(greater_match.group(1))
                max_val = float('inf')
            else:
                normal_range = "Not specified"
                min_val = None
                max_val = None
        
        unit_match = re.search(r'([a-z/%^]+)$', line, re.IGNORECASE)
        if unit_match:
            unit = unit_match.group(1)
        else:
            unit = ""
        
        return {
            'test_name': test_name,
            'value': value,
            'normal_range': normal_range,
            'min_normal': min_val,
            'max_normal': max_val,
            'unit': unit
        }
    
    def extract_all(self, text):
        """Extract all entities from medical report"""
        logger.info("Extracting entities from medical report...")
        
        patient_info = self.extract_patient_info(text)
        test_results = self.extract_test_results(text)
        
        logger.info(f"Extracted {len(test_results)} test results")
        
        return {
            'patient_info': patient_info,
            'test_results': test_results,
            'total_tests': len(test_results)
        }


def extract_entities(text):
    """Convenience function to extract entities"""
    extractor = MedicalEntityExtractor()
    return extractor.extract_all(text)
