import pandas as pd
import numpy as np

class Player:
    all = []

    # initialize player attributes
    def __init__(self,name,realm):
        self.__name = name
        self.__realm = realm

        Player.all.append(self)

    @property 
    def name(self):
        return self.__name
    @property 
    def realm(self):
        return self.__realm
    
    # filter date range
    @staticmethod
    def prepare_set(df,sel_date):
        df["timed"] = np.where(df["num_chests"] == 0,"Untimed","Timed")
        df["completed_at"] = pd.to_datetime(df["completed_at"]).dt.date
        return df.loc[(df["completed_at"] >= sel_date[0]) & (df["completed_at"] <= sel_date[1])]
            
    # retrieve dungeon data in time range
    def fetch_dungeon_data_with_time(self,df,sel_date):
        f_df = Player.prepare_set(df,sel_date)
        return f_df[f_df["player"] == self.__name].groupby(["dungeon_name"])["dungeon_name"].count().reset_index(name="record_count")
    
    # retrieve level data in time range
    def fetch_level_data_with_time(self,df,sel_date):
        f_df = Player.prepare_set(df,sel_date)
        return f_df[f_df["player"] == self.__name].groupby(["mythic_level","timed"])["mythic_level"].count().reset_index(name="record_count")
    