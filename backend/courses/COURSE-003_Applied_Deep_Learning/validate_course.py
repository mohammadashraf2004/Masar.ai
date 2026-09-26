# -*- coding: utf-8 -*-
from pathlib import Path
import ast, importlib.util, json, sys
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'course_manifest.json').read_text(encoding='utf-8'))
files=[]; ids=[]; slugs=[]; errors=[]; exercise_count=0
for m in manifest['modules']:
    for l in m['lessons']:
        p=ROOT/l['file']; files.append(p); ids.append(l['id'])
        try:
            ast.parse(p.read_text(encoding='utf-8'))
            spec=importlib.util.spec_from_file_location(p.stem,p); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
            slugs.append(mod.TOPIC['slug']); exercise_count += len(mod.TOPIC['exercises'])
            assert mod.TOPIC['lesson']['has_code_examples'] is True
            assert len(mod.TOPIC['exercises']) >= 2
            for e in mod.TOPIC['exercises']:
                assert e.get('starter_code') and e.get('acceptance_criteria')
                ast.parse(e['starter_code'])
        except Exception as e:
            errors.append(f"{p}: {e}")
assert len(files)==manifest['lesson_count']==47
assert len(set(ids))==len(ids) and len(set(slugs))==len(slugs)
assert exercise_count>=94
if errors:
    print('VALIDATION ERRORS:'); print('\n'.join(errors)); sys.exit(1)
print(f"OK: {len(files)} lessons, {exercise_count} code exercises, {len(manifest['modules'])} modules")
