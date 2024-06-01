import os
import dent.settings as settings
import pandas as pd
import requests
import json

def xls_handler(fs):
    filename = f"out_{fs.split('/')[-1].split('.')[0]}.json"
    xls = pd.read_excel(f"{settings.BASE_DIR}{fs}") # use r before absolute file path 
    out = {}
    values = xls[xls.columns[1]].values
    for value in values:
        if str(value)!="nan":
            print(value)
            url = f'http://127.0.0.1:8000/search/{value}'
            try:
                r = requests.get(url)
                out[value] = r.json()
            except:
                pass
    try:
        os.mkdir(os.path.join(settings.MEDIA_ROOT, "data"))
    except:
        pass

    full_filename = os.path.join(settings.MEDIA_ROOT, "data", filename)
    with open(full_filename, 'w+', encoding='utf8') as out_json:
        json.dump(out, out_json, indent=4, ensure_ascii=False)
    
    return filename.split("out_data_")[-1].split(".json")[0]
