# 📊 SkillMatch Analytics - Data Science Dashboard

[![Open App](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?logo=streamlit&logoColor=white)](https://skillmatch-analytics-dashboard-fzgnpr7jt9sudgiekbpsq4.streamlit.app/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Repository ini berisi analisis data lowongan pekerjaan (*Exploratory Data Analysis* - EDA) dan dashboard interaktif yang dibangun menggunakan **Streamlit** dan **Plotly** untuk mendukung pengembangan sistem rekomendasi karir berbasis kompetensi pada proyek **SkillMatch** (CC26-PRU431).

Dashboard ini dirancang untuk memetakan kebutuhan industri terkait keterampilan kerja (*skills*), yang kemudian digunakan oleh tim AI Engineer dan Backend sebagai landasan dasar model pencocokan kecocokan kerja (*Skill Match Score*).

---

## 📂 Struktur Folder

```text
Skillmatch/
│
├── .gitignore                   # Mengabaikan file temporary, venv, dan cache lokal
├── README.md                    # Dokumentasi utama proyek (file ini)
├── requirements.txt             # Daftar dependensi library Python
│
├── app.py                       # Kode utama dashboard interaktif Streamlit
├── googleColab_skillmatch.ipynb # Jupyter Notebook tahap preprocessing & analisis EDA awal
└── skillmatch_train_data.csv    # Dataset lowongan pekerjaan (preprocessed)
```

---

## 🛠️ Fitur Dashboard

Dashboard Streamlit ini memiliki 4 halaman utama:
1.  **Executive Overview:** Ringkasan metrik utama (KPI Cards) dari dataset, dilengkapi dengan *Interactive Data Explorer* untuk menyaring baris data berdasarkan pencarian teks dan multi-kategori skill, serta fitur untuk mengunduh dataset hasil filter ke format CSV.
2.  **Univariate Analysis:** Visualisasi distribusi frekuensi dari nama-nama posisi pekerjaan teratas, kategori skill paling populer, serta proporsi jumlah skill yang tercantum per lowongan (Donut Chart).
3.  **Bivariate Analysis:** Menampilkan **Job-Skill Co-occurrence Heatmap** interaktif yang menunjukkan persentase seberapa sering suatu skill disyaratkan untuk posisi pekerjaan tertentu. Dilengkapi juga dengan *Cross-Explorer* untuk mencari breakdown skill berdasarkan pekerjaan atau sebaliknya.
4.  **Data Insights:** Rangkuman temuan bisnis/teknis utama dari dataset dalam bentuk naratif (*storytelling*) menggunakan visual callout box modern.

---

## ⚡ Persyaratan Sistem & Instalasi

Pastikan Anda telah menginstal Python versi **3.8 atau yang lebih baru** di komputer Anda.

### Langkah-langkah Menjalankan secara Lokal:

1.  **Clone / Unduh Folder Project**
    Buka terminal (Command Prompt / PowerShell / Git Bash) dan pastikan Anda berada di direktori project ini:
    ```bash
    cd Skillmatch
    ```

2.  **Buat Virtual Environment (Sangat Disarankan)**
    Membuat lingkungan virtual terpisah agar tidak mengganggu library global komputer:
    *   **Windows:**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    *   **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instal Dependensi**
    Instal semua pustaka (library) Python yang dibutuhkan:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi Streamlit**
    Jalankan perintah berikut untuk membuka dashboard di browser Anda:
    ```bash
    streamlit run app.py
    ```
    Aplikasi akan otomatis terbuka pada peramban default Anda di alamat lokal `http://localhost:8501`.

---

## 🔬 Jupyter Notebook (Preprocessing & EDA)

Jika Anda ingin melihat tahapan data preprocessing, data cleaning, pemetaan kode skill, hingga visualisasi dasar menggunakan Matplotlib dan Seaborn, buka file [googleColab_skillmatch.ipynb](file:///C:/Users/DELL/Downloads/Dicoding/Capstone/New%20folder/SkillMatch%20-%20CC26-PRU431/Skillmatch/googleColab_skillmatch.ipynb):
*   Anda bisa menjalankannya secara lokal dengan mengetikkan perintah `jupyter notebook` atau `jupyter lab` di terminal setelah virtual environment aktif.
*   Alternatifnya, Anda dapat mengunggah file notebook `.ipynb` dan dataset `skillmatch_train_data.csv` ke [Google Colab](https://colab.research.google.com/).
