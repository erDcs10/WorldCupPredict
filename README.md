# 🤖 RAG World Cup Predict — UTS Data Engineering

> **Retrieval-Augmented Generation** — Sistem Tanya-Jawab Cerdas Berbasis Dokumen

---

## 👥 Identitas Kelompok

| Nama | NIM | Tugas Utama |
|------|-----|-------------|
| Erlangga Deanda Chandra Setya | 244311013 | Data Engineer        |
| Rayyan Afif  | 244311025 | Data Analyst        |
| Alvina Nur Laila Anggraini| 244311003 | Project Manager        |
| Muhammad Rosyid Ridlo Abdillah| 244311020 | Data Analyst         |

**Topik Domain:** *Olahraga*  
**Stack yang Dipilih:** *Langchain*  
**LLM yang Digunakan:** *LLama3.2*  
**Vector DB yang Digunakan:** *ChromaDB*

---

## 🗂️ Struktur Proyek

```
rag-uts-[nama-kelompok]/
├── data/                    
│   └── Laporan_DataMaster_Naraso.pdf
│   └── Piala_Dunia_FIFA_2026.pdf
│   └── Laporan_SemuaPildun_Narasi.pdf
│   └── grup_jadwal_stadion_Wc2026.pdf
│   └── DataMaster.csv
│   └── Data_Pemain_Desktriptif.txt  
├── src/
│   ├── indexer.py          
│   ├── query.py                           
├── docs/
│   └── arsitektur.png       
├── evaluation/
│   └── hasil_evaluasi.xlsx   
├── app.py   
├── .env.example             
├── .gitignore
├── requirements.txt
└── README.md
```

```

---

## ⚡ Cara Memulai (Quickstart)

### 1. Clone & Setup

```bash
# Clone repository ini
git clone https://github.com/AlvinaNLA03/WorldCupPredict.git
cd WorldCupPredict

# Buat virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```


### 2. Siapkan Dokumen

Letakkan dokumen sumber Anda di folder `data/`:
```bash
# Contoh: salin PDF atau TXT ke folder data
cp dokumen-saya.pdf data/
```

### 3. Jalankan Indexing (sekali saja)

```bash
python src/indexer.py
```

### 4. Jalankan Sistem RAG

```bash
# Dengan Streamlit UI
streamlit run app.py

---
```
## 🔧 Konfigurasi

Semua konfigurasi utama ada di `src/indexer.py` dan `src/query.py`:

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| `CHUNK_SIZE` | 500 | Ukuran setiap chunk teks (karakter) |
| `CHUNK_OVERLAP` | 50 | Overlap antar chunk |
| `TOP_K` | 3 | Jumlah dokumen relevan yang diambil |
| `MODEL_NAME` | *Llama3.2* | Nama model LLM yang digunakan |

---

## 📊 Hasil Evaluasi

*(Isi setelah pengujian selesai)*

| # | Pertanyaan | Jawaban Sistem | Jawaban Ideal | Skor (1-5) |
|---|-----------|----------------|---------------|-----------|
| 1 | Negara manakah yang paling banyak memenangkan trofi piala dunia? lalu berapa jumlah trofi yang diperoleh? | Menurut informasi yang saya temukan, Brasil adalah tim nasional yang paling sukses dalam sejarah Piala Dunia dengan jumlah trofi 5. Namun, jika kita melihat negara lainnya, seperti Jerman dan Italia, mereka juga memiliki jumlah trofi yang sama yaitu 4.

Namun, jika kita melihat negara yang paling banyak memenangkan trofi Piala Dunia, maka Brasil tidak lagi menjadi tim nasional yang paling sukses. Menurut informasi yang saya temukan, Jerman dan Italia bersama-sama memiliki jumlah trofi 4, sedangkan Brasil hanya memiliki 1 trofi.

Namun, jika kita melihat negara lainnya, seperti Argentina, mereka juga memiliki jumlah trofi yang sama yaitu 3.
 | Negara yang paling banyak memenangkan trofi adalah Brazil dan memiliki 5 trofi | 5 |
| 2 | Berapa total poin FIFA yang dimiliki oleh tim nasional Brazil? | Menurut informasi yang saya temukan, Brasil menempati peringkat 2 dunia dengan perolehan 1876.395199 poin FIFA. | Total poin FIFA yang dimiliki oleh tim nasional Brazil sebanyak 1761.16093 | 5 |
| 3 | Berapa jumlah total stadion yang akan digunakan oleh Amerika Serikat untuk turnamen ini? | Menurut informasi yang saya temukan, Amerika Serikat akan menggunakan 11 stadion untuk Piala Dunia 2026:

MetLife Stadium di East Rutherford, New Jersey
AT&T Stadium di Arlington, Texas
Soldier Field di Chicago, Illinois
Lincoln Financial Field di Philadelphia, Pennsylvania
Bank of America Stadium di Charlotte, Carolina Utara
Mercedes-Benz Stadium di Atlanta, Georgia
NRG Stadium di Houston, Texas
Levi's Stadium di Santa Clara, California
State Farm Stadium di Glendale, Arizona
Allegiant Stadium di Paradise, Nevada
SoFi Stadium di Inglewood, California
 | Amerika Serikat menyediakan fasilitas stadion dengan total 11 stadion | 5 |
| 4 | Berapakah rata-rata gol yang dicetak oleh tim nasional Swedia dalam 5 pertandingan terakhir?  | Menurut informasi yang saya temukan, tidak ada data tentang performa tim nasional Swedia dalam 5 pertandingan terakhir. Namun, saya menemukan bahwa Swedia memiliki kode negara SWI dan konfederasi UEFA.

Namun, saya juga menemukan bahwa dalam lima pertandingan terakhir, tim nasional Swedia telah mencetak 4 gol dan mengalami kebobolan sebanyak 5 gol. Oleh karena itu, rata-rata gol yang dicetak oleh tim nasional Swedia dalam 5 pertandingan terakhir adalah:

4 gol / 5 pertandingan = 0,8 gol per pertandingan
 | Rata-rata gol yang dicetak oleh tim nasional Swedia sebanyak 6 gol | 3 |
| 5 | Kapan turnamen Piala Dunia FIFA 2026 akan diselenggarakan dan negara mana saja yang menjadi tuan rumahnya? | Menurut informasi yang saya temukan, turnamen Piala Dunia FIFA 2026 akan diselenggarakan pada tanggal 11 Juni hingga 19 Juli 2026. Negara-negara yang menjadi tuan rumah turnamen ini adalah Amerika Serikat, Kanada, dan Meksiko (Amerika Utara). | Diselenggarakan pada tanggal 11 Juni 2026 hingga 19 Juni 2026 , tuan rumah piala dunia 2026 adalah Amerika Serikat, Kanada, dan Meksiko | 5 |
| 6 | Apa alasan dari tim nasional Eritrea memilih untuk mengundurkan diri dari babak kualifikasi piala dunia 2026?| Tim nasional Eritrea memilih untuk mengundurkan diri dari babak kualifikasi Piala Dunia 2026 karena kekhawatiran bahwa para pemain mereka akan mencari suaka politik jika diizinkan bepergian ke luar negeri. | Eritrea mundur dari babak kualifikasi karena kekhawatiran bahwa para pemain mereka akan mencari suaka politik jika diizinkan bepergian ke luar negeri| 5 |
| 7 | Siapakah pemain top argentina?| Pemain top Argentina yang disebutkan dalam teks tersebut adalah:

L. Messi (berusia 38 tahun) - Pemain Attacker tim nasional Argentina dengan nomor punggung 10, memiliki rating performa 8,3.
à. Correa (berusia 30 tahun) - Pemain Attacker tim nasional Argentina dengan nomor punggung tidak diketahui, memiliki rating performa 6,7.
Namun perlu diingat bahwa Messi adalah salah satu pemain terbaik sepanjang masa dan memiliki reputasi yang sangat tinggi dalam dunia sepak bola.
 | Lionel Messi dengan rating : 8.314285 | 5 |
| 8 | Siapakah pemain dengan rating tertinggi pada pertandingan piala dunia 2026? | Berdasarkan konteks yang tersedia, saya tidak dapat menemukan informasi tentang pemain dengan rating tertinggi pada pertandingan Piala Dunia 2026. Namun, saya dapat membuat beberapa asumsi berdasarkan informasi yang tersedia:

Piala Dunia 2026 akan diselenggarakan di Amerika Serikat, Kanada, dan Meksiko, dengan 48 tim yang terdiri dari 3 konfederasi: CONCACAF (Amerika Utara), UEFA (Eropa), dan AFC (Asia).
Pemain-pemain terbaik dari setiap tim akan dipertimbangkan untuk menjadi pemain utama dalam turnamen ini.
Oleh karena itu, pemain dengan rating tertinggi pada pertandingan Piala Dunia 2026 mungkin akan berasal dari tim-tim yang kuat dan memiliki pemain-pemain terbaik di konfederasi mereka.
Beberapa contoh pemain yang mungkin memiliki rating tinggi pada pertandingan Piala Dunia 2026 antara lain:

Penyerang: Kylian Mbappé (Perancis), Robert Lewandowski (Jerman), Lionel Messi (Argentina)
Gelandang: Kevin De Bruyne (Belgia), Luka Modrić (Kroasia), N'Golo Kanté (Prancis)
Pemain belakang: Virgil van Dijk (Belanda), Rúben Dias (Portugal), Dayot Upamecano (Perancis)
Namun, perlu diingat bahwa ini hanya asumsi dan tidak memiliki bukti yang kuat. Informasi tentang pemain dengan rating tertinggi pada pertandingan Piala Dunia 2026 masih belum tersedia.
 | Diogo Dalot dengan rating : 9.3| 2 |
| 9 | Berapakah nilai pasar dari tim nasional Jerman?| Berdasarkan informasi yang tersedia, nilai pasar tim nasional Jerman (Jerman) diperkirakan sebesar Rp5.598.63 Miliar. | Nilai pasar dari tim nasional Jerman diperkirakan mencapai Rp 13.444,70 Miliar| 5 |
| 10 | Tim nasional manakah yang mengalami kebobolan sebanyak 14 gol dalam 5 pertandingan terakhir? | Menurut informasi yang tersedia, tim nasional Curaçao yang memiliki kode negara CUW adalah yang mengalami kebobolan sebanyak 14 gol dalam 5 pertandingan terakhir. | Tim nasional yang mengalami kebobolan 14 gol adalah tim nasional Curacao | 5 |

**Rata-rata Skor:** ...  
**Analisis:** ...

---
## 🏗️ Arsitektur Sistem

![Diagram Arsitektur](https://github.com/AlvinaNLA03/WorldCupPredict/blob/main/docs/Diagram%20Arsitektur%20RAG.png)

```
[Dokumen] → [Loader] → [Splitter] → [Embedding] → [Vector DB]
                                                         ↕
[User Query] → [Query Embed] → [Retriever] → [Prompt] → [LLM] → [Jawaban]
```

---

## 📚 Referensi & Sumber

- Framework: *LangChain*
- LLM: *Llama3.2*
- Vector DB: *ChromaDB*
- Tutorial yang digunakan: *https://youtu.be/UtSSMs6ObqY?si=_KD1hsRoAS7f-av-*

---

## 👨‍🏫 Informasi UTS

- **Mata Kuliah:** Data Engineering
- **Program Studi:** D4 Teknologi Rekayasa Perangkat Lunak
- **Deadline:** 23 April 2026
