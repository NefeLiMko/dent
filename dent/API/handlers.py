import os
import dent.settings as settings
import pandas as pd
import requests
import json
from parsers.models import ProductModel
def xls_handler(fs):
    filename = f"out_{fs.split('/')[-1].split('.')[0]}.json"
    
    xls = pd.read_excel(f"{settings.BASE_DIR}{fs}") # use r before absolute file path 
    out = {}
    values = xls[xls.columns[1]].values
    for value in values:
        if str(value)!="nan":
            try:
                for element in ProductModel.objects.filter(articul=value):
                    if value in out.keys():
                        out[value].append({"title":element.name, "price": element.price, "site":element.site, "date":str(element.date)})
                    else:
                        out[value] = [{"articul":element.articul,"title":element.name, "price": element.price, "site":element.site, "date":str(element.date)}]
                    print(out[value])
            except:
                pass
    try:
        os.mkdir(os.path.join(settings.MEDIA_ROOT, "data"))
    except:
        pass

    full_filename = os.path.join(settings.MEDIA_ROOT, "data", filename)
    with open(full_filename, 'w+', encoding='utf8') as out_json:
        json.dump(out, out_json, indent=4, ensure_ascii=False)
    print(f"{settings.BASE_DIR}{fs}")
    return filename.split("out_data_")[-1].split(".json")[0]
