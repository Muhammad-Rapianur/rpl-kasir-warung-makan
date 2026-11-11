# Dokumentasi Spesifikasi Kebutuhan Perangkat Lunak (SRS)
## Sistem Kasir Warung Makan (KasirWarung)

Folder ini berisi dokumen spesifikasi kebutuhan perangkat lunak resmi (*Software Requirements Specification* - SRS) untuk proyek tugas mata kuliah **Rekayasa Perangkat Lunak (RPL)**.

---

## 📄 Berkas Utama
- **[`srs.md`](srs.md)** : Dokumen SRS Ringkas lengkap yang memuat 7 bagian standar:
  1. **Pendahuluan:** Tujuan, ruang lingkup, dan definisi istilah POS warung makan.
  2. **Gambaran Umum:** Profil pengguna (Kasir & Pemilik), lingkungan operasi fisik (*offline-first*), batasan, dan asumsi.
  3. **Kebutuhan Fungsional (KF):** 13 butir kebutuhan berformat *"Sistem harus ..."*, terukur, bebas dari istilah teknologi, dan diprioritaskan dengan MoSCoW (Must: 61.5%).
  4. **Kebutuhan Non-Fungsional (KNF):** 6 butir kebutuhan terukur dengan metrik kuantitatif (Kinerja, Keandalan, Kegunaan, Keamanan).
  5. **Di Luar Lingkup (*Won't Have*):** Batasan fitur fiktif/rumit yang sengaja tidak dibuat (anti-overengineering).
  6. **Matriks Keterlacakan (*Traceability Matrix*):** Pemetaan dari *User Story* ke *KF/KNF* dan rencana pengujian (*Test Cases*).
  7. **Riwayat Konfirmasi Klien:** Catatan validasi kebutuhan langsung dengan pelaku UMKM warung makan.

---

## 🎯 Peran SRS dalam Proyek Ini
1. **Kontrak Resmi Sistem:** Menjadi acuan sah mengenai apa saja yang wajib dibangun oleh tim pengembang dan apa yang tidak dikerjakan.
2. **Cetak Biru Pengujian:** Menjadi rujukan utama pembuatan skenario uji kelayakan (*test cases*) pada tahap akhir pengembangan.
3. **Konteks Dasar PRD & UML:** Menjadi landasan penyusunan *Product Requirements Document* ([`PRD.md`](../../PRD.md)) dan diagram perancangan UML ([`docs/uml/`](../uml/)).
