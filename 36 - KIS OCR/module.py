import pandas as pd
import time


def extract_data(data):
    extract_data.nomor_kartu = data[4]
    extract_data.nama = data[6]
    extract_data.alamat = data[8:9]
    extract_data.tanggal_lahir = data[11]
    extract_data.nik = data[13]
    extract_data.faskes = data[15]
    print('--- Informasi ---')
    print(extract_data.nomor_kartu, extract_data.nama, extract_data.alamat,
          extract_data.tanggal_lahir, extract_data.nik, extract_data.faskes)
    return extract_data.nomor_kartu, extract_data.nama, extract_data.alamat, extract_data.tanggal_lahir, extract_data.nik, extract_data.faskes


def download_excel():
    df = pd.DataFrame({
        'Nomor Kartu': extract_data.nomor_kartu,
        'Nama': extract_data.nama,
        'Alamat': extract_data.alamat,
        'Tanggal Lahir': extract_data.tanggal_lahir,
        'NIK': extract_data.nik,
        'Faskes': extract_data.faskes})
    timestr = time.strftime("%Y%m%d-%H%M%S")
    download_excel.filename_excel = df.to_excel('static/'+timestr+'.xlsx', index=False)
    download_excel.filename_excel = 'static/'+timestr+'.xlsx'
    print('Excel berhasil diunduh')
    return download_excel.filename_excel
