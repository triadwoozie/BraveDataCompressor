import os
import zipfile
import pyuac
import sys
import time

# Path to Brave user data
brave_user_data_path = r"C:\Users"

def get_users():
    # Get all user directories in C:\Users
    users = [f for f in os.listdir(brave_user_data_path) if os.path.isdir(os.path.join(brave_user_data_path, f))]
    return users

def select_user(users):
    # Display users and let the user choose one
    print("Available users:")
    for i, user in enumerate(users):
        print(f"{i + 1}. {user}")
    
    while True:
        try:
            selection = int(input("Select a user by number: ")) - 1
            if 0 <= selection < len(users):
                return users[selection]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def compress_user_data(user, verbose):
    user_data_path = os.path.join(brave_user_data_path, user, "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data")
    
    if not os.path.exists(user_data_path):
        print(f"User Data not found for user {user}.")
        return

    # Zip file name based on selected user
    output_zip = f"user_data_brave_{user}.zip"
    total_files = sum(len(files) for _, _, files in os.walk(user_data_path))  # Count total files for progress
    processed_files = 0

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        print(f"Compressing user data for {user}...")
        
        # Adding the contents under the path "User Data/"
        for root, dirs, files in os.walk(user_data_path):
            # Skip the GCM Store directory
            if 'GCM Store' in dirs:
                if verbose:
                    print("Skipping 'GCM Store' directory.")
                dirs.remove('GCM Store')  # Prevent os.walk from descending into GCM Store

            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip the lockfile
                if file == 'lockfile':
                    continue
                
                # Log the file being added to the zip if verbose mode is enabled
                if verbose:
                    print(f"Adding {file_path}...")
                
                # Attempt to write to the zip file, with a timeout for slow operations
                start_time = time.time()
                timeout = 5  # seconds
                
                while True:
                    try:
                        archive_name = os.path.join("User Data", os.path.relpath(file_path, user_data_path))
                        zipf.write(file_path, archive_name)
                        processed_files += 1
                        break  # Break the loop if the file is written successfully
                    except (PermissionError, OSError) as e:
                        if verbose:
                            print(f"Error accessing {file_path}: {e}")
                        break  # Skip the file if there's an error

                    # Check for timeout
                    if time.time() - start_time > timeout:
                        if verbose:
                            print(f"Timeout reached for {file_path}. Skipping...")
                        break
                
                # Display progress if not in verbose mode
                if not verbose:
                    percent = (processed_files / total_files) * 100
                    print(f"Progress: {percent:.2f}% completed", end='\r')

    if not verbose:
        print()  # For cleaner output after progress display
    print(f"User data for {user} has been compressed and saved as {output_zip}")

def main():
    # Check for verbose flag
    verbose = '-v' in sys.argv

    users = get_users()
    
    if not users:
        print("No users found.")
        return
    
    selected_user = select_user(users)
    compress_user_data(selected_user, verbose)

if __name__ == "__main__":
    # Check if the script is running with admin privileges, if not, request elevation
    if not pyuac.isUserAdmin():
        print("Requesting administrative privileges...")
        pyuac.runAsAdmin()
    else:
        main()
