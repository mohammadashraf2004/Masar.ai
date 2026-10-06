from __future__ import annotations
from pathlib import Path
import importlib.util, json, py_compile, zipfile
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'course_manifest.json').read_text(encoding='utf-8'))
lesson_files=sorted(ROOT.glob('M016-*/*.py'))
assert manifest['modules']==12
assert manifest['core_modules']==10
assert manifest['optional_modules']==1
assert manifest['lessons']==125
assert manifest['core_lessons']==94
assert manifest['optional_lessons']==31
assert len(list(ROOT.glob('M016-*')))==12
assert len(lesson_files)==125
ids=[]; slugs=[]; minutes=0; core_minutes=0; optional_minutes=0; projects=0; optional_projects=0
for p in lesson_files:
    py_compile.compile(str(p), doraise=True)
    spec=importlib.util.spec_from_file_location(p.stem,p)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    ids.append(m.LESSON_ID); slugs.append(m.LESSON_META['slug']); minutes += m.LESSON_META['duration_minutes']
    if m.LESSON_META['optional']:
        optional_minutes += m.LESSON_META['duration_minutes']
        assert m.MODULE_ID=='M016-11'
        assert m.LESSON_META['completion_required'] is False
    else:
        core_minutes += m.LESSON_META['duration_minutes']
        assert m.LESSON_META['completion_required'] is True
    assert len(m.EXERCISES)==2
    assert len(m.QUIZ)==3
    assert all('explanation' in q for q in m.QUIZ)
    assert m.TOPIC['id']==m.LESSON_ID
    if m.MODULE_PROJECT is not None:
        projects += 1
        if m.MODULE_PROJECT.get('optional'): optional_projects += 1
assert ids == [f'L016-{i:03d}' for i in range(1,126)]
assert len(slugs)==len(set(slugs))
assert minutes==6480, minutes
assert core_minutes==4815, core_minutes
assert optional_minutes==1665, optional_minutes
assert projects==11, projects
assert optional_projects==1, optional_projects
assets=json.loads((ROOT/'assets_manifest.json').read_text(encoding='utf-8'))
core_req=sum(1 for x in assets['manual_figures'] if x['curriculum_scope']=='CORE' and x['priority']=='REQUIRED')
core_opt=sum(1 for x in assets['manual_figures'] if x['curriculum_scope']=='CORE' and x['priority']=='OPTIONAL')
k_req=sum(1 for x in assets['manual_figures'] if x['curriculum_scope']=='OPTIONAL_KUBERNETES' and x['priority']=='REQUIRED_IF_TAKING_OPTIONAL_MODULE')
k_opt=sum(1 for x in assets['manual_figures'] if x['curriculum_scope']=='OPTIONAL_KUBERNETES' and x['priority']=='OPTIONAL')
assert (core_req,core_opt,k_req,k_opt)==(25,15,17,10),(core_req,core_opt,k_req,k_opt)
assert (ROOT/'projects'/'final_capstone.json').exists()
print('PASS: COURSE-016 structural validation')
print('Core: 10 modules | 94 lessons | 4815 min (80h15m)')
print('Optional Kubernetes: 1 module | 31 lessons | 1665 min (27h45m)')
print('Capstone: M016-12 | Total lesson minutes: 6480 (108h)')
print('Projects: 10 core + 1 optional + final capstone')
print('Figures: 25 core required + 15 core optional + 17 K8s required-if-taken + 10 K8s optional')
