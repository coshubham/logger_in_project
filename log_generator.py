import random
import string
import time
import logging

# setting up logging for error handling
logging.basicConfig(filename="log_generator_error.log", level=logging.ERROR)

# List the level of logs
LOG_LEVELS = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]

# List of posible actions
ACTIONS = ["Login", "Logout", "Data Request", "File Upload", "Download", "Error"]

# Function to generate random strings for logs
def random_string(length=10):
    """Generate a random string of given length (default length is 10)"""
    try:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    except Exception as e:
        logging.error(f"Error generating random string: {e}")
        return "Error"

       
# Function to generate a log entry

def generate_log_entry():
       """Generate a random log entry with a timestamp, log level, action, and user"""

       try:
              log_level = random.choice(LOG_LEVELS)
              timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
              action = random.choice(ACTIONS)
              user = random_string(8)  # Random user ID of length 8
              log_entry = f"{timestamp} - {log_level} - {action} - User: {user}"
              return log_entry
       except Exception as e:
              logging.error(f"Error generating log entry: {e}")
              return "Error generating log entry"
       
# Function to write logs to a file

def write_logs_to_file(log_filename, num_entries=100):
       """Write the specified number of logs to the given file."""

       try:
              with open(log_filename, 'w') as file:
                     for _ in range(num_entries):
                            log = generate_log_entry()
                            if log != "ERROR":
                                   file.write(log + "\n")
              print(f"Logs have been Successfully write to {log_filename}")
       except Exception as e:
              logging.error(f"Error writing logs to file: {e}")
              print("An error occurred while writing logs. Check log_generator_error.log for details.")

# Generate and write 200 random entries

write_logs_to_file("generated_logs.txt", num_entries=200)  # change num_entries as needed