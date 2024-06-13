
# given csv file, for each number, find the top 5 numbers that follow it
import os
import pandas as pd
import json
WHEEL_LAYOUT = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
NUMBER_TO_POSITION = {num: idx for idx, num in enumerate(WHEEL_LAYOUT)}

# method
def get_top_5_following_numbers(number, top_n=5):
    number = str(number)
    follow_list = follow_counts[number]
    follow_count_pairs = [(i, follow_list[i]) for i in range(len(follow_list))]
    follow_count_pairs.sort(key=lambda x: x[1], reverse=True)
    # get key only
    follow_count_pairs = [i for i, _ in follow_count_pairs]
    return follow_count_pairs[:top_n]
    
def wheel_distance(num1, num2):
    pos1 = NUMBER_TO_POSITION[num1]
    pos2 = NUMBER_TO_POSITION[num2]
    dist = min((pos1 - pos2) % len(WHEEL_LAYOUT), (pos2 - pos1) % len(WHEEL_LAYOUT))
    return dist
def get_top_5_numbers_distance(top_5_numbers, next_number):
    return [wheel_distance(num,next_number) for num in top_5_numbers]

def get_min_distance(top_5_numbers_distance):
    return min(top_5_numbers_distance)
# read csv file
test_folder_path = 'test_files'
output_folder_path = 'output_files'
top_n = 7



for file_name in os.listdir(test_folder_path):
    if file_name.endswith('.csv'):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(os.path.join(test_folder_path, file_name))
        
        # Get the 'Number' column as a list
        numbers = df['Number'].tolist()
        column_name = "Number"

        # for each number, get the top 5 numbers from follow_counts and compare with actual next number
        follow_counts = json.load(open('follow_counts.json'))



        # create next number column 
        df['Next Number'] = df[column_name].shift(-1)

        df.dropna(inplace=True)
        # create top 5 numbers column
        column_top_n = f'Top {top_n} Numbers'
        df[column_top_n] = df[column_name].apply(get_top_5_following_numbers, top_n=top_n)

        column_top_n_distance = f'Top {top_n} Numbers Distance'
        df[column_top_n_distance] = df.apply(lambda x: get_top_5_numbers_distance(x[column_top_n], x['Next Number']), axis=1)

        df['Min Distance'] = df[column_top_n_distance].apply(get_min_distance)
        print("average distance: ", df['Min Distance'].mean())
        # add average distance to result file

        # add top n value to file name

        file_name = f'{file_name}_top_{top_n}.csv'

        output_file_name = file_name.replace('.csv', '_output.csv')
        df.to_csv(os.path.join(output_folder_path, output_file_name), index=False)
        
