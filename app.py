import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="SkillMatch Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern Tableau-like look
st.markdown("""
<style>
    [data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA & DICTIONARY
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv("skillmatch_train_data.csv")
    # Pastikan num_skills terhitung dengan benar
    df["num_skills"] = df["skill_abr"].fillna("").str.split(",").apply(lambda x: len([s for s in x if s.strip()]))
    return df

df = load_data()

skill_mapping = {
    'ACCT': 'Accounting', 'ADM': 'Administration', 'ADVR': 'Advertising', 
    'ANLS': 'Analysis', 'ART': 'Art & Creative', 'BD': 'Business Development', 
    'CNSL': 'Consulting', 'CUST': 'Customer Service', 'DIST': 'Distribution', 
    'DSGN': 'Design', 'EDU': 'Education', 'ENG': 'Engineering', 'FIN': 'Finance', 
    'GENB': 'General Business', 'HCPR': 'Healthcare Provider', 'HR': 'Human Resources', 
    'IT': 'Information Technology', 'LGL': 'Legal', 'MGMT': 'Management', 
    'MNFC': 'Manufacturing', 'MRKT': 'Marketing', 'OTHR': 'Other', 
    'PR': 'Public Relations', 'PRCH': 'Purchasing', 'PRDM': 'Product Management', 
    'PRJM': 'Project Management', 'PROD': 'Production', 'QA': 'Quality Assurance', 
    'RSCH': 'Research', 'SALE': 'Sales', 'SCI': 'Science', 'STRA': 'Strategy', 
    'SUPL': 'Supply Chain', 'TRNG': 'Training', 'WRT': 'Writing'
}
reverse_mapping = {v:k for k,v in skill_mapping.items()}

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
st.sidebar.title("📊 SkillMatch Analytics")
st.sidebar.markdown("Visualisasi interaktif Exploratory Data Analysis (EDA)")

page = st.sidebar.radio(
    "Navigasi Halaman:",
    [
        "1. Executive Overview",
        "2. Univariate Analysis",
        "3. Bivariate Analysis",
        "4. Data Insights"
    ]
)

# =====================================================
# PAGE 1: EXECUTIVE OVERVIEW
# =====================================================
if page == "1. Executive Overview":
    st.title("📊 Executive Overview")
    st.markdown("Ringkasan dataset lowongan pekerjaan untuk analisis SkillMatch.")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Lowongan", f"{len(df):,}")
    
    unique_skills = df["skill_abr"].dropna().str.split(",").explode().str.strip().nunique()
    col2.metric("Kategori Skill Unik", unique_skills)
    
    avg_skills = round(df["num_skills"].mean(), 2)
    col3.metric("Rata-rata Skill / Lowongan", avg_skills)
    
    unique_jobs = df["title_cleaned"].nunique()
    col4.metric("Posisi Pekerjaan Unik", f"{unique_jobs:,}")

    st.markdown("---")
    
    # Interactive Data Explorer
    st.subheader("🔍 Interactive Data Explorer")
    st.markdown("Gunakan filter di bawah ini untuk mencari data secara spesifik. Secara **default, filter tidak aktif** (menampilkan seluruh data).")
    
    c1, c2 = st.columns(2)
    with c1:
        search_job = st.text_input("Cari Posisi Pekerjaan (kosongkan untuk menampilkan semua):", value="")
    with c2:
        selected_skills = st.multiselect("Filter Kategori Skill (kosongkan untuk menampilkan semua):", options=sorted(list(skill_mapping.values())))

    # Filtering Logic
    filtered_df = df.copy()
    if search_job.strip() != "":
        filtered_df = filtered_df[filtered_df["title_cleaned"].str.contains(search_job, case=False, na=False)]
    
    if selected_skills:
        selected_codes = [reverse_mapping[s] for s in selected_skills]
        # Pastikan baris memiliki SEMUA skill yang dipilih (AND condition) atau SALAH SATU (OR). Kita gunakan OR untuk kemudahan eksplorasi.
        pattern = '|'.join(selected_codes)
        filtered_df = filtered_df[filtered_df["skill_abr"].fillna("").str.contains(pattern)]

    st.markdown(f"**Menampilkan {len(filtered_df):,} baris data.**")
    st.dataframe(filtered_df.head(100), use_container_width=True) # Limit to 100 for performance on UI

    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='skillmatch_filtered_data.csv',
        mime='text/csv',
    )


# =====================================================
# PAGE 2: UNIVARIATE ANALYSIS
# =====================================================
elif page == "2. Univariate Analysis":
    st.title("📈 Univariate Analysis (Distribusi)")
    st.markdown("Eksplorasi distribusi kolom utama dalam dataset: Posisi Pekerjaan, Kategori Skill, dan Jumlah Kebutuhan Skill.")

    tab1, tab2, tab3 = st.tabs(["Distribusi Pekerjaan", "Distribusi Skill", "Jumlah Skill per Lowongan"])
    
    with tab1:
        st.subheader("Top Posisi Pekerjaan")
        top_job = st.slider("Tampilkan Top N Posisi:", min_value=5, max_value=50, value=15, step=5)
        job_counts = df["title_cleaned"].value_counts().head(top_job).reset_index()
        job_counts.columns = ["Job Title", "Frequency"]
        
        fig_job = px.bar(
            job_counts, x="Frequency", y="Job Title", 
            orientation='h', 
            title=f"Top {top_job} Posisi Pekerjaan Paling Sering Muncul",
            color="Frequency", color_continuous_scale="Blues"
        )
        fig_job.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_job, use_container_width=True)

    with tab2:
        st.subheader("Top Kategori Skill")
        top_skill = st.slider("Tampilkan Top N Kategori Skill:", min_value=5, max_value=35, value=15, step=5)
        
        skills_exploded = df["skill_abr"].dropna().str.split(",").explode().str.strip()
        skill_counts = skills_exploded.value_counts().head(top_skill).reset_index()
        skill_counts.columns = ["Skill Code", "Frequency"]
        skill_counts["Skill Name"] = skill_counts["Skill Code"].map(skill_mapping)
        
        fig_skill = px.bar(
            skill_counts, x="Frequency", y="Skill Name", 
            orientation='h', 
            title=f"Top {top_skill} Kategori Skill Paling Banyak Dibutuhkan",
            color="Frequency", color_continuous_scale="Purples"
        )
        fig_skill.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_skill, use_container_width=True)

    with tab3:
        st.subheader("Distribusi Jumlah Kategori Skill per Lowongan")
        # Distribusi num_skills
        num_skills_dist = df["num_skills"].value_counts().reset_index()
        num_skills_dist.columns = ["Jumlah Skill", "Total Lowongan"]
        num_skills_dist["Jumlah Skill"] = num_skills_dist["Jumlah Skill"].astype(str) + " Skill"
        
        fig_pie = px.pie(
            num_skills_dist, values="Total Lowongan", names="Jumlah Skill", 
            title="Berapa Banyak Skill yang Diminta dalam 1 Lowongan?",
            hole=0.4, # Donut chart
            color_discrete_sequence=px.colors.sequential.Teal
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        st.info("💡 **Insight (Pertanyaan Bisnis 4):** Sebagian besar lowongan hanya menuntut 1 hingga 2 kategori skill utama (rata-rata 1.75).")


# =====================================================
# PAGE 3: BIVARIATE ANALYSIS
# =====================================================
elif page == "3. Bivariate Analysis":
    st.title("🔄 Bivariate Analysis (Hubungan Job & Skill)")
    st.markdown("Menganalisis korelasi dan keterkaitan antara Posisi Pekerjaan dan Kategori Keterampilan yang dibutuhkan.")

    st.subheader("🔥 Job-Skill Co-occurrence Heatmap")
    st.markdown("Heatmap ini menunjukkan persentase kemunculan sebuah skill pada posisi pekerjaan tertentu. (Menjawab Pertanyaan Bisnis 3)")
    
    col_hm1, col_hm2 = st.columns(2)
    with col_hm1:
        n_top_jobs = st.slider("Jumlah Top Pekerjaan (Y-Axis):", 5, 30, 15)
    with col_hm2:
        n_top_skills = st.slider("Jumlah Top Skill (X-Axis):", 5, 20, 10)
        
    # Get top jobs and skills
    top_jobs_list = df["title_cleaned"].value_counts().head(n_top_jobs).index.tolist()
    top_skills_codes = df["skill_abr"].dropna().str.split(",").explode().str.strip().value_counts().head(n_top_skills).index.tolist()
    
    # Filter dataframe to only include top jobs
    df_hm = df[df["title_cleaned"].isin(top_jobs_list)].copy()
    
    # Create matrix for percentage and hover text
    columns_mapped = [skill_mapping.get(c, c) for c in top_skills_codes]
    heatmap_data = pd.DataFrame(index=top_jobs_list, columns=columns_mapped).fillna(0.0)
    heatmap_hover = pd.DataFrame(index=top_jobs_list, columns=columns_mapped).fillna("")

    for job in top_jobs_list:
        job_subset = df_hm[df_hm["title_cleaned"] == job]
        total_postings = len(job_subset)
        if total_postings == 0:
            continue
            
        skill_lists = job_subset["skill_abr"].dropna().str.split(",")
        exploded_skills = skill_lists.explode().str.strip()
        
        for code in top_skills_codes:
            # Hitung persentase dan jumlah asli
            count = (exploded_skills == code).sum()
            percentage = (count / total_postings) * 100
            
            skill_name = skill_mapping.get(code, code)
            heatmap_data.loc[job, skill_name] = round(percentage, 1)
            heatmap_hover.loc[job, skill_name] = f"{int(count)} lowongan (dari total {int(total_postings)})"
            
    fig_heatmap = px.imshow(
        heatmap_data, 
        labels=dict(x="Kategori Skill", y="Posisi Pekerjaan", color="% Kebutuhan"),
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale=[[0, '#1e293b'], [0.5, '#1e3a8a'], [1, '#3b82f6']], # Dark Slate to Blue
        aspect="auto",
        title="Persentase Kebutuhan Skill per Posisi Pekerjaan (%)",
        text_auto=".1f"
    )
    fig_heatmap.update_traces(
        customdata=heatmap_hover.values,
        hovertemplate="<b>Pekerjaan:</b> %{y}<br><b>Skill:</b> %{x}<br><b>Persentase:</b> %{z:.1f}%<br><b>Jumlah Asli:</b> %{customdata}<extra></extra>"
    )
    fig_heatmap.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("---")
    st.subheader("🎯 Cross-Explorer: Job vs Skill")
    st.markdown("Pilih dari dropdown di bawah ini (default: tidak ada yang dipilih) untuk melihat breakdown spesifik.")
    
    ce_col1, ce_col2 = st.columns(2)
    with ce_col1:
        explore_job = st.selectbox("Pilih Pekerjaan (Lihat Skill-nya):", ["-- Pilih Pekerjaan --"] + sorted(df["title_cleaned"].dropna().unique().tolist()))
        if explore_job != "-- Pilih Pekerjaan --":
            subset_job = df[df["title_cleaned"] == explore_job]
            job_skills = subset_job["skill_abr"].dropna().str.split(",").explode().str.strip().value_counts().reset_index()
            job_skills.columns = ["Code", "Count"]
            job_skills["Skill"] = job_skills["Code"].map(skill_mapping).fillna(job_skills["Code"])
            fig_pie_job = px.pie(job_skills, values='Count', names='Skill', title=f"Komposisi Skill untuk {explore_job}", hole=0.3)
            st.plotly_chart(fig_pie_job, use_container_width=True)
            
    with ce_col2:
        explore_skill = st.selectbox("Pilih Skill (Lihat Pekerjaannya):", ["-- Pilih Skill --"] + sorted(list(skill_mapping.values())))
        if explore_skill != "-- Pilih Skill --":
            skill_code = reverse_mapping[explore_skill]
            subset_skill = df[df["skill_abr"].fillna("").str.contains(skill_code)]
            top_jobs_for_skill = subset_skill["title_cleaned"].value_counts().head(10).reset_index()
            top_jobs_for_skill.columns = ["Job Title", "Count"]
            fig_bar_skill = px.bar(top_jobs_for_skill, x="Count", y="Job Title", orientation='h', title=f"Top 10 Pekerjaan Membutuhkan {explore_skill}", color="Count", color_continuous_scale="Reds")
            fig_bar_skill.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_bar_skill, use_container_width=True)


# =====================================================
# PAGE 4: DATA INSIGHTS
# =====================================================
elif page == "4. Data Insights":
    st.title("📌 Executive Report & Data Insights")
    st.markdown("Berikut adalah rangkuman dari analisis dataset lowongan pekerjaan.")

    st.success("Berdasarkan dataset, **Information Technology**, **Management**, dan **Sales** adalah 3 pilar kompetensi utama yang mendominasi permintaan pasar.")

    c1, c2 = st.columns(2)
    
    with c1:
        st.info("### 1️⃣ Skill Paling Banyak Dicari\nKategori **Information Technology** memiliki frekuensi tertinggi (2.673 kemunculan), menjadikannya kompetensi paling krusial di era digital saat ini.")
        
        st.warning("### 3️⃣ Hubungan Job-Skill\nSetiap posisi pekerjaan memiliki pola kompetensi yang spesifik. Pekerjaan tidak menuntut skill secara acak, melainkan berkelompok (contoh: *Software Engineer* mutlak dengan *IT & Engineering*). Ini adalah dasar kuat untuk fitur **Skill Gap Analysis**.")
        
    with c2:
        st.info("### 2️⃣ Posisi Dominan\nPosisi **Project Manager**, **Administrative Assistant**, dan para akuntan mendominasi volume pencarian tenaga kerja dalam dataset ini.")
        
        st.warning("### 4️⃣ Jumlah Skill per Lowongan\nMayoritas lowongan (lebih dari 85%) hanya mensyaratkan **1 hingga 2 kategori skill utama**. Hal ini membuktikan bahwa spesialisasi lebih ditekankan daripada penguasaan terlalu banyak bidang general.")

    st.markdown("---")
    st.markdown("### Kesimpulan Teknis untuk Pengembangan SkillMatch")
    st.markdown("> *Data ini telah tervalidasi dan siap digunakan oleh tim AI Engineer dan Backend untuk membangun sistem rekomendasi karir (Skill Match Score) berdasarkan matriks relasi Job-Skill yang telah ditemukan dalam tahap EDA ini.*")