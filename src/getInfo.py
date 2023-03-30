import os
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor

defects4j_dir = os.path.expanduser('~/defects4j')
project_ids = ['Chart', 'Cli', 'Closure', 'Codec', 'Collections', 'Compress', 'Csv', 'Gson', 'JacksonCore',
               'JacksonDatabind', 'JacksonXml', 'Jsoup', 'JxPath', 'Lang', 'Math', 'Mockito', 'Time']


def project_info(pid, save=False):
    """ Get information for a specific project """
    query = f'defects4j info -p {pid}'
    if save:
        log_dir = os.path.join(defects4j_dir, f'logs/{pid}')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'{pid}-Info.log')
        with open(log_file, 'w') as f:
            process = subprocess.Popen(query, shell=True, cwd=defects4j_dir, stdout=f, stderr=subprocess.STDOUT)
            process.wait()
    else:
        process = subprocess.Popen(query, shell=True, cwd=defects4j_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        with process.stdout:
            output = process.stdout.read().decode()
            return pid, output
        process.wait()


def log_all_projects_info():
    """ Log information about all projects """
    with ThreadPoolExecutor() as executor:
        executor.map(project_info, project_ids, [True] * len(project_ids))

def show_all_projects_info():
    """ Just show information about all projects """
    with ThreadPoolExecutor() as executor:
        executor.map(project_info, project_ids)
        results = executor.map(project_info, project_ids)
        for res in results:
            print(f'{res[0]}, {res[1]}')
    

if __name__ == '__main__':
    # show_all_projects_info()
    log_all_projects_info()
