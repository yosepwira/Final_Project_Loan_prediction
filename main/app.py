# app.py

import streamlit as st
import numpy as np
import onnxruntime as ort
from utils import load_cluster_map, load_scaler, FEATURES # Import dari utils.py
import os 

# --- 1. SETUP MODEL & UTILS ---

# path model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..' ,'model', 'loan_model.onnx')

# Model ONNX, Scaler, and Cluster Map
@st.cache_resource
def setup_models():
    """Memuat model ONNX, scaler, dan cluster map."""
    try:
        # Load ONNX Session
        session = ort.InferenceSession(MODEL_PATH)
        # Load Scaler
        scaler = load_scaler()
        # Load Cluster Map
        cluster_map = load_cluster_map()
        
        return session, scaler, cluster_map
    except Exception as e:
        st.error(f"Gagal memuat model atau scaler. Pastikan file 'loan_model.onnx' dan 'scaler.pkl' ada di folder 'model'. Detail: {e}")
        return None, None, None

# --- 2. LOGIKA PREDIKSI ---

def predict_and_interpret(features_input, ort_session, scaler, cluster_map):
 
    # 1. Scaling Input
    input_array = np.array(features_input).reshape(1, -1)
    scaled_input = scaler.transform(input_array)
    
    # 2. Prediksi ONNX (Model Klasifikasi Risiko Biner: 0 atau 1)
    input_name = ort_session.get_inputs()[0].name
    ort_inputs = {input_name: scaled_input.astype(np.float32)}
    ort_outs = ort_session.run(None, ort_inputs)
    

    predicted_class = ort_outs[0][0] 
  
    
    if features_input[4] <= 2 and features_input[0] <= 10000: # Grade A/B dan Pinjaman Kecil
        cluster_id = 4
    elif features_input[4] >= 5: # Grade E/F/G
        cluster_id = 2
    else:
        # Gunakan Klaster 1 (Medium Risiko) sebagai default jika tidak ekstrem
        cluster_id = 1 
        
    # 3. Interpretasi Bisnis
    cluster_desc = cluster_map.get(str(cluster_id), "Klaster Tidak Dikenal")
    
    return predicted_class, cluster_desc

# --- 3. TAMPILAN STREAMLIT ---

# Muat model, scaler, dan cluster map di awal
ort_session, scaler, cluster_map = setup_models()

if ort_session and scaler and cluster_map:
    st.title("Mini Project Loan Risk Assessment 🏦")
    st.markdown("Aplikasi prediksi risiko pinjaman (menggunakan **Model ONNX**) dan interpretasi bisnis (menggunakan **K-Means Cluster Map**).")


    with st.form("input_form"):
        # Input from users
        col1, col2 = st.columns(2)
        
        # position must sequence according to FEATURES
        amount_borrowed = col1.number_input(f"1. Nilai Pinjaman (IDR)", min_value=1000, max_value=35000, value=15000, key="f1")
        borrower_rate = col1.number_input("2. Suku Bunga (0.05 - 0.35)", min_value=0.05, max_value=0.35, value=0.15, step=0.01, key="f2")
        installment = col2.number_input("3. Cicilan Bulanan (IDR)", min_value=50.0, max_value=1500.0, value=400.0, key="f3")
        term = st.selectbox("4. Tenor Cicilan", options=[6, 12, 18, 24, 36, 42, 60], index=2, key="f4")
        grade_encoded = st.selectbox("5. Grade Nasabah (1=A hingga 7=G)", options=[1, 2, 3, 4, 5, 6, 7], index=2, key="f5") # Default C=3


        submitted = st.form_submit_button("Prediksi Risiko & Dapatkan Skenario")

        if submitted:
            # INPUT DATA
            input_features = [amount_borrowed, borrower_rate, installment, term,borrower_rate, float(grade_encoded)]
            
            with st.spinner("Memproses prediksi..."):
                predicted_class, interpretation = predict_and_interpret(input_features, ort_session, scaler, cluster_map)
                
                st.subheader("✅ Hasil Prediksi Risiko & Skenario Bisnis")
                
                # show prediction result
                risk_label = "Risiko Default TINGGI (1)" if predicted_class >= 0.5 else "Risiko Default RENDAH (0)"
                st.metric("Prediksi Model Biner", risk_label)
                
              
                st.markdown(f"**Interpretasi Cluster**: {interpretation}")
                
                # Business Scenario based on interpretation
                if "High Risk" in interpretation in interpretation:
                    st.error("🚨 Kategori Bisnis: RISIKO TINGGI / NPL. Perlu verifikasi ketat atau tindakan collection.")
                elif "Medium Risk" in interpretation:
                    st.success("🟢 Kategori Bisnis: RISIKO MEDIUM. Tingkat DPD tinggi. Target untuk refinancing yang agresif.")                    
                elif "Good" in interpretation or "Better" in interpretation or "The Best" in interpretation:
                    st.success("🟢 Kategori Bisnis: BEST DEAL. Lakukan Tindak Lanjut Prioritas & Tawarkan *Upselling*.")
                else:
                    st.warning("🟡 Kategori Bisnis: MEDIUM Risiko. Lakukan Pemantauan Standar.")

