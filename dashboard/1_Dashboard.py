import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
from streamlit_folium import folium_static

# Load data with caching
@st.cache_data
def load_data():
    data = pd.read_csv('dashboard/all_data.csv')
    data['mean_all_pollutants'] = data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean(axis=1)
    return data

data = load_data()

# Sidebar navigasi
st.sidebar.title('Navigasi')
page = st.sidebar.radio('Pilih Halaman:', ['Dashboard', 'Dokumentasi Polutan'])

# Loading indicator
with st.spinner('Memuat data...'):
    st.success('Data berhasil dimuat!')

# Halaman Dashboard
if page == 'Dashboard':
    st.title('Dashboard Kualitas Udara Beijing')

    # Korelasi Antar-Polutan
    st.subheader('Korelasi Antar-Polutan')
    fig, ax = plt.subplots(figsize=(10, 8))
    kolom_numerik = data.select_dtypes(include=['float64', 'int64']).columns
    sns.heatmap(data[kolom_numerik].corr(), annot=True, cmap='coolwarm', fmt='.2f', annot_kws={'size': 8}, square=True, cbar=True, linewidths=0.5, linecolor='black', ax=ax)
    ax.set_title('Heatmap Korelasi Antar-Polutan', fontsize=14)
    st.pyplot(fig)

    # Polutan per Musim
    st.subheader('Polutan per Musim')
    musim_avg = data.groupby('season')[kolom_numerik].mean().reset_index()
    polutan = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    fig = px.line(musim_avg, x='season', y=polutan, title='Rata-rata Polutan per Musim')
    st.plotly_chart(fig)

    # Perbandingan Siang vs Malam
    st.subheader('Perbandingan Polusi Siang dan Malam')
    time_avg = data.groupby('time_of_day')[kolom_numerik].mean().reset_index()
    fig = px.bar(time_avg, x='time_of_day', y=polutan, title='Rata-rata Polutan Siang vs Malam')
    st.plotly_chart(fig)

        # Peta Lokasi Stasiun
    st.subheader('Peta Lokasi Stasiun dan Rata-rata Polusi')
    map = folium.Map(location=[39.9042, 116.4074], zoom_start=10)

    # Cek apakah lat dan lon tersedia, jika tidak tambahkan secara manual
    lokasi_stasiun = {
        'Aotizhongxin': [39.982, 116.417],
        'Changping': [40.226, 116.231],
        'Dongsi': [39.929, 116.417],
        'Guanyuan': [39.932, 116.339],
        'Huairou': [40.363, 116.631],
        'Nongzhanguan': [39.949, 116.461],
        'Shunyi': [40.127, 116.656],
        'Tiantan': [39.882, 116.406],
        'Wanliu': [39.988, 116.304],
        'Wanshouxigong': [39.872, 116.339],
        'Gucheng': [39.913, 116.189],
        'Dingling': [40.289, 116.220]
    }

    if 'lat' not in data.columns or 'lon' not in data.columns:
        data['lat'] = data['station'].map(lambda x: lokasi_stasiun.get(x, [None, None])[0])
        data['lon'] = data['station'].map(lambda x: lokasi_stasiun.get(x, [None, None])[1])

    # Agregasi data untuk mengurangi jumlah titik di peta
    aggregated_data = data.groupby('station').agg({
        'lat': 'first',
        'lon': 'first',
        'mean_all_pollutants': 'mean'
    }).reset_index()

    for _, row in aggregated_data.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=7,
            color='red' if row['mean_all_pollutants'] > 250 else 'orange',
            fill=True,
            fill_opacity=0.7,
            popup=f"{row['station']}: {row['mean_all_pollutants']:.2f} µg/m³"
        ).add_to(map)

    folium_static(map)

    # Filter Sidebar
    season = st.sidebar.selectbox('Pilih Musim:', data['season'].dropna().unique())
    filtered_data = data[data['season'] == season]
    st.write(f'Data untuk Musim {season}', filtered_data)

    pm25_filter = st.sidebar.slider('Filter PM2.5:', 0, int(data['PM2.5'].max()), (0, 100))
    st.write('Data dengan PM2.5 dalam rentang:', pm25_filter)
    st.write(data[(data['PM2.5'] >= pm25_filter[0]) & (data['PM2.5'] <= pm25_filter[1])])

    # Download Data
    st.download_button('Unduh Data', data.to_csv().encode('utf-8'), 'air_quality_data.csv', 'text/csv')

# Halaman Dokumentasi Polutan
elif page == 'Dokumentasi Polutan':
    st.title('Dokumentasi Polutan dan Dampaknya')

    polutan_info = {
        'PM2.5': 'Partikel udara halus berukuran ≤2.5 µm. Bisa masuk ke paru-paru dan aliran darah.',
        'PM10': 'Partikel kasar berukuran ≤10 µm. Berasal dari debu jalanan dan konstruksi.',
        'SO2': 'Sulfur dioksida, dihasilkan dari pembakaran batu bara dan bahan bakar fosil.',
        'NO2': 'Nitrogen dioksida, berasal dari kendaraan dan industri.',
        'CO': 'Karbon monoksida, gas beracun dari pembakaran bahan bakar.',
        'O3': 'Ozon troposfer, terbentuk dari reaksi fotokimia.'
    }

    for polutan, deskripsi in polutan_info.items():
        st.subheader(polutan)
        st.markdown(deskripsi)
        st.divider()

    st.markdown('### Sumber:')
    st.markdown('- [WHO Air Quality Guidelines](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health)')
    st.markdown('- [US Environmental Protection Agency (EPA)](https://www.epa.gov/air-pollution)')
