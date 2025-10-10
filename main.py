import streamlit as st
import pandas as pd
from player import Player

run_details = pd.read_csv("run_details.csv")

dungeons = run_details[run_details["player"] == "Ruana"].groupby(["dungeon_name"])["dungeon_name"].count().reset_index(name="record_count")


print(dungeons.head(8))
st.write("")
st.bar_chart(x="dungeon_name",y="record_count",data=dungeons,x_label="",y_label="Count",color="#AAD372",sort="-record_count",horizontal=True)



