import os
import zipfile
import shutil
import pyuac
import sys

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

def compress_user_data(user):
    user_data_path = os.path.join(brave_user_data_path, user, "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data")
    
    if not os.path.exists(user_data_path):
        print(f"User Data not found for user {user}.")
        return

    # Zip file name based on selected user
    output_zip = f"user_data_brave_{user}.zip"
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Adding the contents under the path "User Data/"
        for root, dirs, files in os.walk(user_data_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Relocate files in the zip under "User Data/[contents]"
                archive_name = os.path.join("User Data", os.path.relpath(file_path, user_data_path))
                zipf.write(file_path, archive_name)
    
    print(f"User data for {user} has been compressed and saved as {output_zip}")

def main():
    users = get_users()
    
    if not users:
        print("No users found.")
        return
    
    selected_user = select_user(users)
    compress_user_data(selected_user)

if __name__ == "__main__":
    # Check if the script is running with admin privileges, if not, request elevation
    if not pyuac.isUserAdmin():
        print("Requesting administrative privileges...")
        pyuac.runAsAdmin()
    else:
        main()
