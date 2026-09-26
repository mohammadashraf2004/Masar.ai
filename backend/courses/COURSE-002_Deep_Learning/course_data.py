# -*- coding: utf-8 -*-
"""Read the entire Deep Learning Foundations course as Python seed data.

Usage from this folder: python course_data.py
This is DATA ONLY, not a DB migration or an executable backend seeder.
"""
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parent
COURSE = json.loads((ROOT / 'course_manifest.json').read_text(encoding='utf-8'))

def load_lesson(path):
    source = ROOT / path
    spec = importlib.util.spec_from_file_location(source.stem, source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.TOPIC, module.SOURCE

def get_modules():
    modules = []
    for entry in COURSE['modules']:
        topics = [load_lesson(x['file'])[0] for x in entry['lessons']]
        modules.append({'title': entry['arabic_title'], 'description': entry['learning_objective'],
                        'order': int(entry['module_id'][1:]), 'topics': topics})
    return modules

# Compatible structural wrapper with the uploaded example's LEVELS -> TOPICS format.
# This course is reusable across multiple career tracks; do not assume that
# 'deep-learning-foundations' is an existing CareerTrack or overwrite an unrelated track.
LEVELS = get_modules()

if __name__ == '__main__':
    topics = [topic for module in LEVELS for topic in module['topics']]
    print('modules:', len(LEVELS), 'lessons:', len(topics),
          'guided_minutes:', sum(t['lesson']['estimated_minutes'] for t in topics))
