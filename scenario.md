Parameter,Input yang Direkomendasikan,Alasan
Grade,1 (A) atau 2 (B),Memastikan kualitas kredit terbaik.
Bunga,0.06 - 0.08 (Sangat Rendah),"Mengikuti kriteria ""Suku Bunga Terbaik""."
Nilai Pinjaman,"$10,000 (Kecil-Menengah)",Sesuai dengan deskripsi klaster.
Tenor,36 bulan,Tenor standar.
Nilai Cicilan,$300,Cicilan yang wajar.


Parameter,Input yang Direkomendasikan,Alasan
Grade,3 (C),Kualitas standar/menengah.
Bunga,0.12 - 0.14 (Bunga Menengah),Menghindari status risiko tinggi (0.17+).
Nilai Pinjaman,"$28,000 - $30,000 (Terbesar)",Memastikan masuk ke segmen High Value.
Tenor,60 bulan,Tenor panjang.
Nilai Cicilan,$650,Cicilan tinggi karena nilai pinjaman besar.


Parameter,Input yang Direkomendasikan,Alasan
Grade,4 (D),Menunjukkan kualitas kredit menurun.
Bunga,0.17 - 0.19 (Tinggi),"Sesuai kriteria ""Suku Bunga Tinggi""."
Nilai Pinjaman,"$7,000","Pinjaman kecil (tidak terlalu menarik), tetapi berisiko."
Tenor,36 bulan,Tenor standar.
Nilai Cicilan,$250,Cicilan yang wajar.


Parameter,Input yang Direkomendasikan,Alasan
Grade,6 (F) atau 7 (G),Kualitas kredit terburuk.
Bunga,0.25 - 0.35 (Sangat Tinggi),Menunjukkan risiko maksimum dan biaya pinjaman yang mahal.
Nilai Pinjaman,"$12,000",Pinjaman menengah.
Tenor,60 bulan,Tenor panjang.
Nilai Cicilan,$450,Cicilan tinggi karena bunga yang mencekik.


Target Klaster,Grade,Bunga,Nilai Pinjaman
0 (The Best),A/B (1-2),0.06,"$10,000"
4 (Better),B (2),0.08,"$22,000"
2 (Monitor Besar),C (3),0.14,"$30,000"
3 (Medium Risk),D (4),0.18,"$7,000"
1 (High Risk/NPL),G (7),0.30,"$12,000"