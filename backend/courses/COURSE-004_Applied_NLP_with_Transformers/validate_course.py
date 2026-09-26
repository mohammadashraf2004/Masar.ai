from pathlib import Path
import ast, json, re, zipfile
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'course_manifest.json').read_text(encoding='utf-8'))
files=sorted((ROOT/'modules').glob('M004_*/*L004_*.py'))
assert len(files)==manifest['lessons']==71, (len(files), manifest['lessons'])
ids=[]; slugs=[]; total=0
for p in files:
    src=p.read_text(encoding='utf-8')
    ast.parse(src, filename=str(p))
    m=re.search(r"LESSON_ID = [\'\"]([^\'\"]+)", src); assert m, p
    ids.append(m.group(1))
    s=re.search(r'"slug": ([^,]+),', src); assert s, p
    slugs.append(ast.literal_eval(s.group(1)))
    mm=re.search(r'"estimated_minutes": (\d+),',src); assert mm,p
    total += int(mm.group(1))
assert len(ids)==len(set(ids))==71
assert len(slugs)==len(set(slugs))==71
assert total==manifest['guided_minutes']==2985, total
assert len(list((ROOT/'modules').glob('M004_*')))==11
print({'modules':11,'lesson_files':71,'guided_minutes':total,'guided_time':'49h45m','unique_ids':True,'unique_slugs':True,'python_syntax':'PASS'})
