import os
from PIL import Image
import boto3

def get_image_size(image_path):
    try:
        with Image.open(image_path) as image:
            width, height = image.size
            return width, height
    except Exception as e:
        print(f"Error opening image: {image_path} ({e})")
        return None, None

def check_if_folder_exists(bucket, folder_name):
    folder_exists = False
    for obj in bucket.objects.filter(Prefix=folder_name):
        if obj.key == folder_name:
            folder_exists = True
            break

    if not folder_exists:
        bucket.put_object(Key=f"{folder_name}/")
        folder_exists = True
    
    return folder_exists

def edit_create_mode_upload(bucket, i, folder_name):
    try:
        image_path = f"./{folder_name}/{i.split()[0]}"
        width, height = get_image_size(image_path)
        if width and height:
            metadata = {'width': str(width), 'height': str(height)}
            bucket.upload_file(image_path, f"{folder_name}/{i.split()[0]}", ExtraArgs={'Metadata': metadata})
            print(f"Uploaded {i.split()[0]} with size: {width}x{height}")
        else:
            print(f"Failed to get size for {i.split()[0]}")
    except Exception as e:
        print(f"Error uploading {i.split()[0]}: {e}")

def delete_mode_upload(bucket, i, folder_name):
    try:
        bucket.Object(f"{folder_name}/{i.split()[0]}").delete()
        print(f"Deleted {folder_name}/{i.split()[0]} from {bucket_name}")
    except Exception as e:
        print(f"Error deleting {i.split()[0]}: {e}")

def read_file_info(file_path):
    file_info = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                filename, mod_time = parts
                file_info.append(f"{filename} {mod_time}")
    return file_info

def get_folder_content(folder_path):
    folder_content = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file != "uploaded.txt":
                file_path = os.path.join(root, file)
                mod_time = os.path.getmtime(file_path)
                folder_content.append(f"{file} {mod_time}")
    return folder_content

s3 = boto3.resource('s3', aws_access_key_id='', aws_secret_access_key='')
bucket_name = 'polaroidfiles'
bucket = s3.Bucket(bucket_name)

for filename in os.listdir('./'):
    createMode = []
    deleteMode = []
    editMode = []
    if os.path.isdir(filename):
        uploadedFiles = read_file_info(file_path=f"./{filename}/uploaded.txt")
        existingFiles = get_folder_content(f"./{filename}")
        for existItem in existingFiles[:]:
            flag = False
            for uploadedItem in uploadedFiles[:]:
                if existItem.split()[0] == uploadedItem.split()[0]:
                    flag = True
                    uploadedFiles.remove(uploadedItem)
                    if existItem.split()[1] == uploadedItem.split()[1]:
                        continue
                    else:
                        editMode.append(existItem)
                    break
            if not flag:
                createMode.append(existItem)

        print(createMode)
        print(editMode)
        print(uploadedFiles)

        check_if_folder_exists(bucket, folder_name=filename)

        f = open(f"./{filename}/uploaded.txt", "r+")
        lines = f.readlines()
        for i in lines:
            if i.split()[0] in editMode:
                edit_create_mode_upload(bucket, i, folder_name=filename)
                lines.remove(i)
                lines.append(f"{editMode[editMode.index(i)]} \n")
            elif i.split()[0] in deleteMode:
                delete_mode_upload(bucket, i, folder_name=filename)
                lines.remove(i)
        for i in createMode:
            edit_create_mode_upload(bucket, i, folder_name=filename)
            lines.append(f"{i} \n")
        f.close()
        f = open(f"./{filename}/uploaded.txt", "w")
        f.writelines(lines)
        f.close()
