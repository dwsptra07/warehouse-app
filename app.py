import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- PENGATURAN TAMPILAN & TEMA BAJAK LAUT ---
st.set_page_config(
    page_title="Pusat Logistik Bajak Laut - Warehouse",
    page_icon="🏴‍☠️",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        background-color: #d4af37;
        color: #000000;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid #b8860b;
    }
    .stButton>button:hover {
        background-color: #ffd700;
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# --- KONEKSI GOOGLE SHEETS ---
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- KONEKSI GOOGLE SHEETS CLOUD (VERSI TERBARU) ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def init_connection():
    try:
        # Cek apakah berjalan di Streamlit Cloud menggunakan st.secrets
        if hasattr(st, "secrets") and "gcp_service_account" in st.secrets:
            creds_dict = dict(st.secrets["gcp_service_account"])
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        else:
            # Jika berjalan di laptop lokal menggunakan file credentials.json
            creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

        client = gspread.authorize(creds)
        spreadsheet = client.open("Monitoring Serah Terima Part Service")
        sheet = spreadsheet.get_worksheet(0)
        return sheet
    except Exception as e:
        st.error(f"Detail Error Koneksi: {e}")
        return None

sheet = init_connection()

# --- DAFTAR AKUN & HAK AKSES KRU TERBARU ---
AKUN_KRU = {
    "Putra": {"pass": "2626", "role": "Kapten"},
    "Dimas": {"pass": "dimas123", "role": "Kru"},
    "Robih": {"pass": "robih123", "role": "Kru"},
    "Cinta": {"pass": "cinta123", "role": "Kru"},
    "Ali": {"pass": "ali123", "role": "Kru"},
    "Dio": {"pass": "dio123", "role": "Kru"},
    "Rindi": {"pass": "rindi123", "role": "Kru"},
    "Amirudin": {"pass": "amir123", "role": "Kapten"}
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# --- SISTEM LOGIN SIDEBAR ---
st.sidebar.markdown("# 🏴‍☠️ KELOMPOK KAPAL WHS")
st.sidebar.markdown("---")

if not st.session_state.logged_in:
    st.sidebar.subheader("🔐 Gerbang Masuk Kru")
    input_user = st.sidebar.selectbox("Pilih Nama Kru", list(AKUN_KRU.keys()))
    input_pass = st.sidebar.text_input("Kata Sandi / Kunci", type="password")
    
    if st.sidebar.button("⚓ Naik ke Kapal (Login)"):
        if input_pass == AKUN_KRU[input_user]["pass"]:
            st.session_state.logged_in = True
            st.session_state.username = input_user
            st.session_state.role = AKUN_KRU[input_user]["role"]
            st.rerun()
        else:
            st.sidebar.error("❌ Kata sandi salah, Kapten!")
            
    st.title("🏴‍☠️ PUSAT LOGISTIK & SERAH TERIMA PART SERVICE WAREHOUSE")
    st.markdown("### *Selamat datang di pelabuhan data Warehouse! Silakan login melalui panel di sebelah kiri untuk mulai berlayar.*")
    st.info("💡 Hubungi Kapten (Putra) jika belum memiliki kunci sandi kru.")

else:
    # Status Login di Sidebar
    role_badge = "👑 KAPTEN" if st.session_state.role == "Kapten" else "⚓ KRU WAREHOUSE"
    st.sidebar.success(f"🟢 **{st.session_state.username}**\n*{role_badge}*")
    
    if st.sidebar.button("🚪 Turun Kapal (Logout)"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()
        
    st.sidebar.markdown("---")
    
    # Menu Berdasarkan Hak Akses
    if st.session_state.role == "Kapten":
        menu = st.sidebar.radio("🗺️ Rute Pelayaran Kapten:", [
            "⚓ Dek Utama (Input WO)", 
            "📜 Peta Harta Karun (Monitoring & Download)", 
            "🎯 Perintah Misi Pengambilan Part"
        ])
    else:
        menu = st.sidebar.radio("🗺️ Rute Pelayaran Kru:", [
            "⚓ Dek Utama (Input WO)", 
            "📜 Peta Harta Karun (Monitoring & Download)",
            "🎯 Misi Tugas Saya"
        ])

    if sheet is None:
        st.error("❌ Google Sheets belum terhubung. Periksa kembali nama file atau credentials.json!")
    else:
        # --- MENU 1: DEK UTAMA (INPUT WO) ---
        if menu == "⚓ Dek Utama (Input WO)":
            st.title("🏴‍☠️ Dek Utama: Pencatatan Part Service")
            st.markdown(f"*Ahoy, **{st.session_state.username}**! Catat harta karun Part Service baru di sini tanpa takut nomor WO ganda.*")
            
            with st.form("pirate_entry_form", clear_on_submit=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    tgl_wo = st.date_input("Tanggal WO Diterima", value=datetime.today())
                    no_wo = st.text_input("No WO (Wajib Diisi)")
                    unit = st.selectbox("Unit", ["TL5122", "EX2000", "HD785", "PC1250", "Lainnya"])
                    section = st.selectbox("Section", ["SUPPORT", "PRODUCTION", "PLANT", "LOGISTICS"])
                    
                with col2:
                    pic_terima_doc = st.text_input("PIC Penerima Doc. WO", value=st.session_state.username)
                    tgl_sch = st.date_input("Tanggal SCH Service", value=datetime.today())
                    no_pr = st.text_input("No PR", value="STOCK")
                    
                with col3:
                    pic_proses_pr = st.text_input("PIC Proses No PR")
                    status_supply = st.selectbox("Status Supply to User", ["WAITING", "PROCESS", "COMPLETED"])
                    pic_terima_part = st.text_input("PIC Penerima Part")
                    no_gi = st.text_input("No GI")
                    
                submit_button = st.form_submit_button("🚀 Labuhkan Data ke Google Sheets")
                
                if submit_button:
                    if not no_wo.strip():
                        st.warning("⚠️ Peringatan Kapten: Nomor WO wajib diisi!")
                    else:
                        try:
                            max_attempts = 3
                            for attempt in range(max_attempts):
                                try:
                                    existing_data = sheet.get_all_values()
                                    is_duplicate = False
                                    if len(existing_data) > 1:
                                        for row in existing_data[1:]:
                                            if len(row) > 1 and row[1].strip().lower() == no_wo.strip().lower():
                                                is_duplicate = True
                                                break
                                    
                                    if is_duplicate:
                                        st.error(f"❌ Gagal! Nomor WO **{no_wo}** sudah pernah tercatat dalam buku log pelayaran.")
                                        break
                                    else:
                                        row_data = [
                                            str(tgl_wo),
                                            no_wo.strip(),
                                            unit,
                                            section,
                                            pic_terima_doc,
                                            str(tgl_sch),
                                            no_pr,
                                            pic_proses_pr,
                                            status_supply,
                                            pic_terima_part,
                                            no_gi
                                        ]
                                        sheet.append_row(row_data)
                                        st.success(f"🎉 Hore! Data No WO **{no_wo}** berhasil diamankan ke dalam Google Sheets.")
                                        break
                                except Exception as inner_e:
                                    if attempt == max_attempts - 1:
                                        raise inner_e
                        except Exception as e:
                            st.error(f"Terjadi badai jaringan saat menyimpan data: {e}. Silakan klik tombol simpan sekali lagi!")

        # --- MENU 2: PETA HARTA KARUN (MONITORING & DOWNLOAD) ---
        elif menu == "📜 Peta Harta Karun (Monitoring & Download)":
            st.title("📜 Peta Harta Karun: Arsip & Monitoring WO")
            st.markdown("*Cari data pelayaran lama atau unduh laporan lengkap untuk dibagikan ke markas besar.*")
            
            try:
                all_data = sheet.get_all_values()
                if len(all_data) > 1:
                    header = all_data[0]
                    rows = all_data[1:]
                    
                    df = pd.DataFrame(rows, columns=header)
                    
                    search_query = st.text_input("🔍 Cari Berdasarkan Nomor WO:")
                    if search_query:
                        df_filtered = df[df.iloc[:, 1].str.contains(search_query, case=False, na=False)]
                    else:
                        df_filtered = df
                        
                    st.dataframe(df_filtered, use_container_width=True)
                    
                    csv_data = df_filtered.to_csv(index=False, sep=';').encode('utf-8')
                    st.download_button(
                        label="📥 Unduh Buku Log (Format Excel/CSV Rapi)",
                        data=csv_data,
                        file_name="Buku_Log_Warehouse_Bajak_Laut.csv",
                        mime="text/csv",
                    )
                else:
                    st.info("Peti harta karun masih kosong, Kapten. Belum ada data tersimpan.")
            except Exception as e:
                st.warning("⚠️ Koneksi ke server terganggu ombak. Silakan muat ulang halaman web.")

        # --- MENU 3A: PERINTAH MISI KAPTEN (KHUSUS KAPTEN) ---
        elif menu == "🎯 Perintah Misi Pengambilan Part" and st.session_state.role == "Kapten":
            st.title("🎯 Papan Perintah Misi & Tugas Kru")
            st.markdown("*Berikan instruksi khusus atau penugasan pengambilan part kepada kru warehouse di bawah komandomu.*")
            
            # Daftar pilihan kru untuk tugas (mengambil dari list nama kru selain kapten yang sedang login)
            daftar_kru_tugas = [k for k, v in AKUN_KRU.items() if v["role"] == "Kru"]
            
            with st.form("mission_form"):
                st.subheader("Buat Perintah Pengambilan Part Baru")
                c1, c2 = st.columns(2)
                with c1:
                    target_kru = st.selectbox("Tugaskan Kepada Kru", daftar_kru_tugas)
                    no_wo_target = st.text_input("Nomor WO Terkait")
                with c2:
                    prioritas = st.selectbox("Tingkat Urgensi", ["Normal", "Urgent / Segera", "Darurat Unit Down"])
                    
                catatan_misi = st.text_area("Instruksi / Catatan Pengambilan Part (Cth: Ambil di Rak A-2, pastikan part segel utuh)")
                
                kirim_misi = st.form_submit_button("📢 Kirim Perintah ke Kru")
                if kirim_misi:
                    if not no_wo_target.strip():
                        st.warning("⚠️ Masukkan Nomor WO yang akan ditugaskan!")
                    else:
                        if "list_misi" not in st.session_state:
                            st.session_state.list_misi = []
                        
                        st.session_state.list_misi.append({
                            "kru": target_kru,
                            "wo": no_wo_target,
                            "prioritas": prioritas,
                            "catatan": catatan_misi,
                            "status": "Belum Diambil"
                        })
                        st.success(f"🎉 Perintah misi untuk **{target_kru}** (No WO: {no_wo_target}) berhasil dikirim!")

            st.markdown("---")
            st.subheader("📋 Daftar Misi Aktif yang Diberikan")
            if "list_misi" in st.session_state and len(st.session_state.list_misi) > 0:
                df_misi = pd.DataFrame(st.session_state.list_misi)
                st.dataframe(df_misi, use_container_width=True)
            else:
                st.info("Belum ada misi aktif yang diberikan ke kru saat ini.")

        # --- MENU 3B: MISI TUGAS SAYA (KHUSUS KRU) ---
        elif menu == "🎯 Misi Tugas Saya":
            st.title(f"🎯 Papan Misi Tugas: {st.session_state.username}")
            st.markdown("*Berikut adalah daftar perintah atau tugas pengambilan part yang diberikan oleh Kapten untukmu.*")
            
            if "list_misi" in st.session_state:
                misi_kru = [m for m in st.session_state.list_misi if m["kru"] == st.session_state.username]
                
                if len(misi_kru) > 0:
                    for idx, misi in enumerate(misi_kru):
                        with st.expander(f"📦 Misi No WO: {misi['wo']} (Prioritas: {misi['prioritas']})"):
                            st.write(f"**Instruksi Kapten:** {misi['catatan']}")
                            st.write(f"**Status Saat Ini:** `{misi['status']}`")
                            
                            if misi['status'] == "Belum Diambil":
                                if st.button(f"✅ Tandai Selesai (Diambil)", key=f"btn_misi_{idx}"):
                                    misi['status'] = "Selesai Diambil"
                                    st.success("Misi berhasil diselesaikan! Kerja bagus, kawan!")
                                    st.rerun()
                            else:
                                st.info("✨ Misi ini sudah selesai dikerjakan.")
                else:
                    st.info("⚓ Belum ada tugas misi khusus untukmu saat ini. Istirahat yang cukup atau bantu rekan yang lain!")
            else:
                st.info("⚓ Belum ada misi dari Kapten untuk saat ini.")
