import os
import pandas as pd
import glob
import json

def get_files(filepath):
        all_files = []
        for root,dirs,files in os.walk(filepath):
            files = glob.glob(os.path.join(root,'*.json'))
            for f in files:
                all_files.append(os.path.abspath(f))
        return all_files


path_to_json = r'C:\Users\Strike\Desktop\python\tutorial\scientists'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

# here I define my pandas Dataframe with the columns I want to get from the json
jsons_data = pd.DataFrame(columns=['name', 'awards', 'education_text'])
# we need both the json and an index number so use enumerate()
for index, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        json_text = json.load(json_file)
        # here you need to know the layout of your json and each json has to have
        # the same structure (obviously not the structure I have here)

        name = int(json_text['name']) 
        awards = json_text['awards']
        education_text = json_text['education_text']
        # here I push a list of data into a pandas DataFrame at row given by 'index'
        
        jsons_data.loc[index] = [name, awards, education_text]

# now that we have the pertinent json data in our DataFrame let's look at it
print(jsons_data)
jsons_data.to_csv (r'C:\Users\Strike\Desktop\python\data\data.csv', index = None,header=False)
# scientists = get_files(r"C:\Users\Strike\Desktop\python\tutorial\scientists")
# filepath = scientists[0]
# print(filepath)
# df = pd.read_json(filepath, lines=True)
# df.head()