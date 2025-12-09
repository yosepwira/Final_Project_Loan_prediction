import os
import joblib
import onnxruntime as rt
import numpy as np
import json

# Load Config
def load_grade_map():
    # load from json file
    base_dir = os.getcwd()
    file_path = os.path.join(base_dir, 'parameter', 'grade_map.json')


# Default Dictionary (Cadangan jika file JSON hilang/rusak)
    default_map = {
        'A': 1.0, 'B': 2.0, 'C': 3.0, 
        'D': 4.0, 'E': 5.0, 'F': 6.0, 'G': 7.0
    }


    try : 
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f) # set dictionary python
        else :
            return default_map
    except Exception as e : 
        print(f"Error loading grade map: {e}")
        return default_map 

# Set Global Variable    
GRADE_MAP = load_grade_map()

def get_model_paths():
    base_dir = os.getcwd()
    model_path = os.path.join(base_dir, 'model', 'loan_model.onnx')
    le_path = os.path.join(base_dir, 'model', 'label_encoder_v2.pkl')
    return model_path, le_path 

def load_resources():
    model_path, le_path = get_model_paths()
    session = None
    le = None 
    input_name = None
    label_name = None 
    error = None 

    try:
        session = rt.InferenceSession(model_path)
        le = joblib.load(le_path)
        input_name = session.get_inputs()[0].name
        label_name = session.get_outputs()[0].name

    except Exception as e:
        error = f"Error loading resources: {e}"

    return session, le, input_name, label_name, error

def process_prediction(session, le, input_name, label_name, amount, term, rate_percent, installment, grade_huruf):

    try:
        rate_decimal = rate_percent / 100.0
        # Map grade
        grade_angka = GRADE_MAP.get(grade_huruf, 4.0)  # Default to 4.0 if not found

        input_data = np.array([[amount, term, rate_decimal, installment, grade_angka]], dtype=np.float32)

        pred_idx = session.run([label_name], {input_name : input_data})[0]
        pred_label = le.inverse_transform(pred_idx)[0]

        recommendation = "" 
        status = ""

        if "Prime" in pred_label:
            status = "success"
            recommendation = "✅ **APPROVE:** Nasabah Premium (Risiko Rendah)"
        elif "Standard" in pred_label:
            status = "info"
            recommendation = "ℹ️ **APPROVE:** Nasabah Standar"
        elif "Subprime" in pred_label:
            status = "warning"
            recommendation = "⚠️ **REVIEW:** Perlu Agunan tambahan / bunga tinggi" 
        elif "Macet" in pred_label: 
            status = "error"
            recommendation = "❌ **REJECT:** Risiko Gagal Bayar Tinggi"
        else:
            status = "info"
            recommendation = f"Kategori : {pred_label}"


        return pred_label, recommendation, status

    except Exception as e:
        return None, f"Error during prediction: {e}", "Error"    

        

