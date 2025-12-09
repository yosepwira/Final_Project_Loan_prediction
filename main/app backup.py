import streamlit as st
import utils 

# config page
st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon = "🏦",
    layout="centered"
)

# load by cache
@st.cache_resource
def init_system():
    return utils.load_resources()

# call function load from utils
session, le, input_name, label_name, error_msg = init_system()

# check if found error when load resources
if error_msg:
    st.error(f" Failed load resources: {error_msg}")
    st.stop() #stop execution

# UI HEADER
st.title("🏦 Loan Approval Prediction System")
st.markdown("""
Aplikasi ini menggunakan **Machine Learning (XGBoost + ONNX)** untuk menilai profil risiko nasabah.
Silakan masukkan parameter pinjaman di bawah ini.
""")
st.divider()

# UI : Form input
col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Jumlah Pinjaman (Rp)", min_value=100, max_value=10000000, value=50000, step=500)
    term = st.selectbox("Jangka Waktu Pinjaman", options=[6, 12, 24, 36, 48, 60], index=1)
    rate_percent = st.slider("Tingkat Suku Bunga (%)", min_value=1.0, max_value=20.0, value=12.0, step=0.1)

with col2: 
    installment = st.number_input("Cicilan per Bulan ($)", min_value=10.0, value=300.0, step=10.0)
    
    # Ambil daftar Grade langsung dari utils (agar sinkron dengan backend)
    # Kita sort agar urut A, B, C...
    daftar_grade = sorted(list(utils.GRADE_MAP.keys()))
    grade_huruf = st.selectbox("Grade Nasabah", options=daftar_grade)

# --- 5. LOGIKA EKSEKUSI ---
if st.button("🔍 Analisa Risiko", use_container_width=True):
    
    # Tampilkan spinner loading biar terlihat canggih
    with st.spinner('AI sedang menganalisis profil nasabah...'):
        
        # Panggil fungsi "otak" dari utils
        label_hasil, pesan_rekomendasi, status_warna = utils.process_prediction(
            session, le, input_name, label_name,
            amount, term, rate_percent, installment, grade_huruf
        )

    st.divider()

    # --- 6. TAMPILKAN HASIL ---
    if label_hasil:
        st.subheader("📝 Hasil Keputusan AI")
        
        # Tampilkan Alert Dinamis sesuai status (success/info/warning/error)
        if status_warna == "success":
            st.success(f"**Kategori: {label_hasil}**")
            st.markdown(pesan_rekomendasi)
            st.balloons() # Efek balon jika nasabah bagus
            
        elif status_warna == "info":
            st.info(f"**Kategori: {label_hasil}**")
            st.markdown(pesan_rekomendasi)
            
        elif status_warna == "warning":
            st.warning(f"**Kategori: {label_hasil}**")
            st.markdown(pesan_rekomendasi)
            
        elif status_warna == "error":
            st.error(f"**Kategori: {label_hasil}**")
            st.markdown(pesan_rekomendasi)
    else:
        # Jika return None (Error system)
        st.error(pesan_rekomendasi)

# Footer
st.markdown("---")
st.caption("🚀 Powered by ONNX Runtime & XGBoost | V1.0")