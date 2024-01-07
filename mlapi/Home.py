import streamlit as st
import os
import subprocess

st.set_page_config(layout="centered", page_title="MindWatch")

# Initialize error variable
error = False

test_path = "test.py"

# General Settings
st.subheader("General Settings", divider="grey")

# Input file directory
input_directory = st.text_input(
    "Input File path:", help="Enter the input file path", value=""
)
if input_directory and not os.path.isdir(input_directory):
    st.error("The provided file path does not exist. Please provide a valid file path.")
    error = True

# Aggressive Behavior Detection Settings
st.subheader("Mindwave Test", divider="grey")

if st.button("Start Test", type="primary"):
    try:
        subprocess.run(["python", test_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")