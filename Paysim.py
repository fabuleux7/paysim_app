import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# Konfigurasi Halaman
# =============================
st.set_page_config(
    page_title="Dashboard Analisis Fraud Transaksi",
    layout="wide"
)

# =============================
# SIDEBAR (MENU NAVIGASI)
# =============================
st.sidebar.title("📁 Menu Analisis")
menu = st.sidebar.radio(
    "Pilih Menu:",
    [
        "Dashboard Awal",
        "Distribusi Jenis Transaksi",
        "Jumlah Fraud vs Non-Fraud",
        "Fraud Berdasarkan Step",
        "Fraud Berdasarkan Jenis Transaksi",
        "Pola Transaksi Mencurigakan"
    ]
)

# =============================
# MENU 1 – DASHBOARD AWAL
# =============================
if menu == "Dashboard Awal":
    st.title("📊 Dashboard Analisis Fraud Transaksi Keuangan")
    st.write("Menampilkan dataset transaksi sebelum dilakukan analisis Hadoop MapReduce.")

    uploaded_file = st.file_uploader(
        "Upload dataset transaksi (CSV)",
        type=["csv"]
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(
                uploaded_file,
                sep=";",
                engine="python",
                on_bad_lines="skip"
            )

            st.success("Dataset berhasil dimuat")

            st.subheader("📌 Informasi Dataset")
            col1, col2 = st.columns(2)
            col1.metric("Jumlah Baris", df.shape[0])
            col2.metric("Jumlah Kolom", df.shape[1])

            st.subheader("📄 Preview Data")
            st.dataframe(df.head(50), use_container_width=True)

        except Exception as e:
            st.error("Gagal membaca file CSV")
            st.exception(e)

    else:
        st.info("Silakan upload file CSV untuk melihat data.")



# =============================
# MENU 2 – DISTRIBUSI JENIS TRANSAKSI
# =============================
elif menu == "Distribusi Jenis Transaksi":
    st.title("📈 Distribusi Jenis Transaksi dalam Dataset")

    uploaded_txt = st.file_uploader(
        "Upload file hasil MapReduce Distribusi Jenis Transaksi (.txt)",
        type=["txt"]
    )

    if uploaded_txt is not None:
        try:
            df = pd.read_csv(
                uploaded_txt,
                sep="\t",
                header=None,
                names=["Jenis Transaksi", "Jumlah"]
            )

            st.success("Data hasil MapReduce berhasil dimuat")

            st.subheader("📄 Data Hasil MapReduce")
            st.dataframe(df, use_container_width=True)

            st.subheader("📊 Visualisasi Jumlah Transaksi")

            # Bar Chart (Streamlit native)
            st.bar_chart(df.set_index("Jenis Transaksi"))

        except Exception as e:
            st.error("Gagal membaca file TXT")
            st.exception(e)

    else:
        st.info("Silakan upload file TXT hasil MapReduce.")


# =============================
# MENU 3 – JUMLAH FRAUD VS NON-FRAUD
# =============================
elif menu == "Jumlah Fraud vs Non-Fraud":
    st.title("🚨 Jumlah Fraud vs Non-Fraud dalam Dataset")

    uploaded_txt = st.file_uploader(
        "Upload file hasil MapReduce (Fraud vs Non-Fraud) (.txt)",
        type=["txt"]
    )

    if uploaded_txt is not None:
        try:
            # Baca file hasil MapReduce
            df = pd.read_csv(
                uploaded_txt,
                sep="\t",
                header=None,
                names=["Label", "Jumlah"]
            )

            # Pastikan tipe data
            df["Label"] = pd.to_numeric(df["Label"], errors="coerce")
            df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce")

            # Mapping label
            df["Kategori"] = df["Label"].map({
                0: "Non-Fraud",
                1: "Fraud"
            })

            st.success("Data fraud berhasil dimuat")

            # =====================
            # METRIC RINGKAS
            # =====================
            col1, col2 = st.columns(2)

            non_fraud = int(df.loc[df["Kategori"] == "Non-Fraud", "Jumlah"].sum())
            fraud = int(df.loc[df["Kategori"] == "Fraud", "Jumlah"].sum())

            col1.metric("Total Non-Fraud", non_fraud)
            col2.metric("Total Fraud", fraud)

            # =====================
            # TABEL DATA
            # =====================
            st.subheader("📄 Data Hasil MapReduce")
            st.dataframe(df[["Kategori", "Jumlah"]], use_container_width=True)

            # =====================
            # VISUALISASI
            # =====================
            st.subheader("📊 Visualisasi Perbandingan Fraud")
            st.write("**Pie Chart – Proporsi Fraud vs Non-Fraud**")

            # Pusatkan pie chart
            col_left, col_center, col_right = st.columns([1, 2, 1])
            with col_center:
                fig_pie, ax_pie = plt.subplots(figsize=(4, 4), dpi=100)
                ax_pie.pie(
                    df["Jumlah"],
                    labels=df["Kategori"],
                    autopct="%1.2f%%",
                    startangle=90
                )
                ax_pie.set_title("Proporsi Fraud vs Non-Fraud")
                ax_pie.axis("equal")

                st.pyplot(fig_pie, use_container_width=False)

        except Exception as e:
            st.error("Gagal membaca file TXT")
            st.exception(e)
    else:
        st.info("Silakan upload file TXT hasil MapReduce.")


# =============================
# MENU 4 – FRAUD BERDASARKAN STEP
# =============================
elif menu == "Fraud Berdasarkan Step":
    st.title("⏱️ Jumlah Fraud Berdasarkan Step (Jam)")

    uploaded_txt = st.file_uploader(
        "Upload file hasil MapReduce (Fraud Berdasarkan Step) (.txt)",
        type=["txt"]
    )

    if uploaded_txt is not None:
        try:
            # Baca file hasil MapReduce
            df = pd.read_csv(
                uploaded_txt,
                sep="\t",
                header=None,
                names=["Step", "Jumlah Fraud"]
            )

            # Pastikan tipe data benar
            df["Step"] = pd.to_numeric(df["Step"], errors="coerce")
            df["Jumlah Fraud"] = pd.to_numeric(df["Jumlah Fraud"], errors="coerce")

            # Buang baris invalid
            df = df.dropna()

            # Urutkan berdasarkan step
            df = df.sort_values("Step")

            st.success("Data fraud per step berhasil dimuat")

            # =====================
            # TABEL DATA
            # =====================
            st.subheader("📄 Data Jumlah Fraud per Step")
            st.dataframe(df, use_container_width=True)

            # =====================
            # VISUALISASI LINE CHART
            # =====================
            st.subheader("📈 Pola Fraud Berdasarkan Waktu (Step)")

            fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
            ax.plot(
                df["Step"],
                df["Jumlah Fraud"],
                marker="o",
                linestyle="-"
            )
            ax.set_xlabel("Step (Jam)")
            ax.set_ylabel("Jumlah Fraud")
            ax.set_title("Jumlah Fraud Berdasarkan Step")

            st.pyplot(fig, use_container_width=False)

            # =====================
            # INSIGHT SINGKAT
            # =====================
            max_step = df.loc[df["Jumlah Fraud"].idxmax()]

            st.info(
                f"📌 Fraud tertinggi terjadi pada step {int(max_step['Step'])} "
                f"dengan jumlah {int(max_step['Jumlah Fraud'])} fraud."
            )

        except Exception as e:
            st.error("Gagal membaca file TXT")
            st.exception(e)

    else:
        st.info("Silakan upload file TXT hasil MapReduce.")



# =============================
# MENU 5 – FRAUD BERDASARKAN JENIS TRANSAKSI
# =============================
elif menu == "Fraud Berdasarkan Jenis Transaksi":
    st.title("📌 Kategori Transaksi dengan Fraud Terbanyak")

    uploaded_txt = st.file_uploader(
        "Upload file hasil MapReduce (Fraud Berdasarkan Jenis Transaksi) (.txt)",
        type=["txt"]
    )

    if uploaded_txt is not None:
        try:
            # Baca file hasil MapReduce
            df = pd.read_csv(
                uploaded_txt,
                sep="\t",
                header=None,
                names=["Jenis Transaksi", "Jumlah Fraud"]
            )

            # Pastikan tipe data benar
            df["Jumlah Fraud"] = pd.to_numeric(df["Jumlah Fraud"], errors="coerce")
            df = df.dropna()

            # Urutkan dari fraud terbanyak (untuk visualisasi horizontal)
            df_sorted = df.sort_values("Jumlah Fraud", ascending=True)

            st.success("Data fraud berdasarkan jenis transaksi berhasil dimuat")

            # =====================
            # TABEL DATA
            # =====================
            st.subheader("📄 Data Hasil MapReduce")
            st.dataframe(
                df.sort_values("Jumlah Fraud", ascending=False),
                use_container_width=True
            )

            # =====================
            # VISUALISASI
            # =====================
            st.subheader("📊 Visualisasi Fraud per Jenis Transaksi")

            fig, ax = plt.subplots(figsize=(5, 2.5), dpi=100)
            ax.barh(
                df_sorted["Jenis Transaksi"],
                df_sorted["Jumlah Fraud"],
                color="#F44336"
            )

            ax.set_xlabel("Jumlah Fraud")
            ax.set_ylabel("Jenis Transaksi")
            ax.set_title("Jumlah Fraud Berdasarkan Jenis Transaksi")

            st.pyplot(fig, use_container_width=False)

            # =====================
            # INSIGHT OTOMATIS
            # =====================
            top = df.sort_values("Jumlah Fraud", ascending=False).iloc[0]

            st.info(
                f"📌 Transaksi dengan fraud terbanyak adalah **{top['Jenis Transaksi']}** "
                f"dengan jumlah **{int(top['Jumlah Fraud'])}** kasus."
            )

        except Exception as e:
            st.error("Gagal membaca file TXT")
            st.exception(e)
    else:
        st.info("Silakan upload file TXT hasil MapReduce.")


# =============================
# MENU 6 – POLA TRANSAKSI MENCURIGAKAN
# =============================
elif menu == "Pola Transaksi Mencurigakan":

    st.header("🚨 Pola Transaksi Fraud Paling Mencurigakan")

    # =============================
    # BAGIAN 1 – TABEL POLA TRANSAKSI FRAUD
    # =============================
    st.subheader("📄 Detail Transaksi Fraud Antar Akun")

    uploaded_pola = st.file_uploader(
        "Upload file TXT: Pola Transaksi Fraud Paling Mencurigakan",
        type=["txt"],
        key="pola_fraud"
    )

    if uploaded_pola is not None:
        try:
            df_pola = pd.read_csv(
                uploaded_pola,
                sep="\t",
                header=None,
                names=["Pola Transaksi", "Jumlah"]
            )

            st.dataframe(df_pola, use_container_width=True)

            st.caption(
                "Menampilkan pasangan pengirim → penerima yang terindikasi fraud"
            )

        except Exception as e:
            st.error("❌ Gagal membaca file Pola Transaksi Fraud")
            st.exception(e)
    else:
        st.info("Silakan upload file Pola Transaksi Fraud Paling Mencurigakan.")

    # =============================
    # BAGIAN 2 – VISUALISASI TRANSAKSI FRAUD BERULANG
    # =============================
    st.subheader("📊 Transaksi Fraud Paling Sering Berulang")

    uploaded_repeat = st.file_uploader(
        "Upload file TXT: Repeated Transactions",
        type=["txt"],
        key="repeated_fraud"
    )

    if uploaded_repeat is not None:
        try:
            df_repeat = pd.read_csv(
                uploaded_repeat,
                sep="\\|",
                skiprows=2,
                header=None,
                names=["Pola Transaksi", "Jumlah Transaksi"],
                engine="python"
            )

            df_repeat["Pola Transaksi"] = df_repeat["Pola Transaksi"].str.strip()
            df_repeat["Jumlah Transaksi"] = pd.to_numeric(
                df_repeat["Jumlah Transaksi"],
                errors="coerce"
            )

            df_repeat = df_repeat.dropna()

            # Ambil Top 10 paling mencurigakan
            top_repeat = df_repeat.sort_values(
                by="Jumlah Transaksi",
                ascending=False
            ).head(10)

            st.write("**Top Pola Transaksi Fraud Paling Sering Terjadi**")

            st.bar_chart(
                top_repeat.set_index("Pola Transaksi")["Jumlah Transaksi"]
            )

        except Exception as e:
            st.error("❌ Gagal membaca file Repeated Transactions")
            st.exception(e)
    else:
        st.info("Silakan upload file Repeated Transactions.")

