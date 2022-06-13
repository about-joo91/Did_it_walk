import pandas as pd
import pathlib
import os

class Recommend:
    def __init__(self):
        cos_sim_path = pathlib.Path(os.environ['COS_SIM_FILE_PATH'])
        self.cos_sim_df = pd.read_csv(cos_sim_path)

    def find_shoes_recommend(self, shoes):
        shoe_name = str(shoes) + '.png'
        recommend_items = self.cos_sim_df[shoe_name].sort_values(ascending=False)[1:4].index
        return recommend_items

recommendation = Recommend()