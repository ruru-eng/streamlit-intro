import streamlit as st
import pandas as pd
from player import Player
from datetime import timedelta, date, datetime
import altair as alt

# Load data
df = pd.read_csv("run_details.csv")
chars = pd.read_csv("characters.csv")
static = pd.read_csv("static_info.csv")

# Set default dates
start_date = date(2025, 8, 13)
end_date = date.today()
default_date_range = (start_date, end_date)

# If not, then initialize it
if "selected_date" not in st.session_state:
    st.session_state.selected_date = default_date_range

# Function to reset the date range
def reset_date_range():
    st.session_state.selected_date = default_date_range

# Layout
col1, col2 = st.columns(2)
with col1:
        player_selection = st.selectbox(
            "Pick a player:",
            [name.capitalize() for name in chars["name"].to_list()]
        )
        st.write("**Selected player:**", player_selection)
        player = Player(player_selection, "") #name, realm

with col2:
    # Reset button
    if st.button("Reset Date Range"):
        reset_date_range()
    # Date range slider
    selected_date = st.slider(
        "Select a date range:",
        min_value=start_date,
        max_value=end_date,
        value=st.session_state.selected_date,
        format="MM/DD/YYYY",
        step=timedelta(days=1),
        key="selected_date"
    )
with st.container(border=True,horizontal=True,horizontal_alignment="center"):
     st.metric(label="Item level",value=player.fetch_static_data(static)["item_level"])
     st.metric(label="M+ score",value=player.fetch_static_data(static)["mplus_score"])
     st.write(f"Raid progression\n{player.fetch_static_data(static)["raid_progression"]}")
    #  st.metric(label="Raid Progression",value=player.fetch_static_data(static)["raid_progression"])
with st.container(border=True):
    dungeons = alt.Chart(player.fetch_dungeon_data_with_time(df,selected_date)).mark_bar(cornerRadiusTopRight=5,cornerRadiusBottomRight=5).encode(
        x=alt.X("record_count:Q",axis=alt.Axis(tickMinStep=1)).title("Record Count"),
        y=alt.Y("dungeon_name:O",axis=alt.Axis(labelLimit=200)).title("").sort("-x"),
        color=alt.Color("timed").scale(scheme="category10")
    ).properties(title="Dungeon distribution").configure_legend(disable=True)
    st.altair_chart(dungeons, use_container_width=True)

with st.container(border=True):
    bar_chart = alt.Chart(player.fetch_level_data_with_time(df,selected_date)).mark_bar(cornerRadiusTopLeft=5,cornerRadiusTopRight=5,size=30).encode(
        x=alt.X("mythic_level:Q",axis=alt.Axis(labelAngle=0,tickMinStep=1)).title("Level"),
        y=alt.Y("record_count:Q",axis=alt.Axis(tickMinStep=5)).title("Record Count"),
        color=alt.Color("timed").scale(scheme="category10")
    ).properties(title="Level distribution").configure_legend(disable=True)
    st.altair_chart(bar_chart, use_container_width=True)

