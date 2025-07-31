import numpy as np
import pandas as pd
import random
import string
import logging
import matplotlib.pyplot as plt

def grnerate_log_entry():
       """
       Generate a random log entry with a timespan, lig level, action and user.
       """
       timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
       log_level = random.choices(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"])
       action = random.choice(["Login", "Logout", "Data Request", "File Upload", "Download", "Error"])
       user = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) # Random 6 characters user id will be formed
       return f"{timestamp} - {log_level} - {action} - User:{user}"

# function write a log to a file

def write_logs_to_file(log_filename, num_entries=100):
       """
       Write the specifed number of logs in the given file.
       """
       try:
              with open(log_filename, 'w') as file:
                     for _ in range(num_entries):
                            log = grnerate_log_entry()
                            file.write(log + '\n')
              print(f"Logs has been Successfully written to the file, {log_filename}.")
       except Exception as e:
              logging.error(f"Error in the write_logs_to_file: {e}")
              print("An error occured while writting logs to the files.")

# Function to read the logs file and process it.

def load_and_process_logs(log_filename= "data_processing_generated_logs.txt"):
       """
       Loads and processes the logs from the given file, cleaning and parsing the timespans.
       """
       try:
              # Ready the log file into a pandas DataFrame, spliting by the '-' separator
              df =pd.read_csv(log_filename, sep=' - ', header=None, names=["Timestamp", "Log_Level", "Action", "User"], engine="python")

              df["Timestamp"] = df["Timestamp"].str.strip() # clean and trim space around the Timestamp

              # convert the timestamp coulam to datetime
              df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

              # drop rows invalid timestamp
              df = df.dropna(subset=["Timestamp"])

              if df.empty:
                     print("No valid data found after timestap conversion.")
              else:
                     print("Data after ti,estapm conversion:")
                     print(df.head())  #show the data after cleanning

               # set the Timestamp colum as the index for time-vased operations/calculations      
              df.set_index('Timestamp', inplace=True)

              return df
       except Exception as e:
              print(f"Error processing log file: {e}")
              return None
       
# Fuction to perfom basic statistical analysis using pandas and numpy

def analyze_data(df):
       """
       Performs the basics analysis, such as counting log levels and actions, and computing basic statistics such as mean, max etc.
       """
       try:
              if df is None or df.empty:
                     print("No data available for analysis.")
                     return None, None
              
              # count the occurance to each log level
              log_level_counts = df['Log_Level'].value_counts()

              #count the occurrence of each action
              action_counts = df['Action'].value_counts()

              log_count = len(df)      #total number of logs
              unique_users = df['User'].nunique() # Number of unique_users
              logs_per_day = df.resample('D').size() # Number of logs per day

              # Averages of actions per day
              average_logs_per_day = logs_per_day.mean()

              #Max logs per day
              max_logs_per_day = logs_per_day.max()

              #Display summary statistics
              print("\nLog Leve; Counts:\n", log_level_counts)
              print("\nAction Counts:\n", action_counts)
              print(f"\nTotal Number of Logs:{log_count}")
              print(f"Number of unique Users: {unique_users}")
              print(f"Average Logs per day: {average_logs_per_day:.2f}")
              print(f"Max logs per day: {max_logs_per_day}")

              # create a dictinary to return the analysis results
              stats = {
                     "log_level_counts": log_level_counts,
                     "action_counts": action_counts,
                     "log_count": log_count,
                     "unique_users": unique_users,
                     "average_logs_per_day": average_logs_per_day,
                     "max_logs_per_day":max_logs_per_day
              }

              return stats
       except Exception as e:
              print(f"Error analyzing data: {e}")
              return None
       
#function to Visualize trends over time using Matplotlib
def visualize_treands(df):
              """
              visualises log frequency trend over time using matplotlib.
              """
              try:
                     logs_by_days = df.resample('D').size()

                     # plotting log frequency over time using matplotlib
                     plt.figure(figsize=(10,5))
                     plt.plot(logs_by_days.index, logs_by_days.values, marker='o', linestyle='-', color='b')
                      
                      # customize the ploat
                     plt.title("Log Frequency Over Time")
                     plt.xlabel("Date")
                     plt.ylabel('Number of logs')
                     plt.xticks(rotation=45)
                     plt.grid(True)

                     # show the plot
                     plt.tight_layout()
                     plt.show()

              except Exception as e:
                     print(f"Error visualing data: {e}")

log_filename = 'data_processing_generated_logs.txt'

# step1: write random logs to the files
write_logs_to_file(log_filename, num_entries=200)

# step 2: Looad and Process the logs from the  file
df_logs = load_and_process_logs(log_filename)

# step 3: Perform basic analysis on the log data
if df_logs is not None:
       stats = analyze_data(df_logs)

        # step 4: Visualise trend over time
       visualize_treands(df_logs)
