

import shutil


import os


file_ends_with = ".go"
begin_dir = ""

move_to_dir = ""


file_begin_with = "m_"

def tmp_a():
    for dirpath, dnames, fnames in os.walk(begin_dir):
        for f in fnames:
            if f.endswith(file_ends_with):
                tmp_file_name = f
                if tmp_file_name.startswith(file_begin_with):
                    full_path =  os.path.join(dirpath, f)
                    #shutil.move( full_path,move_to_dir)



def tmp_b():

    for dirpath, dnames, fnames in os.walk(begin_dir):
        for f in fnames:
            if f.endswith(file_ends_with):
                tmp_file_name = f
                if tmp_file_name not in "funcs_map_gorp.go" :
                    continue
                #if tmp_file_name.startswith(file_begin_with):
                full_dir = dirpath
                full_path =  os.path.join(dirpath, f)
                #shutil.move( full_path,move_to_dir)
                #print full_path
                #print full_dir
                full_dirs = full_dir.split("/")
                tmp_domain = full_dirs[-1]
                if "gobbs" in tmp_domain:
                    tmp_domain = tmp_domain.replace("gobbs_","")
                #print tmp_domain
                new_file_name = tmp_file_name[:-3]+"_" + tmp_domain +".go"
                #print new_file_name
                from_file = full_dir +"/"+ tmp_file_name
                to_file = full_dir +"/"+ new_file_name
                print from_file
                print to_file
                #os.rename( from_file, to_file )





move_files_set = {}
def tmp_c():
    for dirpath, dnames, fnames in os.walk(begin_dir):
        for f in fnames:
            if f.endswith(file_ends_with):
                tmp_file_name = f
                full_dir = dirpath
                full_path =  os.path.join(dirpath, f)
                if move_files_set.has_key(tmp_file_name):
                    print "exists", tmp_file_name
                else:
                    move_files_set[ tmp_file_name ] = tmp_file_name
                    print full_path
                #shutil.move( full_path,move_to_dir)

tmp_c()

