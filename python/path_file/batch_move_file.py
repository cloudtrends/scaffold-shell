

import shutil


import os


file_ends_with = ".go"
begin_dir = ""

move_to_dir = ""


file_begin_with = "m_"

for dirpath, dnames, fnames in os.walk(begin_dir):
    for f in fnames:
        if f.endswith(file_ends_with):
            tmp_file_name = f
            if tmp_file_name.startswith(file_begin_with):
                full_path =  os.path.join(dirpath, f)
                shutil.move( full_path,move_to_dir)


