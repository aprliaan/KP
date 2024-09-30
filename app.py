from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

def read_data():
    return pd.read_csv('data.csv', encoding='ISO-8859-1')

@app.route('/')
def home():
    df = read_data()
    missing_data_count = df.isna().sum()
    cost_center_counts = df['Cost Center'].value_counts()
    perusahaan_counts = df['Perusahaan'].value_counts()
    job_title_counts = df['Job Title'].value_counts()
    nama_requester_counts = df['Nama Requester'].value_counts()
    fungsi_counts = df['Fungsi'].value_counts().head()
    
    # Convert hasil ke dictionary untuk ditampilkan di HTML
    context = {
        'missing_data_count': missing_data_count.to_dict(),
        'cost_center_counts': cost_center_counts.to_dict(),
        'perusahaan_counts': perusahaan_counts.to_dict(),
        'job_title_counts': job_title_counts.to_dict(),
        'nama_requester_counts': nama_requester_counts.to_dict(),
        'fungsi_counts': fungsi_counts.to_dict()
    }
    
    return render_template('home.html', **context)

@app.route('/perbedaan_fungsi_department')
def perbedaan_fungsi_department():
    df = read_data()
    df['Fungsi'] = df['Fungsi'].str.strip().str.lower()
    df['Department'] = df['Department'].str.strip().str.lower()
    df['cek fungsi departmen'] = df['Fungsi'] == df['Department']
    df['cek fungsi departemen'] = np.where(df['Fungsi'].notna() & df['Department'].notna(), df['Fungsi'] == df['Department'], 'False')
    cek_1 = pd.DataFrame([df['REQ Number'], df['Fungsi'], df['Department'], df['cek fungsi departemen']]).transpose()

    cek_1

    return render_template('perbedaan_fungsi_department.html', output=cek_1.to_dict(orient='records'))

@app.route('/perbedaan_nama_requester_customer')
def perbedaan_nama_requester_customer():
    df = read_data()
    df['Nama Requester'] = df['Nama Requester'].str.strip().str.lower()
    df['Customer'] = df['Customer'].str.strip().str.lower()
    df['cek Requester Customer'] = df['Nama Requester'] == df['Customer']
    df['cek Requester Customer'] = np.where(df['Nama Requester'].notna() & df['Customer'].notna(), df['Nama Requester'] == df['Customer'], 'False')
    cek_2 = pd.DataFrame([df['REQ Number'], df['Nama Requester'], df['Customer'], df['cek Requester Customer']]).transpose()

    cek_2

    return render_template('perbedaan_nama_requester_customer.html', output=cek_2.to_dict(orient='records'))

@app.route('/perbedaan_perusahaan_requestor_company')
def perbedaan_perusahaan_requestor_company():
    df = read_data()
    df['Perusahaan'] = df['Perusahaan'].str.strip().str.lower()
    df['Requestor Company'] = df['Requestor Company'].str.strip().str.lower()
    df['cek perusahaan company'] = df['Perusahaan'] == df['Requestor Company']
    cek_3 = pd.DataFrame([df['REQ Number'], df['Perusahaan'], df['Requestor Company'], df['cek perusahaan company']]).transpose()

    cek_3

    return render_template('perbedaan_perusahaan_requestor_company.html', output=cek_3.to_dict(orient='records'))

@app.route('/perbedaan_site')
def perbedaan_site():
    df = read_data()
    df['site'] = df['site'].str.strip().str.lower()
    df['Site'] = df['Site'].str.strip().str.lower()
    df['cek site'] = df['site'] == df['Site']
    df['cek site'] = np.where(df['site'].notna() & df['Site'].notna(), df['site'] == df['Site'], 'False')
    cek_4 = pd.DataFrame([df['REQ Number'], df['site'], df['Site'], df['cek site']]).transpose()

    cek_4

    return render_template('perbedaan_site.html', output=cek_4.to_dict(orient='records'))

@app.route('/perbedaan_site_group')
def perbedaan_site_group():
    df = read_data()
    df['site Group'] = df['site Group'].str.strip().str.lower()
    df['Site Group'] = df['Site Group'].str.strip().str.lower()
    df['cek site group'] = df['Site Group'] == df['Site Group']
    df['cek site group'] = np.where(df['site Group'].notna() & df['site Group'].notna(), df['site Group'] == df['Site Group'], 'False')
    cek_5 = pd.DataFrame([df['REQ Number'], df['site Group'], df['Site Group'], df['cek site group']]).transpose()

    cek_5
    return render_template('perbedaan_site_group.html', output=cek_5.to_dict(orient='records'))

@app.route('/grafik_persentase')
def grafik_persentase():
    df = read_data()
    
    # Grafik jumlah data kosong di setiap kolom
    missing_data_count = df.isna().sum()
    plt.figure(figsize=(12, 8))
    missing_data_count.plot(kind='bar', color='skyblue')
    plt.title('Jumlah Data Kosong di Setiap Kolom', fontsize=16)
    plt.xlabel('Kolom', fontsize=14)
    plt.ylabel('Jumlah Kosong', fontsize=14)
    plt.tight_layout()
    missing_data_plot_path = 'static/missing_data_plot.png'
    plt.savefig(missing_data_plot_path, dpi=300)
    plt.close()
    
    # Grafik distribusi Job Title
    job_title_counts = df['Job Title'].value_counts()
    plt.figure(figsize=(12, 8))
    job_title_counts.plot(kind='bar', color='skyblue')
    plt.title('Distribusi Job Title', fontsize=16)
    plt.xlabel('Job Title', fontsize=14)
    plt.ylabel('Jumlah', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    job_title_plot_path = 'static/job_title_plot.png'
    plt.savefig(job_title_plot_path, dpi=300)
    plt.close()
    
    # Grafik distribusi Perusahaan
    perusahaan_counts = df['Perusahaan'].value_counts()
    plt.figure(figsize=(12, 8))
    perusahaan_counts.plot(kind='bar', color='skyblue')
    plt.title('Distribusi Perusahaan', fontsize=16)
    plt.xlabel('Perusahaan', fontsize=14)
    plt.ylabel('Jumlah', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    perusahaan_plot_path = 'static/perusahaan_plot.png'
    plt.savefig(perusahaan_plot_path, dpi=300)
    plt.close()
    
    # Grafik distribusi Cost Center
    cost_center_counts = df['Cost Center'].value_counts()
    plt.figure(figsize=(12, 8))
    cost_center_counts.plot(kind='bar', color='skyblue')
    plt.title('Distribusi Cost Center', fontsize=16)
    plt.xlabel('Cost Center', fontsize=14)
    plt.ylabel('Jumlah', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    cost_center_plot_path = 'static/cost_center_plot.png'
    plt.savefig(cost_center_plot_path, dpi=300)
    plt.close()

    # Grafik persentase Fungsi
    fungsi = df['Fungsi'].value_counts()
    persentase_per_jenis = fungsi / len(df) * 100
    labels = persentase_per_jenis.index
    sizes = persentase_per_jenis.values
    colors = plt.cm.tab10.colors

    plt.figure(figsize=(12, 8))
    plt.barh(labels, sizes, color=colors)
    plt.title('Persentase Jumlah Data per Fungsi', fontsize=16)
    plt.xlabel('Persentase (%)', fontsize=14)
    plt.ylabel('Fungsi', fontsize=14)
    plt.tight_layout()
    fungsi_plot_path = 'static/fungsi_plot.png'
    plt.savefig(fungsi_plot_path, dpi=300)
    plt.close()

    return render_template('grafik_persentase.html', 
                           missing_data_plot='missing_data_plot.png',
                           job_title_plot='job_title_plot.png',
                           perusahaan_plot='perusahaan_plot.png',
                           cost_center_plot='cost_center_plot.png',
                           fungsi_plot='fungsi_plot.png')

if __name__ == '__main__':
    app.run(debug=True)
