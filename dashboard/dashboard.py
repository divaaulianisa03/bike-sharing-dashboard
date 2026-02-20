import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load data
main_data = pd.read_csv("main_data.csv")
main_data['dteday'] = pd.to_datetime(main_data['dteday'])

day_df  = main_data[main_data['source'] == 'day'].copy()
hour_df = main_data[main_data['source'] == 'hour'].copy()

# Sidebar filter
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

with st.sidebar:
    st.header("Filter Data")

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataframe berdasarkan rentang tanggal
day_filtered  = day_df[(day_df['dteday'] >= str(start_date)) &
                       (day_df['dteday'] <= str(end_date))]
hour_filtered = hour_df[(hour_df['dteday'] >= str(start_date)) &
                        (hour_df['dteday'] <= str(end_date))]

# Header
st.header('Bike Sharing Dashboard 🚴')
st.markdown("---")

# ── Visualisasi 1: Tren Peminjaman per Tahun ──────────────────────
st.subheader('Tren Peminjaman Sepeda per Tahun')

yearly_trend = day_filtered.groupby('yr')['cnt'].sum().reset_index()
yearly_trend['yr'] = yearly_trend['yr'].replace({0: 2011, 1: 2012})

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(yearly_trend['yr'], yearly_trend['cnt'],
              color=['#90CAF9', '#1565C0'], width=0.4)
ax.set_title('Tren Peminjaman Sepeda per Tahun (2011 vs 2012)', fontsize=16)
ax.set_xlabel('Tahun')
ax.set_ylabel('Total Peminjaman')
ax.set_xticks([2011, 2012])

for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30000,
            f'{bar.get_height():,.0f}', ha='center', va='bottom',
            fontsize=12, fontweight='bold')

plt.tight_layout()
st.pyplot(fig)

st.markdown("---")

# ── Visualisasi 2: Rata-rata Peminjaman per Jam (Hari Kerja) ──────
st.subheader('Rata-rata Peminjaman Sepeda per Jam pada Hari Kerja')

workday_hour   = hour_filtered[hour_filtered['workingday'] == 1]
hourly_workday = workday_hour.groupby('hr')['cnt'].mean().reset_index()
hourly_workday.columns = ['jam', 'rata_rata_peminjaman']

if not hourly_workday.empty:
    peak_idx = hourly_workday['rata_rata_peminjaman'].idxmax()
    low_idx  = hourly_workday['rata_rata_peminjaman'].idxmin()

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(hourly_workday['jam'], hourly_workday['rata_rata_peminjaman'],
            marker='o', linewidth=2, color='#1565C0')

    ax.scatter(hourly_workday.loc[peak_idx, 'jam'],
               hourly_workday.loc[peak_idx, 'rata_rata_peminjaman'],
               color='red', s=120, zorder=5,
               label=f'Tersibuk: Jam {int(hourly_workday.loc[peak_idx, "jam"])}')
    ax.scatter(hourly_workday.loc[low_idx, 'jam'],
               hourly_workday.loc[low_idx, 'rata_rata_peminjaman'],
               color='orange', s=120, zorder=5,
               label=f'Tersepi: Jam {int(hourly_workday.loc[low_idx, "jam"])}')

    ax.set_title('Rata-rata Peminjaman Sepeda per Jam pada Hari Kerja (2011–2012)', fontsize=14)
    ax.set_xlabel('Jam')
    ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_xticks(range(0, 24))
    ax.legend()

    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("Data tidak tersedia untuk filter yang dipilih.")

st.markdown("---")
st.caption('Diva CDC-03 Copyright (c) 2026')
