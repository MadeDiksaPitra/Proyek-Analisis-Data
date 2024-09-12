import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math

# Streamlit layout
st.set_page_config(layout="centered")

st.markdown("### Made Diksa Pitra")

# Heading utama
st.title("Analisis Penggunaan Sepeda dan Pengaruh Cuaca")
st.markdown("### Analisis data dari dataset 'hour.csv' dan 'day.csv'")

# Gathering Data
st.header("Dataset")

# Gathering data CSV files dari folder Data (hour.csv and day.csv)
hour_data = pd.read_csv('./hour.csv')
day_data = pd.read_csv('./day.csv')

# Menampilkan 5 baris pertama untuk kedua dataset
st.subheader("Dataset hour.csv")
st.write(hour_data.head(5))

st.subheader("Dataset day.csv")
st.write(day_data.head(5))

# EDA (Exploratory Data Analysis)
st.header("Exploratory Data Analysis (EDA)")

# Atur style untuk Seaborn plots
sns.set(style="whitegrid")

# Histogram untuk Data Hour
st.subheader("Histograms for Hourly Data")
fig, ax = plt.subplots(figsize=(15, 12))
plt.suptitle('Histograms for Hourly Data', fontsize=16)

num_columns_hour = hour_data.select_dtypes(include=['float64', 'int64']).columns
num_plots_hour = len(num_columns_hour)
rows_hour = math.ceil(num_plots_hour / 4)

for i, column in enumerate(num_columns_hour, 1):
    plt.subplot(rows_hour, 4, i)
    sns.histplot(hour_data[column], bins=30, kde=False, color='skyblue')
    plt.title(f'Distribution of {column}', fontsize=12)
    plt.xlabel(column)
    plt.ylabel('Frequency')

plt.tight_layout(rect=[0, 0, 1, 0.96])
st.pyplot(fig)

# Histogram untuk Data Day
st.subheader("Histograms for Daily Data")
fig, ax = plt.subplots(figsize=(12, 10))
plt.suptitle('Histograms for Daily Data', fontsize=16)

num_columns_day = day_data.select_dtypes(include=['float64', 'int64']).columns
num_plots_day = len(num_columns_day)
rows_day = math.ceil(num_plots_day / 3)

for i, column in enumerate(num_columns_day, 1):
    plt.subplot(rows_day, 3, i)
    sns.histplot(day_data[column], bins=20, kde=False, color='lightcoral')
    plt.title(f'Distribution of {column}', fontsize=12)
    plt.xlabel(column)
    plt.ylabel('Frequency')

plt.tight_layout(rect=[0, 0, 1, 0.96])
st.pyplot(fig)

# Visualization & Explanatory Analysis
st.header("Visualization & Explanatory Analysis")

# Line chart untuk membandingkan hari kerja dan akhir pekan
st.subheader("Penyewaan Sepeda: Hari Kerja dibanding Akhir Pekan")
grouped_hour_data = hour_data.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))

weekday_data = grouped_hour_data[grouped_hour_data['workingday'] == 1]
plt.plot(weekday_data['hr'], weekday_data['cnt'], label='Weekday (Hari Kerja)', color='b', linewidth=2)

weekend_data = grouped_hour_data[grouped_hour_data['workingday'] == 0]
plt.plot(weekend_data['hr'], weekend_data['cnt'], label='Weekend (Akhir Pekan)', color='g', linewidth=2)

plt.title('Penyewaan Sepeda: Hari Kerja dibanding Akhir Pekan', fontsize=16)
plt.xlabel('Jam', fontsize=12)
plt.ylabel('Rata-rata Penyewaan Sepeda', fontsize=12)
plt.legend(title='Tipe Hari', loc='upper left')
plt.grid(True)
plt.xticks(range(0, 24, 1))
st.pyplot(fig)

# Stacked Bar Chart untuk pengaruh cuaca
st.subheader("Pengaruh Cuaca terhadap Penggunaan Sepeda")
grouped_data = hour_data.groupby(['hr', 'weathersit'])['cnt'].sum().unstack()

fig, ax = plt.subplots(figsize=(12, 8))
grouped_data.plot(kind='bar', stacked=True, ax=ax, color=['skyblue', 'lightcoral', 'yellowgreen', 'orange'])

plt.title('Distribusi Penyewaan Sepeda Berdasarkan Jam dan Kondisi Cuaca', fontsize=16)
plt.xlabel('Jam', fontsize=12)
plt.ylabel('Total Rentals', fontsize=12)
weather_labels = ["Clear", "Mist", "Light Snow", "Heavy Rain"]
plt.legend(title='Kondisi Cuaca', labels=weather_labels, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(fig)

# Analisis Lanjutan
st.header("Advanced Analysis")

# Pivot table untuk analisis lanjutan
st.subheader("Analisis Pengaruh Cuaca terhadap Penyewaan Sepeda")
pivot_table = hour_data.pivot_table(values='cnt', index='season', columns='weathersit', aggfunc='mean')
st.write("**Pivot Table (Rata-rata Penyewaan Sepeda berdasarkan Musim dan Kondisi Cuaca)**")
st.dataframe(pivot_table)

# Heatmap untuk visualisasi pivot table
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", fmt=".1f", linewidths=.5)
plt.title('Average Bike Rentals by Season and Weather Condition', fontsize=14)
plt.xlabel('Weather Condition')
plt.ylabel('Season')
plt.xticks([0.5, 1.5, 2.5, 3.5], ["1: Clear/Few clouds", "2: Mist/Cloudy", "3: Light Rain/Snow", "4: Heavy Rain/Snow"], rotation=45)
plt.yticks([0.5, 1.5, 2.5, 3.5], ["1: Spring", "2: Summer", "3: Fall", "4: Winter"])
st.pyplot(fig)

# Kesimpulan
st.header("Conclusion")

st.subheader("1. Kapan waktu puncak penggunaan sepeda terjadi pada hari kerja dibandingkan dengan akhir pekan?")
st.write("""
Waktu puncak penggunaan sepeda pada hari kerja cenderung terjadi dua kali sehari, yaitu pada pagi hari sekitar pukul 8 dan sore hari sekitar pukul 17-18. Ini mencerminkan pola perjalanan terkait aktivitas bekerja, di mana pengguna menggunakan sepeda untuk perjalanan pergi dan pulang kerja.
Pada akhir pekan, waktu puncak penggunaan sepeda lebih tersebar, dengan peningkatan stabil sepanjang hari, terutama dari siang hingga sore (pukul 11.00 hingga 17.00). Ini menunjukkan bahwa pengguna lebih sering menggunakan sepeda untuk aktivitas rekreasi atau bersantai, yang tidak terikat dengan jam kerja.
Kesimpulan: Penggunaan sepeda pada hari kerja mengikuti pola aktivitas yang lebih terstruktur terkait jam kerja, sementara pada akhir pekan, penggunaan sepeda lebih merata sepanjang hari, dengan waktu puncak terjadi pada siang hingga sore hari.
""")

st.subheader("2. Bagaimana pengaruh cuaca terhadap jumlah penggunaan sepeda?")
st.write("""
Cuaca yang cerah atau sedikit berawan (kategori 1) menunjukkan tingkat penggunaan sepeda yang lebih tinggi baik oleh pengguna. Pengguna lebih sensitif terhadap cuaca dibandingkan jumlah penyewaan yang jauh lebih rendah pada cuaca buruk.
Cuaca mendung atau berkabut (kategori 2), penggunaan sepeda oleh pengguna menurun, namun tetap stabil.
Cuaca hujan ringan, salju ringan (kategori 3), terlihat penurunan signifikan dalam penggunaan sepeda oleh kedua kategori pengguna, namun beberapa pengguna cenderung masih menyewa meskipun dalam cuaca buruk.
Cuaca ekstrem seperti hujan deras atau badai salju (kategori 4), hampir tidak ada penggunaan sepeda baik oleh pengguna kasual maupun terdaftar.
Kesimpulan: Cuaca memiliki pengaruh yang signifikan terhadap jumlah penggunaan sepeda, terutama oleh pengguna yang cenderung lebih memilih kondisi cuaca cerah. Pengguna terdaftar tetap menggunakan sepeda meskipun dalam cuaca kurang ideal, namun pada kondisi cuaca yang ekstrem, penggunaan sepeda menurun drastis.
""")
