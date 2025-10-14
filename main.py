import streamlit as st
import pandas as pd
from player import Player
from datetime import timedelta, date, datetime
import altair as alt

# Load data
df = pd.read_csv("run_details.csv")
chars = pd.read_csv("characters.csv")


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
with st.container(border=True):
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
    # Bar chart
    st.write("Dungeon distribution")
    st.bar_chart(
        data=player.fetch_dungeon_data_with_time(df,selected_date),
        x="dungeon_name",
        y="record_count",
        x_label="Record Count",
        y_label="",
        sort="-record_count",
        horizontal=True
    )

print(alt.theme.names())
with st.container(border=True):

    bar_chart = alt.Chart(player.fetch_level_data_with_time(df,selected_date)).mark_bar().encode(
        x="mythic_level:N",
        y="record_count:Q",
        color="timed"
    )
    st.altair_chart(bar_chart, use_container_width=True)

