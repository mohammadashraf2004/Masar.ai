from pathlib import Path
import ast,json,re
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'course_manifest.json').read_text(encoding='utf-8'))
files=sorted((ROOT/'modules').glob('M008_*/*L008_*.py'))
assert len(files)==manifest['lessons']==106,(len(files),manifest['lessons'])
ids=[]; slugs=[]; total=0; project_count=0
for p in files:
    src=p.read_text(encoding='utf-8'); ast.parse(src,filename=str(p))
    m=re.search(r"LESSON_ID = '([^']+)'",src); assert m,p; ids.append(m.group(1))
    tree=ast.parse(src); topic_node=None
    for node in tree.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TOPIC' for t in node.targets): topic_node=node.value
    assert topic_node is not None,p
    # DifficultyLevel enum references make full literal_eval impossible, so extract slug/minutes by regex.
    s=re.search(r"'slug': '([^']+)'",src); assert s,p; slugs.append(s.group(1))
    mm=re.search(r"'estimated_minutes': ([0-9]+)",src); assert mm,p; total+=int(mm.group(1))
    if "'project': {" in src: project_count+=1
assert len(ids)==len(set(ids))==106
assert sorted(ids)==[f'L008-{i:03d}' for i in range(1,107)],sorted(ids)
assert len(slugs)==len(set(slugs))==106
assert total==manifest['guided_minutes']==5815,total
assert len(list((ROOT/'modules').glob('M008_*')))==11
assert project_count==11,project_count
assets=list((ROOT/'assets').glob('*.png')); assert len(assets)==manifest['visual_assets']==76,len(assets)
assert len(json.loads((ROOT/'assets_manifest.json').read_text(encoding='utf-8')))==76
print({'modules':11,'lesson_files':106,'guided_minutes':total,'guided_time':'96h55m','frozen_id_range':'L008-001..L008-106','unique_ids':True,'unique_slugs':True,'module_projects':project_count,'visual_assets':len(assets),'python_syntax':'PASS'})
