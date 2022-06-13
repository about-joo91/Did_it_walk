import pandas as pd
import pathlib

class Recommend:
    def __init__(self):
        cos_sim_path = pathlib.Path(r'/Users/kohyunwoo/Downloads/cos_sim_eff_v2_l.csv')
        self.cos_sim_df = pd.read_csv(cos_sim_path)

    def find_shoes_recommend(self, shoes):
        shoe_name = str(shoes) + '.png'
        recommend_items = self.cos_sim_df[shoe_name].sort_values(ascending=False)[1:4].index
        return recommend_items

recommendation = Recommend()