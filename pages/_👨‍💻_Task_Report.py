from email.policy import default
import streamlit as st
from Project_1 import callback_upload
from tools import ifchelper
from tools import graph_maker
from datetime import datetime
import pandas as pd
import numpy as np


#### Database


from deta import Deta # pip install deta
from dotenv import load_dotenv 

load_dotenv(".env")
DETA_KEY = "a0eaq7dsd6v_dcuPKnANQY2E9o12c1k3Ch2DKPQBLAUD"

# Initialize with a project key

deta = Deta(DETA_KEY)

db = deta.Base("Info1")

def save_to_database():
    for task in session.task_data_1:
        name = task["Name"]
        activity_advance = task["ActivityAdvance"]
        description = task["Description"]
        # Save the task data to Deta
        db.put({"Name": name, "ActivityAdvance": activity_advance, "Description": description})

#### Database

def initialize_session_state():
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["SequenceData"] = {}
    session["task_data_1"] = []
    session["modified"] = False


def load_data():
    if "ifc_file" in session:
        session.Graphs = {
            "objects_graph": graph_maker.get_elements_graph(session.ifc_file),
            "high_frquency_graph": graph_maker.get_high_frequency_entities_graph(session.ifc_file)
        }
        load_work_schedules()
        session["isHealthDataLoaded"] = True

def load_work_schedules():
    session.SequenceData = {
        "schedules": session.ifc_file.by_type("IfcWorkSchedule"),
        "tasks": session.ifc_file.by_type("IfcTask"),
        "ScheduleData": [{
            "Id": schedule.id(), 
            "Data": ifchelper.get_schedule_tasks(schedule)
            } for schedule in session.ifc_file.by_type("IfcWorkSchedule")
        ],
    }

def add_work_schedule():
    ifchelper.create_work_schedule(session.ifc_file, session["schedule_input"])
    load_work_schedules()
    
    
def draw_schedules():

        session= st.session_state
        number_of_schedules = len(session.SequenceData["schedules"])
        st.subheader(
            f'Work Schedules: {number_of_schedules}' 
        )
        schedules = [f'{work_schedule.Name} / {work_schedule.id()}'  for work_schedule in session.SequenceData["schedules"] or []]
        st.selectbox("Schedules", schedules, key="schedule_selector" )
        schedule_id = int(session.schedule_selector.split("/",1)[1]) if session.schedule_selector else None
        schedule = session.ifc_file.by_id(schedule_id) if schedule_id else None
        if schedule:
            tasks = ifchelper.get_schedule_tasks(schedule) if schedule else None
            if tasks:
                st.info(f'Number of Tasks : {len(tasks)}')
                task_data = ifchelper.get_task_data(tasks)
                st.table(task_data) 
                session.task_data_1 = task_data     
            else:
                st.warning("No Tasks 😥")
        else:
            st.warning("No Schedules 😥")
    
def execute():
    
    st.header(" 👨‍🔧 Report")

    if "isHealthDataLoaded" not in session:
        initialize_session_state()

    if not session.isHealthDataLoaded:
        load_data()

    if session.isHealthDataLoaded:
        tab1, tab2 = st.tabs(["📝 Schedules","📈 Report"])
        
        with tab1:
            draw_schedules()        
        
        with tab2:
            number_of_schedules_1 = len(session.SequenceData["schedules"])
            st.subheader(
                f'Work Schedules: {number_of_schedules_1}' 
            )
            schedules_1 = [f'{work_schedule.Name} / {work_schedule.id()}'  for work_schedule in session.SequenceData["schedules"] or []]
            st.selectbox("Schedules", schedules_1, key="schedule_selector_1" )
            schedule_id_1 = int(session.schedule_selector_1.split("/",1)[1]) if session.schedule_selector_1 else None
            schedule_1 = session.ifc_file.by_id(schedule_id_1) if schedule_id_1 else None
            if schedule_1:
                tasks_1 = ifchelper.get_schedule_tasks(schedule_1) if schedule_1 else None
                if tasks_1:
                    with st.form("entry_form", clear_on_submit=True):
                            
                        new_values = []
                        for i, task in enumerate(session.task_data_1):
                            
                            new_value = st.number_input(f"Activity Advance for {task['Name']}", min_value=0, max_value=100, key=i)
                            new_values.append(new_value)

                        "---"
                        submitted = st.form_submit_button("Save changes!")
                        if submitted:
                            # Copying the changes to the original dictionaries in task_data
                            
                            for i, new_value in enumerate(new_values):
                                session.task_data_1[i]["ActivityAdvance"] = new_value

                                if new_value == 0:
                                    Description= "Not started"
                                elif new_value > 0  and new_value < 30:
                                    Description= "Low advance"
                                elif new_value >= 30  and new_value < 60:
                                    Description= "Moderate advance"
                                elif new_value >= 60  and new_value < 99:
                                    Description= "Good advance"
                                elif new_value == 100:
                                    Description= "Finished"

                                session.task_data_1[i]["Description"] = Description
                            
                            save_to_database()
                            st.write("Data saved!")
                            st.table(session.task_data_1)
                            session.modified = True


                else:
                    st.warning("No Tasks 😵")
            else:
                st.warning("No Schedules 😵")

    else:
        st.header("Step 1: Load a file from the Home Page")

    
session = st.session_state

execute()
