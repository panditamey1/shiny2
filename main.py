import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import json 
import numpy as np
print("streamlit version: ", st.__version__)
# Sample follow_counts dictionary for demonstration purposes
# Replace this with your actual dictionary populated from CSV files
with open('follow_counts.json') as f:
    follow_counts = json.load(f)

# Function to get top numbers following the given number
def get_top_following_numbers(number, top_n=5):
    number = str(number)
    follow_list = follow_counts[number]
    follow_count_pairs = [(i, follow_list[i]) for i in range(len(follow_list))]
    follow_count_pairs.sort(key=lambda x: x[1], reverse=True)
    return follow_count_pairs[:top_n]

# Function to generate speech audio
def generate_speech(text):
    tts = gTTS(text)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file

# Streamlit app
st.title("Top")
saved_results = {}
# User input
number = st.number_input("Enter number:", min_value=0, max_value=36, step=1, key='number')
top_n_number = st.number_input("Enter number of top numbers:", min_value=1, max_value=20, step=1, value=10)

# Display top numbers following the given number
if st.button("Show Top Numbers"):
    if number not in saved_results:
        top_numbers = get_top_following_numbers(number, top_n=top_n_number)
        df = pd.DataFrame(top_numbers, columns=["Number", "Count"])
        st.write(f"Top {top_n_number} numbers following {number}:")
        st.table(df.transpose())

        # Generate and play speech
        numbers_text = ', '.join([str(num) for num, _ in top_numbers])

        speech_text = f" {numbers_text}."

        saved_results[number] = speech_text 
    else:
        st.write(f"Top {top_n_number} numbers following {number}:")
        st.write(saved_results[number])
        speech_text = saved_results[number]
    audio = generate_speech(speech_text)
    st.audio(audio, format='audio/wav',autoplay = True, loop =True)
number1 = st.number_input("Enter base number to add follow number:", min_value=0, max_value=36, step=1, key='number1')
number2add = st.number_input("Enter number to add as follow:", min_value=0, max_value=36, step=1, key='number2add')

# Add number to follow_counts
if st.button("Add number to follow_counts"):
    number1 = str(number1)
    number2add = str(number2add)
    follow_counts[number1].append(number2add)
    st.write(f"Number {number2add} added to follow_counts for {number1}")
    with open('follow_counts.json', 'w') as f:
        json.dump(follow_counts, f)
    # Generate and play speech
    #speech_text = f"Number {number2add} added to follow counts for {number1}."
    #audio = generate_speech(speech_text)
    #st.audio(audio, format='audio/mp3')
