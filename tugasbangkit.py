import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    hour_data = pd.read_csv('hour.csv')
    day_data = pd.read_csv('day.csv')
    return hour_data, day_data

# Muat data
hour_data, day_data = load_data()

# Pastikan kolom dteday adalah tipe datetime
day_data['dteday'] = pd.to_datetime(day_data['dteday'])

# Judul aplikasi
st.title("Data Analysis of Bike-Sharing")

# Penjelasan awal
st.markdown("""
Bike sharing systems are new generation of traditional bike rentals where the whole process from membership, rental, and return back has become automatic. Through these systems, users are able to easily rent a bike from a particular position and return it at another position. Currently, there are about over 500 bike-sharing programs around the world which is composed of over 500 thousand bicycles. Today, there exists great interest in these systems due to their important role in traffic, environmental, and health issues.

Apart from interesting real-world applications of bike sharing systems, the characteristics of data being generated by these systems make them attractive for research. Opposed to other transport services such as bus or subway, the duration of travel, departure, and arrival position is explicitly recorded in these systems. This feature turns bike sharing systems into a virtual sensor network that can be used for sensing mobility in the city. Hence, it is expected that most of the important events in the city could be detected via monitoring these data.
""")

# Pilih dataset
dataset_option = st.selectbox("Pilih dataset untuk ditampilkan:", ["Hour Data", "Day Data"])

if dataset_option == "Day Data":
    # Tampilkan data harian
    st.subheader("Data Sewa Sepeda per Hari")
    st.dataframe(day_data)

    # Visualisasi penjualan per hari
    st.subheader("Penjualan per Hari")
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='dteday', y='cnt', data=day_data)
    plt.title("Penjualan Sepeda per Hari")
    plt.xlabel("Tanggal")
    plt.ylabel("Jumlah Sewa")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Statistik deskriptif
    st.subheader("Statistik Deskriptif Penjualan per Hari")
    st.write(day_data['cnt'].describe())

    # Scatterplot
    st.subheader("Scatterplot dari cnt terhadap Fitur Lainnya")
    features = ['temp', 'atemp', 'hum', 'windspeed']
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    for i, feature in enumerate(features):
        ax = axes[i // 2, i % 2]
        sns.scatterplot(x=feature, y='cnt', data=day_data, ax=ax)
        ax.set_title(f'Scatterplot cnt vs {feature}')
        correlation = day_data['cnt'].corr(day_data[feature])
        ax.text(0.5, 0.9, f'Correlation: {correlation:.2f}', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_xlabel(feature)
        ax.set_ylabel('Jumlah Sewa')
    plt.tight_layout()
    st.pyplot(fig)

elif dataset_option == "Hour Data":
    # Tampilkan data per jam
    st.subheader("Data Sewa Sepeda per Jam")
    st.dataframe(hour_data)

    # Visualisasi penjualan per jam
    st.subheader("Penjualan per Jam")
    plt.figure(figsize=(10, 5))
    sns.barplot(x='hr', y='cnt', data=hour_data)
    plt.title("Penjualan Sepeda per Jam")
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Sewa")
    st.pyplot(plt)

    # Statistik deskriptif
    st.subheader("Statistik Deskriptif Penjualan per Jam")
    st.write(hour_data['cnt'].describe())

    # Visualisasi berdasarkan kondisi cuaca
    st.subheader("Jumlah Sewa berdasarkan Kondisi Cuaca")
    plt.figure(figsize=(10, 5))
    sns.countplot(x='weathersit', data=hour_data)
    plt.title("Jumlah Sewa per Kondisi Cuaca")
    plt.xlabel("Kondisi Cuaca")
    plt.ylabel("Jumlah Sewa")
    st.pyplot(plt)

# Informasi tambahan
st.sidebar.header("Informasi Kolom")
st.sidebar.write("""
- **instant**: record index
- **dteday**: date
- **season**: season (1:spring, 2:summer, 3:fall, 4:winter)
- **yr**: year (0: 2011, 1: 2012)
- **mnth**: month (1 to 12)
- **hr**: hour (0 to 23, hanya ada di hour.csv)
- **holiday**: apakah hari tersebut adalah hari libur
- **weekday**: hari dalam seminggu
- **workingday**: jika hari tersebut bukan akhir pekan dan bukan hari libur
- **weathersit**: kondisi cuaca
- **temp**: suhu normal dalam Celsius
- **atemp**: suhu terasa dalam Celsius
- **hum**: kelembapan
- **windspeed**: kecepatan angin
- **casual**: jumlah pengguna biasa
- **registered**: jumlah pengguna terdaftar
- **cnt**: total sewa sepeda
""")

# Jalankan aplikasi
if __name__ == "__main__":
    st.write("Aplikasi ini menampilkan analisis data sewa sepeda dari dataset hour.csv dan day.csv.")
