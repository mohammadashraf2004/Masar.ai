from pathlib import Path
import ast, json, re
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'course_manifest.json').read_text(encoding='utf-8'))
files=sorted((ROOT/'modules').glob('M007_*/*L007_*.py'))
assert len(files)==manifest['lessons']==60, (len(files), manifest['lessons'])
ids=[]; slugs=[]; total=0; project_count=0
for p in files:
    src=p.read_text(encoding='utf-8')
    ast.parse(src, filename=str(p))
    m=re.search(r"LESSON_ID = '([^']+)'", src); assert m, p
    ids.append(m.group(1))
    s=re.search(r'"slug": ([^,]+),', src); assert s, p
    slugs.append(ast.literal_eval(s.group(1)))
    mm=re.search(r'"estimated_minutes": ([0-9]+),',src); assert mm,p
    total += int(mm.group(1))
    if '"project": {' in src: project_count += 1
assert len(ids)==len(set(ids))==60
assert sorted(ids)==[f'L007-{i:03d}' for i in range(1,61)], sorted(ids)
assert len(slugs)==len(set(slugs))==60
assert total==manifest['guided_minutes']==2430, total
assert len(list((ROOT/'modules').glob('M007_*')))==10
assert project_count==10, project_count
print({'modules':10,'lesson_files':60,'guided_minutes':total,'guided_time':'40h30m','frozen_id_range':'L007-001..L007-060','unique_ids':True,'unique_slugs':True,'module_projects':project_count,'python_syntax':'PASS'})
