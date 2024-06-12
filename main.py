import streamlit as st
import pandas as pd
from collections import defaultdict

# Sample follow_counts dictionary for demonstration purposes
# Replace this with your actual dictionary populated from CSV files
import json 
with open('follow_counts.json') as f:
    follow_counts = json.load(f)

# Function to get top 5 numbers following the given number
def get_top_5_following_numbers(number, top_n=5):
    number = str(number)
    follow_list = follow_counts[number]
    follow_count_pairs = [(i, follow_list[i]) for i in range(len(follow_list))]
    follow_count_pairs.sort(key=lambda x: x[1], reverse=True)
    return follow_count_pairs[:top_n]

# Streamlit app
st.title("Top")

# User input
number = st.number_input("Enter:", min_value=0, max_value=36, step=1)
top_n_number = st.number_input("Enter number of top numbers:", min_value=1, max_value=10, step=1, value=5)
# Display top 5 numbers following the given number
if st.button("Show Top 5 Numbers"):
    top_5_numbers = get_top_5_following_numbers(number, top_n=top_n_number)
    df = pd.DataFrame(top_5_numbers, columns=["Number", "Count"])
    st.write(f" {number}:")
    st.table(df.transpose())
    st.table(df)

# add number to follow_counts
if st.button("Add number to follow_counts"):
    number = st.number_input("Enter number to add:", min_value=0, max_value=36, step=1)
    follow_counts[number] = defaultdict(int)
    st.write(f"Number {number} added to follow_counts")
    with open('follow_counts.json', 'w') as f:
        json.dump(follow_counts, f)
