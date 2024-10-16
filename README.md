# BraveDataCompressor

**BraveDataCompressor** is a Python tool that copies and compresses Brave browser user data with administrator privileges, ensuring secure access and efficient backups. It is used most often to copy user data from Windows to Linux, though right now, this script **only works with Windows**.

> **Warning**: Please close the Brave browser before running this script. The script may not work properly if Brave is running.

## Features

- Lists all user profiles available on the system.
- Allows selecting a user whose Brave browser data will be compressed.
- Compresses the user data into a ZIP file named `user_data_brave_<selected_user>.zip`.
- Ensures the script runs with administrator privileges using `pyuac`.
- Maintains the directory structure within the ZIP as `User Data/[contents]`.
- Supports verbose mode for detailed logging (use the `-v` flag).

## Prerequisites

Before running the script, make sure you have the following:

- Python 3.x installed.
- The required Python packages installed.

### Install Required Packages

You can install the required packages by running:

```bash
pip install pyuac pywin32
```

## How to Use

1. Clone this repository or download the script.

2. Open a terminal or command prompt in the directory containing the `script.py` file.

3. Run the script using Python:

```bash
python script.py
```

4. If you want detailed logging, run the script with the `-v` flag:

```bash
python script.py -v
```

5. If the script does not have administrator privileges, it will prompt you with a UAC (User Account Control) dialog to grant access.

6. The script will list the available users. Select the user whose Brave browser data you want to compress by entering the corresponding number.

7. The Brave browser user data will be compressed into a file named `user_data_brave_<selected_user>.zip` in the current directory.

## File Structure

The resulting ZIP file will follow this structure:

```
user_data_brave_<selected_user>.zip
└── User Data
    ├── file1
    ├── file2
    └── etc.
```

## Script Details

- **Script Name**: `script.py`
- **Compression Format**: ZIP
- **Default Output**: `user_data_brave_<selected_user>.zip`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credits

- [pyuac](https://pypi.org/project/pyuac/) is used for requesting administrator privileges.
- [pywin32](https://pypi.org/project/pywin32/) is used for Windows-specific functionality.
