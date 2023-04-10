import os
import csv
from natsort import natsorted
import pandas as pd


defects4j_dir = os.path.expanduser('~/defects4j')
project_ids = ['Chart', 'Cli', 'Closure', 'Codec', 'Collections', 'Compress', 'Csv', 'Gson', 'JacksonCore',
               'JacksonDatabind', 'JacksonXml', 'Jsoup', 'JxPath', 'Lang', 'Math', 'Mockito', 'Time']

def list_files_in_folder(folder_path):
    l = []
    files = os.listdir(folder_path)
    for file in natsorted(files):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            l.append(file_path)
    return l


def statistical_warnings_type(work_folder):
    files = [] # 835 in total
    for pid in project_ids:
        folder_path = os.path.join(work_folder, f'{pid}')
        files.extend(list_files_in_folder(folder_path))
        csv_dir = os.path.join(defects4j_dir, f'csv/{pid}')
        os.makedirs(csv_dir, exist_ok=True)

    df_res = pd.DataFrame() # warnings_type_summary.csv
    for file in files:
        print(f'Processing {file}')
        dfs = pd.read_html(file)
        # save all tables to csv, just for test
        # s = file[42:-20] 
        # for i, df in enumerate(dfs):
        #     df.to_csv(f'{defects4j_dir}/csv/{s}{i}.csv', index=False, quoting=csv.QUOTE_ALL)
        #     print(f'Generating {defects4j_dir}/csv/{s}{i}.csv')
        df0 = dfs[0]
        total_warnings_density = df0[df0['Metric'] == 'Total Warnings']['Density*'].values[0]   
        data_dict = dfs[1].groupby('Warning Type').agg({'Number': 'sum'}).reset_index().set_index('Warning Type').to_dict()['Number']
        df1 = pd.DataFrame.from_dict(data_dict, orient='index').T
        df1.index = [file[42:-21]]
        df1['Density*'] = total_warnings_density
        df_res = pd.concat([df_res, df1], ignore_index=False)
        
    cols = sorted(col for col in sorted(df_res.columns.tolist()) if col != 'Density*')
    cols.append('Density*')
    df_res = df_res[cols].fillna(0)
    df_res = df_res.astype({col: int for col in cols if col != 'Density*'})
    df_res.iloc[0, 0] = 'Programs/bug_id'
    df_res.to_csv(f'{defects4j_dir}/csv/spotbugs_warnings_type_summary.csv', index=True)
        


if __name__ == '__main__':
    work_folder = f'{defects4j_dir}/spotbugs-html-reports'
    statistical_warnings_type(work_folder)