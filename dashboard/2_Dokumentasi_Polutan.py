import streamlit as st

# Judul Halaman
st.title('Dokumentasi Polutan dan Dampaknya')

# Deskripsi Singkat
st.markdown("""
Halaman ini menjelaskan berbagai jenis polutan udara, sumbernya, dan dampaknya terhadap kesehatan manusia dan lingkungan.
""")

# Informasi Polutan
polutan_info = {
    "PM2.5": "Partikel udara halus berukuran ≤2.5 µm. Dapat masuk ke paru-paru dan aliran darah, menyebabkan penyakit kardiovaskular dan pernapasan.",
    "PM10": "Partikel udara kasar berukuran ≤10 µm. Biasanya berasal dari debu jalanan, konstruksi, dan aktivitas industri.",
    "SO2": "Sulfur dioksida, berasal dari pembakaran batu bara dan bahan bakar fosil. Dapat menyebabkan iritasi saluran pernapasan.",
    "NO2": "Nitrogen dioksida, dihasilkan dari emisi kendaraan dan industri. Memperburuk asma dan menurunkan fungsi paru.",
    "CO": "Karbon monoksida, gas beracun tak berbau dari pembakaran bahan bakar. Mengganggu distribusi oksigen dalam tubuh.",
    "O3": "Ozon troposfer, terbentuk dari reaksi kimia antara NOx dan VOC di bawah sinar matahari. Memicu iritasi saluran napas dan mata."
}

# Tampilkan Informasi Polutan
for polutan, deskripsi in polutan_info.items():
    st.subheader(polutan)
    st.markdown(deskripsi)
    st.divider()

# Tambahkan Sumber Referensi
st.markdown("""
### Sumber:
- [WHO Air Quality Guidelines](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health)
- [US Environmental Protection Agency (EPA)](https://www.epa.gov/air-pollution)
""")
