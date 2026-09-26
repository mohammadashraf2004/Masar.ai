from pathlib import Path
import ast, json, re
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'course_manifest.json').read_text(encoding='utf-8'))
files=sorted((ROOT/'modules').glob('M005_*/*L005_*.py'))
assert len(files)==manifest['lessons']==70, (len(files), manifest['lessons'])
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
assert len(ids)==len(set(ids))==70
assert sorted(ids)==[f'L005-{i:03d}' for i in range(1,71)], sorted(ids)
assert len(slugs)==len(set(slugs))==70
assert total==manifest['guided_minutes']==3055, total
assert len(list((ROOT/'modules').glob('M005_*')))==10
print({'modules':10,'lesson_files':70,'guided_minutes':total,'guided_time':'50h55m','frozen_id_range':'L005-001..L005-070','unique_ids':True,'unique_slugs':True,'python_syntax':'PASS'})
