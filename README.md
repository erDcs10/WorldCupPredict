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
| 1 | Negara manakah yang paling banyak memenangkan trofi piala dunia? lalu berapa jumlah trofi yang diperoleh? | ... | Negara yang paling banyak memenangkan trofi adalah Brazil dan memiliki 5 trofi | ... |
| 2 | Berapa total poin FIFA yang dimiliki oleh tim nasional Brazil? | ... | Total poin FIFA yang dimiliki oleh tim nasional Brazil sebanyak 1761.16093 | ... |
| 3 | Berapa jumlah total stadion yang akan digunakan oleh Amerika Serikat untuk turnamen ini? | ... | Amerika Serikat menyediakan fasilitas stadion dengan total 11 stadion | ... |
| 4 | Berapakah rata-rata gol yang dicetak oleh tim nasional Swedia dalam 5 pertandingan terakhir?  | ... | Rata-rata gol yang dicetak oleh tim nasional Swedia sebanyak 6 gol | ... |
| 5 | Kapan turnamen Piala Dunia FIFA 2026 akan diselenggarakan dan negara mana saja yang menjadi tuan rumahnya? | ... | Diselenggarakan pada tanggal 11 Juni 2026 hingga 19 Juni 2026 , tuan rumah piala dunia 2026 adalah Amerika Serikat, Kanada, dan Meksiko | ... |
| 6 | Apa alasan dari tim nasional Eritrea memilih untuk mengundurkan diri dari babak kualifikasi piala dunia 2026?| ... | Eritrea mundur dari babak kualifikasi karena kekhawatiran bahwa para pemain mereka akan mencari suaka politik jika diizinkan bepergian ke luar negeri| ... |
| 7 | Siapakah pemain top argentina?| ... | Lionel Messi dengan rating : 8.314285 | ... |
| 8 | Siapakah pemain dengan rating tertinggi pada pertandingan piala dunia 2026? | ... | Diogo Dalot dengan rating : 9.3| ... |
| 9 | Berapakah nilai pasar dari tim nasional Jerman?| ... | Nilai pasar dari tim nasional Jerman diperkirakan mencapai Rp 13.444,70 Miliar| ... |
| 10 | Tim nasional manakah yang mengalami kebobolan sebanyak 14 gol dalam 5 pertandingan terakhir? | ... | Tim nasional yang mengalami kebobolan 14 gol adalah tim nasional Curacao | ... |

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
