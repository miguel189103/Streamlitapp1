from email.policy import default
import streamlit as st
from Project_1 import callback_upload
from tools import ifchelper
from tools import graph_maker
import pandas as pd
import plotly.express as px


session = st.session_state

def initialize_session_state_1():
    session["isHealthDataLoaded1"] = False

def load_data_1():
    if "ifc_file" in session:
        session["isHealthDataLoaded1"] = True

def execute():
    
    st.header(" 🤖 Analysis")

    if "isHealthDataLoaded1" not in session:
        initialize_session_state_1()

    if not session.isHealthDataLoaded1:
        load_data_1()

    if session.isHealthDataLoaded1 and session.modified:
        updated_data = session.task_data_1         
        df = pd.DataFrame(updated_data)
        st.header("Please filter here:")

        Name_selection = st.multiselect(
            "Select the name of the activity:",
            options= df["Name"].unique(),
            default= df["Name"].unique(),
        )

        Description_selection = st.multiselect(
            "Select the state:",
            options= df["Description"].unique(),
            default= df["Description"].unique(),
        )

        activity_advance = st.multiselect(
            "Select the activity advance:",
            options= df["ActivityAdvance"].unique(),
            default= df["ActivityAdvance"].unique(),
        )

        df_selection = df.query(
                "Name == @Name_selection & Description == @Description_selection &  ActivityAdvance == @activity_advance"
            )

        st.dataframe(df_selection)

        activity_counts = df_selection["Description"].value_counts()
        fig = px.bar(
            activity_counts,
            x=activity_counts.index,
            y=activity_counts.values,
            labels={"x": "Description", "y": "Count"},
            title="Activities by Category",
            color_discrete_sequence=["#0083B8"]*len(activity_counts),
            template="plotly_white",
            )

        st.plotly_chart(fig)

    else: st.write("Please first modify the activities advance in the Task Report page")

execute()
                            

