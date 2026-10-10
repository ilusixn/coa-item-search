# Builds CoAItemSearch_Data (the item list) from your own server's acore_world.item_template.
#
#   python tools/make_item_data.py --mysql "C:/CoA-Repack/mysql/bin/mysql.exe" --defaults "C:/CoA-Repack/mysql/admin-client.ini"
#   python tools/make_item_data.py --tsv items.tsv          (a tab-separated export: entry, Quality, ItemLevel, name)
#
# Writes CoAItemSearch_Data/data1.lua ... data8.lua next to this repo's CoAItemSearch_Data.toc. Each file holds one big
# Lua string of "id<\1>quality<\1>itemlevel<\1>name" lines: a few strings instead of hundreds of thousands of tables,
# because the 32-bit 3.3.5 client is short on memory. The data addon is LoadOnDemand: it loads on the first /items.
import argparse, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'CoAItemSearch_Data')
QUERY = ("SELECT entry, Quality, ItemLevel, REPLACE(REPLACE(name, '\\n', ' '), '\\t', ' ') "
         "FROM acore_world.item_template ORDER BY entry")

ap = argparse.ArgumentParser()
ap.add_argument('--mysql', help='path to mysql.exe')
ap.add_argument('--defaults', help='MySQL client .ini with the server login (--defaults-file)')
ap.add_argument('--tsv', help='use an existing tab-separated export instead of MySQL')
ap.add_argument('--files', type=int, default=8)
args = ap.parse_args()

if args.tsv:
    text = open(args.tsv, encoding='utf-8', errors='replace').read()
else:
    if not args.mysql:
        ap.error('give --mysql (and --defaults) or --tsv')
    cmd = [args.mysql] + (['--defaults-file=' + args.defaults] if args.defaults else []) + ['-N', '--batch', '-e', QUERY]
    text = subprocess.run(cmd, capture_output=True, check=True).stdout.decode('utf-8', errors='replace')

SEP = chr(1)
lines = []
for l in text.splitlines():
    p = l.split('\t')
    if len(p) < 4 or not p[3]:
        continue
    name = p[3].replace(']', '').replace(chr(92), '')            # nothing that could close the Lua long string
    lines.append(SEP.join((p[0], p[1], p[2], name)))

os.makedirs(OUT, exist_ok=True)
size = len(lines) // args.files + 1
toc = ['## Interface: 30300', '## Title: CoA Item Search (data)',
       '## Notes: Item list for CoA Item Search, loaded on demand', '## LoadOnDemand: 1']
for i in range(args.files):
    name = 'data%d.lua' % (i + 1)
    part = '\n'.join(lines[i * size:(i + 1) * size])
    open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n').write(
        'CoAItemSearchData = CoAItemSearchData or {}\ntable.insert(CoAItemSearchData, [==[\n' + part + '\n]==])\n')
    toc.append(name)
open(os.path.join(OUT, 'CoAItemSearch_Data.toc'), 'w', encoding='utf-8', newline='\n').write('\n'.join(toc) + '\n')
print('%d items written to %s' % (len(lines), os.path.normpath(OUT)))
