# Polaroid Version Control

This Python script manages file uploads to an AWS S3 bucket named `polaroidfiles`. It allows for uploading, editing, and deleting files based on changes detected in a local folder structure.

## File Structure
```
.
├── README.md
├── main.py
└── {folder_name}/
    ├── uploaded.txt
    ├── {file_1}
    ├── {file_2}
    └── ...

```


## Functions

### 1. `get_image_size(image_path)`

- **Purpose**: Retrieves the width and height of an image file.
- **Dependencies**: Requires the PIL (`Pillow`) library for image processing.

### 2. `check_if_folder_exists(bucket, folder_name)`

- **Purpose**: Checks if a folder exists in the S3 bucket; creates it if not.
- **Dependencies**: Utilizes `boto3` for AWS S3 interaction.

### 3. `edit_create_mode_upload(bucket, i, folder_name)`

- **Purpose**: Uploads or edits a file in the S3 bucket based on changes detected locally.
- **Dependencies**: Uses `get_image_size` for metadata and `boto3` for file upload.

### 4. `delete_mode_upload(bucket, i, folder_name)`

- **Purpose**: Deletes a file from the S3 bucket.
- **Dependencies**: Utilizes `boto3` for AWS S3 interaction.

### 5. `read_file_info(file_path)`

- **Purpose**: Reads and returns file information (filename and modification time) from a local text file.

### 6. `get_folder_content(folder_path)`

- **Purpose**: Retrieves a list of files and their modification times from a local folder.

## Usage

1. **Setup**: Ensure you have Python 3.x installed along with the required libraries (`Pillow` and `boto3`).
   
2. **AWS Setup**: Set up your AWS credentials (`aws_access_key_id` and `aws_secret_access_key`) in the script.

3. **Folder Structure**: Organize your files in individual folders (`{folder_name}`) with an `uploaded.txt` file tracking uploads.

4. **Execution**: Run `main.py` to synchronize local changes with the S3 bucket:

5. **Monitoring**: Check console outputs for upload status and error messages.

## Notes

- Ensure `uploaded.txt` files are correctly formatted with filenames and modification times.
- Handle exceptions and errors that may occur during file operations and AWS S3 interactions.
