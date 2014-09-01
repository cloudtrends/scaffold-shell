#! /usr/bin/python

from __future__ import division

import sys
import os
from Crypto.Hash import SHA256

import sys
import os
from Crypto.Hash import SHA256
from ctypes import *

#
if len(sys.argv) < 3:
    print "usage: vhd_reader imagename dest_name \n"
    exit(-1)

#print "target image name: ", sys.argv[1]


global_disk_type_val = 0


#
import MySQLdb
db_conn = MySQLdb.connect("172.16.204.110","root","password","vhd4k" )
cursor = db_conn.cursor()

def check_sha256_exist( sha256_key ):
    select_sql ='SELECT `key`  FROM sha256  WHERE `key`=\''+ sha256_key +'\' '
    count = cursor.execute( select_sql )
    if count == 1:
        result = cursor.fetchone();
        return True
    return False

def insert_new_sha256(sha256_key='', from_vhd=''):
    if len(sha256_key) != 64:
        return
    insert_sql = 'INSERT INTO sha256(`key`, from_vhd) values( \''+ sha256_key +'\' , \''+ from_vhd +'\' )'
    cursor.execute(insert_sql)



def get_sha256(content):
    h = SHA256.new()
    h.update(content)
    return h.hexdigest()


def print_content(content):
    print "\n--- --- --- --- --- --- --- BEGIN"
    for c in content:
        sys.stdout.write( hex ( ord(c) ) + ' ')
    print "\n--- --- --- --- --- --- --- END"



def print_hex(name='', content=None):
    print "--- --- --- --- --- --- --- BEGIN", name
    for c in content:
        sys.stdout.write( hex ( ord(c) ) + ' ')
    print name,"\n--- --- --- --- --- --- --- --- --- --- --- --- --- --- END"


class POINT(Structure):
    _fields_ = ("x", c_int), ("y", c_int)


print "--- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- "


def bytes2int(str):
    return int(str.encode('hex'), 16)

def bytes2hex(str):
    return '0x'+str.encode('hex')


def dynamic_disk(content):
    current_total = 0
    current_total_curr = 0
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    cookie = 8
    current_total = current_total + cookie
    cookie_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total

    #print cookie_val.value
    #print_hex('cookie_val', cookie_val)

    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---


    data_offset = 8
    current_total = current_total + data_offset

    print current_total_curr, current_total

    data_offset_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total

    #print_hex('data_offset_val', data_offset_val)
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    table_offset = 8
    current_total = current_total + table_offset
    table_offset_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total

    print_hex('table_offset_val', table_offset_val)

    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    header_version = 4
    current_total = current_total + header_version
    header_version_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total

    #print_hex('header_version_val', header_version_val)

    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    max_table_entries = 4
    current_total = current_total + max_table_entries
    max_table_entries_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total

    #ba_tmp = ()
    #i_tmp = 0
    #for c in max_table_entries_val:
    #    print 'a:',c
    #    if 4 == i_tmp:
    #        break
    #    l = list(ba_tmp)
    #    l.append(c)
    #    ba_tmp = tuple(l)
    #    i_tmp = i_tmp + 1

    #b = (8, 1, 0, 0)
    #print 'len:', len(ba_tmp)
    #total_sum = sum( ord( ba_tmp[i] )  << (i * 8) for i in range(4))

    total_ord_sum =  bytes2int( str( max_table_entries_val[:-1] ) )
    #print bytes2hex( str( max_table_entries_val[:-1] ) )
    #print 'total_sum:', total_sum

    print_hex('max_table_entries_val', max_table_entries_val)
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    block_size = 4
    current_total = current_total + block_size
    block_size_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total

    print_hex('block_size_val', block_size_val)

    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    check_sum = 4
    current_total = current_total + check_sum
    check_sum_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    parent_unique_id = 16
    current_total = current_total + parent_unique_id
    parent_unique_id_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    parent_time_stamp = 4
    current_total = current_total + parent_time_stamp
    parent_time_stamp_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    reserved = 4
    current_total = current_total + reserved
    reserved_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    parent_unicode_name = 512
    current_total = current_total + parent_unicode_name
    parent_unicode_name_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total

    name = parent_unicode_name_val.value
    #n1 = name.decode("latin-1")
    #n2 = name.decode("utf-8")
    #n3 = bytearray.fromhex(name).decode('utf-8')
    #n4 = name.decode('hex').decode('utf-8')
    #print 'unicode name=', parent_unicode_name_val.value
    #print n1
    #print n2
    #print n3
    #print n4
    #print_hex('parent_unicode_name_val', parent_unicode_name_val)

    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    parent_locator_entry1 = 24
    current_total = current_total + parent_locator_entry1
    parent_locator_entry1_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    parent_locator_entry2 = 24
    current_total = current_total + parent_locator_entry2
    parent_locator_entry2_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    parent_locator_entry3 = 24
    current_total = current_total + parent_locator_entry3
    parent_locator_entry3_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    parent_locator_entry4 = 24
    current_total = current_total + parent_locator_entry4
    parent_locator_entry4_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    parent_locator_entry5 = 24
    current_total = current_total + parent_locator_entry5
    parent_locator_entry5_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    parent_locator_entry6 = 24
    current_total = current_total + parent_locator_entry6
    parent_locator_entry6_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    parent_locator_entry7 = 24
    current_total = current_total + parent_locator_entry7
    parent_locator_entry7_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    parent_locator_entry8 = 24
    current_total = current_total + parent_locator_entry8
    parent_locator_entry8_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    reserved2 = 256
    current_total = current_total + reserved2
    reserved2_val = create_string_buffer(content[current_total_curr:current_total])
    current_total_curr = current_total
    # --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    print 'total', current_total, current_total_curr
    return total_ord_sum




def  fix_dist(content):
    global global_disk_type_val
    disk_type_val = 0

    while True:
        cookie = create_string_buffer(content[:8])
        print sizeof(cookie), repr(cookie.raw), cookie.value
        #print_content(content)
        features = create_string_buffer(content[8:12])
        file_format_version = create_string_buffer(content[12:16])
        data_off_set = create_string_buffer(content[16:24])

        time_stamp = create_string_buffer(content[24:28])
        creator_app = create_string_buffer(content[28:32])

        creator_ver = create_string_buffer(content[32:36])
        creator_os = create_string_buffer(content[36:40])


        ori_size = create_string_buffer(content[40:48])
        curr_size = create_string_buffer(content[48:56])

        disk_geo = create_string_buffer(content[56:60])
        disk_type = create_string_buffer(content[60:64])


        check_sum = create_string_buffer(content[64:68])

        unique_id = create_string_buffer(content[68:84])

        save_state = create_string_buffer(content[84:85])

        reserved = create_string_buffer(content[85:512])

        #print 'reserved:', reserved

        print_content(file_format_version)
        total_ord_sum =  bytes2int( str( data_off_set[:-1] ) )
        print 'data offset :', total_ord_sum
        #print 'data_off_set', bytes2int( str( data_off_set.value[:-1]  ) )
        #total_ord_sum =  bytes2int( str( data_off_set[:-1] ) )
        print_hex('data_off_set', data_off_set)

        print_hex('creator_ver', creator_ver)
        print_hex('creator_os', creator_os)

        print_hex('disk_geo', disk_geo)


        #print_hex('disk_type', disk_type)
        disk_type_val = bytes2int(disk_type[:-1])
        global_disk_type_val = disk_type_val
        print 'disk type is: ', str( global_disk_type_val  )


        print creator_app
        print_hex('creator_app', creator_app)

        print 'features:', file_format_version.raw, file_format_version.value
        #content = fp1.read(1024)
        #print_content(content)

        break
    return disk_type_val



file_name_vhd = sys.argv[1]
fp1 = open(file_name_vhd,"rb")
fp2 = open(sys.argv[2],"w")


mode = sys.argv[3]





def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def tell_pos(msg='', fp1=None):
    position = fp1.tell();
    print msg, "Current file position : ", position


def print_4_bytes_hex_value(one_bat_entry_array):
    hex_array =  "".join(map(lambda b: format(b, "02x"), one_bat_entry_array))
    print 'hex_array=', hex_array


content512 = fp1.read(512)
fix_dist(content512)


if global_disk_type_val != 3:
    print "vhd disk is not dynamic type (3) exit :", global_disk_type_val
    exit()




total_ord_sum = 0



statinfo = os.stat(file_name_vhd)

def dynamic_disk_check():
    global total_ord_sum
    content512_1536 = fp1.read(1024)
    #tell_pos('after read dynamic header :', fp1)
    #fix_dist(content)
    total_ord_sum = dynamic_disk(content512_1536)
    total_entries_num = total_ord_sum
    print 'total_ord_sum is :', total_ord_sum , ' each of them is 2m , so total is:', total_ord_sum * 1024 * 1024 * 2, ' readable:', sizeof_fmt( total_ord_sum * 1024 * 1024 * 2 )
    entries=total_ord_sum
    each_size= 4
    total_bat_offset = entries * each_size
    print 'max_table_entries_val =', total_ord_sum
    total_bat_offset_gap = total_bat_offset
    while total_bat_offset_gap > 512:
        total_bat_offset_gap = total_bat_offset_gap - 512
    total_bat_offset_gap = 512 - total_bat_offset_gap
    print 'total_bat_offset_gap:', total_bat_offset_gap
    total_bat_offset = total_bat_offset + total_bat_offset_gap
    print 'total_bat_offset: ',total_bat_offset
    #
    content_1536_to_bat = fp1.read(total_bat_offset)
    print 'total_bat_offset len: ', fp1.tell() - total_bat_offset
    tell_pos('after read bat ', fp1)
    curr_pos = 0
    print '=== === === === === === === === === === === === === === === === === === === === === === === === === === === '
    pre_offset_str=""
    for i in range(total_ord_sum):
        one_bat_entry = create_string_buffer(content_1536_to_bat[curr_pos:curr_pos+each_size])
        one_bat_entry_array = bytearray(one_bat_entry[:-1])
        for a in one_bat_entry_array:
            #print 'aaa', a
            continue
        one_bat_entry_reverse_array = bytearray(one_bat_entry[:-1])[::-1]
        for b in one_bat_entry_reverse_array:
            #print 'bbb', b
            continue
        #one_bat_entry_array=one_bat_entry_array
        #print len(one_bat_entry_array)
        #print_hex('one_bat_entry', one_bat_entry)
        #print bytes2int(str(one_bat_entry_array))
        curr_str = str(one_bat_entry_reverse_array)
        if pre_offset_str == curr_str:
            break
            print i ,
        else:
            #print_hex('one_bat_entry_array', str(one_bat_entry_array))
            #print bytes2int(curr_str) ,
            pre_offset_str = curr_str
            #one_bat_entry_offset =  bytes2int( str( one_bat_entry[:-1] ) )
            #if one_bat_entry_offset == 4294967295:
            #    break
            one_bat_entry_offset =  bytes2int( str( one_bat_entry_reverse_array[:-1] ) )
            if one_bat_entry_offset == 16777215:
                break
            print one_bat_entry_offset ,
            #print 'one_bat_entry_offset:', one_bat_entry_offset
            #for xx in one_bat_entry:
            #    print  hex(ord(xx)),
        #print "--- --- "
        #one_bat_entry_array = bytearray(one_bat_entry_array.reverse())
        #print_4_bytes_hex_value(one_bat_entry_array)
        #print_hex('one_bat_entry_array', str(one_bat_entry_array))
        #print_4_bytes_hex_value(one_bat_entry_reverse_array)
        #print_hex('one_bat_entry_reverse_array', str(one_bat_entry_reverse_array))
        curr_pos = curr_pos + each_size
        if i > 3 :
            continue

print '=== === === === === === === === === === === === === === === === === === === === === === === === === === === '

if 3 == global_disk_type_val:
    dynamic_disk_check()




def print_for_human(repeat_num, new_num, total_num):
    #print '\r[{0}] {1}%'.format('#'*(repeat_num/total_num), total_num)
    repeat_num = int(repeat_num)
    total_num = int(total_num)
    sys.stdout.write("\r repeat :  %.2f%%  %d  %d    " % (  (repeat_num/total_num) , repeat_num  , total_num ) )
    sys.stdout.flush()

def read_dynamic_content():
    global total_ord_sum

    count_repeat = 0
    count_new = 0
    count_total = 0
    #content_mbr = fp1.read(512)
    sha_map={}
    one_block_2m_plus_512 = 512 + (1024 * 1024 * 2)
    if True:
        left_size = 0
        for i in range(total_ord_sum):
            content_1536_to_bat = fp1.read( one_block_2m_plus_512  )
            if left_size < 1048575:
                print '\ncurrent ord num:', i, ' left size is:', left_size
            if not content_1536_to_bat :
                left_size = statinfo.st_size - fp1.tell()
                if 512 == left_size:
                    print '\nreach 512 break OK'
                #    break
                print '\nleft size:', left_size
                tell_pos('fp1 not readable pos: ', fp1)
                print '\n already read ord count:', i, '   total_ord_sum:', total_ord_sum
                break
            #tell_pos( '\n'  + str(i)  + ' blocks read 512 + 2M: ', fp1)
            step_k = 4096
            #sha256 = get_sha256(content_1536_to_bat[512:])
            begin = 512
            curr_index = 0
            while curr_index < 512:
                four_k_content = content_1536_to_bat[begin:begin+step_k]
                sha256 = get_sha256(four_k_content)
                if check_sha256_exist(sha256):
                    count_repeat = count_repeat + 1
                    pass
                else:
                    #insert_new_sha256(sha256,'')
                    count_new = count_new + 1
                count_total =  count_total + 1
                curr_index = curr_index + 1
                begin = begin + step_k
            left_size = statinfo.st_size - fp1.tell()
            print_for_human(count_repeat, count_new, count_total)
            if 512 == left_size:
                print 'reach 512 break, the format is OK'
                break

if 3 == global_disk_type_val:
    read_dynamic_content()


position = fp1.tell();
print "Current file position : ", position


print "total file position : ", statinfo.st_size



fp1.seek(statinfo.st_size - 512)
content512 = fp1.read(512)



fp1.seek(statinfo.st_size - 2098176)
content512 = fp1.read(512)





#print "begin check footer"
#fix_dist(content512)
fp1.close()
fp2.close()


