#!/usr/bin/env python

import json,fire,re
from pathlib import Path

def is_export(cell):
    if cell['cell_type'] != 'code': return False
    src = cell['source']
    if len(src) == 0 or len(src[0]) < 7: return False
    #import pdb; pdb.set_trace()
    return re.match(r'^\s*#\s*export\s*$', src[0], re.IGNORECASE) is not None

def notebook2script(fname):
    "Finds cells starting with `#export` and puts them into a new module"
    fname = Path(fname)
    fname_out = f'nb_{fname.stem.split("_")[0]}.py'
    main_dic = json.load(open(fname,'r'))
    code_cells = [c for c in main_dic['cells'] if is_export(c)]
    module = f'''
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: dev_nb/{fname.name}

'''
    for cell in code_cells: module += ''.join(cell['source'][1:]) + '\n\n'
    # remove trailing spaces
    module = re.sub(r' +$', '', module, flags=re.MULTILINE)
    output_path = fname.parent/'fastlib'/fname_out
    open(output_path,'w').write(module[:-2])
    print(f"Converted {fname} to {output_path}")

if __name__ == '__main__': fire.Fire(notebook2script)

