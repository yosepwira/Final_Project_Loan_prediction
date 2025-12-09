import os
import json
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler # Import ini jika Anda melatih dan menyimpan StandardScaler

def load_cluster_map():
    """
    Memuat peta (map) interpretasi bisnis untuk setiap klaster (K=8).
    Kriteria didasarkan pada Centroid (rata-rata fitur) yang dianalisis.
    """
    default_cluster = {
        # Kunci klaster menggunakan string untuk kompatibilitas JSON
        # 🟢 Kualitas Terbaik & Terbesar
        "0": "The Best. ",
        "4": "Better",

        # 🟡 Kualitas Menengah (Monitor)
        "2": "Good (Needs Monitoring)",

        
        # 🟠 Risiko Tinggi (Perhatian)
        "3": "Medium Risk. (Late Payment Monitor)",

        # 🔴 Risiko KRITIS (Collection)
        "1": "High Risk. (Collection Needed)",
    }
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..' ,'model', 'cluster_map.json')

    try:
        # Coba muat dari file JSON jika ada
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        else:
            # Jika file tidak ada, kembalikan default
            return default_cluster
    except Exception:
        # Jika terjadi error saat memuat/membaca, kembalikan default
        return default_cluster
    
# Definisikan fitur yang digunakan dalam model (sesuai dengan urutan saat training)
FEATURES = [
    'amount_borrowed', 
    'borrower_rate', 
    'installment',
    'term', 
    'borrower_rate',
    'grade_encoded'
]

def load_scaler():
    """
    Memuat objek StandardScaler yang digunakan saat training.
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))
    # SCALER_PATH = os.path.join(base_dir, 'model', 'scaler.pkl')
    SCALER_PATH = os.path.join(base_dir, '..', 'model', 'scaler.pkl')
    
    try:
        scaler = joblib.load(SCALER_PATH)
        return scaler
    except Exception as e:
        print(f"ERROR: Gagal memuat scaler. Pastikan file 'scaler.pkl' ada di folder 'model'. Detail: {e}")
        # Jika gagal, kembalikan scaler baru (tetapi hasil prediksi akan tidak akurat!)
        return StandardScaler()    

