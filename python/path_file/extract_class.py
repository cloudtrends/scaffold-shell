



'''
            BELOW CODE ARE TOOLS FOR DJANGO MODEL PROCESS FOR MIGRATE

'''



def read_op():
    lines = [line.strip() for line in open('/Users/cloud/tmp/py_classes.txt')]
    for line in lines:
        if line.startswith('class '):
            if line.startswith('class M'):
                continue
            line = line.replace('(models.Model):', '').replace('class ', '')
            #print(line)# line
            #
            #print('from portal.models import ' + line)
            #print('admin.site.register('+ line +')')


def write_op():
    dest_file_name ='/Users/cloud/tmp/py_classes_4.txt'

    lines = [line for line in open('/Users/cloud/tmp/py_classes.txt')]
    all_new_lines = []
    for line in lines:
        if line in '    id = models.IntegerField(primary_key=True)  # AutoField?\n' and len(line) > 10:
            print('find')
            line_auto = '    id = models.AutoField(primary_key=True)\n'
            all_new_lines.append( line_auto )
        else:
            if line in '        managed = False\n' and len(line) > 10:
                print('skip')
            else:
                all_new_lines.append( line )
    print( all_new_lines )
    with open(dest_file_name, 'w') as f:
        f.write(''.join(all_new_lines))


def default_001():
    dest_file_name ='/Users/cloud/tmp/py_classes_5.txt'
    ori_file_name = '/Users/cloud/tmp/py_classes_001.txt'
    str_beginwith = '    id = models.AutoField(primary_key=True)\n'
    lines = [line for line in open(ori_file_name)]
    all_new_lines = []
    for line in lines:
        if line in str_beginwith :
            print('find:')
        else:
            all_new_lines.append( line )
    with open(dest_file_name, 'w') as f:
        f.write(''.join(all_new_lines))


default_001()



