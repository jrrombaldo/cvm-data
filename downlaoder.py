from pathlib import Path
from datetime import date
from dateutil.relativedelta import relativedelta
from multiprocessing.pool import ThreadPool
import wget
from os import unlink, listdir
from os.path import join, exists

results_path = Path('results')
results_path.mkdir(parents=True, exist_ok=True)

files_to_download = []
since_year = 2005


def download_files(file_url):
    to_download = join(results_path, file_url.rsplit("/")[-1])
    if exists(to_download): unlink(to_download)
    print (f'downloading {file_url}')
    return wget.download(file_url, str(results_path.absolute()), bar=None)


# os.unlink(join(results_path, 'cad_fi.csv'))
# os.unlink(join(results_path, date.today().strftime("inf_diario_fi_%Y%m.csv")))


files_to_download.append('http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv')


# if the results directory is empty, download everything, otherwise, lets download last month
if len(listdir(results_path)) < 2:
    for f in [(date.today() - relativedelta(months=delta)).strftime("%Y%m") for delta in range (0, 18)]:
        files_to_download.append(f'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{f}.zip')
        
    for hf in [delta for delta in range (since_year, date.today().year-1)]:
        files_to_download.append(f'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/HIST/inf_diario_fi_{hf}.zip')
else:
    files_to_download.append(f'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{date.today().strftime("%Y%m")}.zip')


pool_output = ThreadPool(25).map(download_files, files_to_download)
print(pool_output)
