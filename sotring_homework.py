import os
import shutil
import zipfile

source_path = '/Users/vladislavtretakov/Desktop/test_folder_3'

os.makedirs(os.path.join(source_path, 'images'), exist_ok=True)
os.makedirs(os.path.join(source_path, 'documents'), exist_ok=True)
os.makedirs(os.path.join(source_path, 'audio'), exist_ok=True)
os.makedirs(os.path.join(source_path, 'video'), exist_ok=True)
os.makedirs(os.path.join(source_path, 'archives'), exist_ok=True)
os.makedirs(os.path.join(source_path, 'other'), exist_ok=True)

def normalize(input_str):
    cyrillic_to_latin = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z',
        'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }

    result_str = ''
    for char in input_str:
        if char.lower() in cyrillic_to_latin:
            result_str += cyrillic_to_latin[char.lower()] if char.islower() else cyrillic_to_latin[char.lower()].capitalize()
        elif char.isalnum() or char in {'_'}:
            result_str += char
        else:
            result_str += '_'

    return result_str

def extract_archive(file_path, destination_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == '.zip':

        folder_name = os.path.splitext(os.path.basename(file_path))[0]
        destination_folder = os.path.join(destination_path, folder_name)

        os.makedirs(destination_folder, exist_ok=True)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)

def sorting_files(source_path):
    for file in os.listdir(source_path):
        name, ext = os.path.splitext(file)
        ext = ext.lower()
        normalized_name = normalize(name)
        new_name = normalized_name + ext

        file_path = os.path.join(source_path, file)

        if ext == "":
            continue
        elif ext == '.pdf' or ext == '.doc' or ext == '.docx' or ext == '.txt' or ext == '.xlsx' or ext == '.pptx':
            destination_path = os.path.join(source_path, 'documents', new_name)
        elif ext == '.jpeg' or ext == '.png' or ext == '.jpg' or ext == '.svg':
            destination_path = os.path.join(source_path, 'images', new_name)
        elif ext == '.mp3' or ext == '.ogg' or ext == '.wav' or ext == '.amr':
            destination_path = os.path.join(source_path, 'audio', new_name)
        elif ext == '.avi' or ext == '.mp4' or ext == '.mov' or ext == '.mkv':
            destination_path = os.path.join(source_path, 'video', new_name)
        elif ext in ['.zip', '.gz', '.tar']:
            destination_path = os.path.join(source_path, 'archives', new_name)
            extract_archive(file_path, destination_path)
        else:
            print(f"Розширення {ext} не відомо")
            destination_path = os.path.join(source_path, 'other', new_name)

        shutil.move(file_path, destination_path)




sorting_files(source_path)

def remove_empty_folders(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)

remove_empty_folders(source_path)
