# Soundcloud DJ Parser

## Overview
The **Soundcloud DJ Parser** script is designed to help you gather email addresses of DJs who follow a specific SoundCloud channel. It scrapes the followers of a given SoundCloud channel and looks for the keyword "dj" in their username or description. When a match is found, the script extracts the user's email address and compiles the data into an Excel file. This tool is perfect for those looking to send promo material to DJs, allowing them to play your unreleased music.

## Installation

To use the script, you need to have Python installed along with a few additional libraries. You can install these dependencies using `pip` by running the following command:

```bash
pip install selenium openpyxl
```

Additionally, you'll need a Chrome WebDriver to run Selenium. Make sure it's installed and added to your system's PATH. You can download it here: [ChromeDriver](https://developer.chrome.com/docs/chromedriver?hl=ru#latest_chromedriver_binaries)

## How to Use
### Running the Script
You can either run the script directly or provide the SoundCloud channel name as a parameter.

### With Command-Line Argument:

To specify the SoundCloud channel using the command line, run the script as follows:

```bash
python sc_dj_parser.py --name <soundcloud_channel>
```

Replace <soundcloud_channel> with the technical name of the channel from the URL. For example, if the channel URL is https://soundcloud.com/bcco, the channel name would be bcco.

### Without Argument:

If you don't provide the SoundCloud channel name as a parameter, the script will prompt you to input it manually after starting.

```bash
python sc_dj_parser.py
```

## What the Script Does
The script opens a Chrome browser using Selenium and scrapes the followers of the given SoundCloud channel.
It searches each follower’s username and description for the word "dj" (case insensitive).
When a match is found, it extracts the email address from the user's description (if available) and compiles this data into an Excel file.
The final Excel file is named after the SoundCloud channel and will contain the following columns: User URL, User Name, and Email.
Note: The script physically opens and navigates through SoundCloud pages using the Chrome browser. This is necessary for data scraping and is completely normal, so don’t be alarmed when Chrome opens during the process.

### Example:
```bash
python sc_dj_parser.py --name bcco
```

This command will parse the followers of the bcco SoundCloud channel and save the collected data to an Excel file called bcco.xlsx.

## Merge Excel Files Script

This script is designed to merge all Excel files created by the `SC DJ Parser` script into a single Excel file. It scans the current directory for all `.xlsx` files and combines them into one, ensuring no duplicate entries (based on `User URL` and `Email`). Once the merge is complete, the original Excel files are deleted, leaving only the final merged file.

### How to Use

1. Run the script:

    ```bash
    python merge_excel_files.py
    ```

2. After running, the script will:
    - Collect all `.xlsx` files in the current directory (except any pre-existing merged files).
    - Merge the contents of these files, ensuring no duplicate entries.
    - Save the merged result into a new file called `dj_emails.xlsx`.
    - Delete the original Excel files.

### Notes

- **Unique Entries:** The script considers an entry as unique based on the combination of `User URL` and `Email`.
- **Output File:** The final merged file is named `dj_emails.xlsx`. If you run the script multiple times, any previously merged file will be updated with the new merged data, and old input files will be removed.
