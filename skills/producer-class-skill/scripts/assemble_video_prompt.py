"""Assemble a complete single-shot prompt using the user-approved concise labels."""
import argparse
import hashlib
import json
import math
import re
from pathlib import Path


def require_text(spec, key):
    value = spec.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Missing non-empty text: ' + key)
    if value.strip().lower() in {'tbd', '待确认', '同上', '沿用上文', '...', '…'}:
        raise ValueError('Unresolved text in final prompt: ' + key)
    return value.strip()


def shot_fields(spec):
    """Validate explicit delivery fields; do not infer optical correctness."""
    shot = spec.get('shot')
    if not isinstance(shot, dict):
        raise ValueError('Provide structured shot fields; old five-block input is incomplete')
    text_keys = ('id', 'aspect_ratio', 'shot_size', 'camera_position',
                 'focal_length', 'aperture_dof', 'focus', 'composition', 'movement')
    unknown = set(shot) - set(text_keys) - {'duration_seconds', 'edit_seconds', 'camera_lens'}
    if unknown:
        raise ValueError('Unknown shot fields: ' + ', '.join(sorted(unknown)))
    values = {key: require_text(shot, key) for key in text_keys}
    for key in ('duration_seconds', 'edit_seconds'):
        if key == 'edit_seconds' and key not in shot:
            continue
        value = shot.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError('Provide positive finite number: shot.' + key)
    if shot.get('edit_seconds', 0) > shot['duration_seconds']:
        raise ValueError('edit_seconds exceeds generated clip duration; revise the plan')
    if not re.fullmatch(r'[1-9]\d*(?:\.\d+)?\s*:\s*[1-9]\d*(?:\.\d+)?', values['aspect_ratio']):
        raise ValueError('aspect_ratio must be a positive W:H ratio, e.g. 16:9')
    metadata = '时长：' + str(shot['duration_seconds']) + '秒。\n画幅：' + values['aspect_ratio'] + '。'
    camera_values = []
    if 'camera_lens' in shot:
        camera_values.append(require_text(shot, 'camera_lens'))
    camera_values += [values[key] for key in ('focal_length', 'aperture_dof',
                      'camera_position', 'focus', 'composition', 'movement')]
    camera = '景别：' + values['shot_size'] + '\n\n摄影参数：' + '；'.join(camera_values)
    assets = spec.get('assets')
    if not isinstance(assets, list):
        raise ValueError('Provide assets list; use [] for text-only generation')
    asset_lines, slots = [], set()
    for asset in assets:
        if not isinstance(asset, dict) or set(asset) != {'slot', 'name', 'use'}:
            raise ValueError('Each asset requires exactly slot, name, use')
        fields = {key: require_text(asset, key) for key in ('slot', 'name', 'use')}
        if fields['slot'] in slots:
            raise ValueError('Duplicate asset slot: ' + fields['slot'])
        slots.add(fields['slot'])
        asset_lines.append(fields['slot'] + '《' + fields['name'] + '》：' + fields['use'])
    return metadata, '；'.join(asset_lines) if asset_lines else '无参考图', camera


def assemble(spec):
    if not isinstance(spec, dict):
        raise ValueError('Input must be one JSON object')
    allowed = {
        'style', 'body', 'camera_mode', 'consistency_tail',
        'prefix', 'camera_suffix', 'common_tail',
        'shot', 'assets', 'sound', 'binding', 'transitions',
    }
    unknown = set(spec) - allowed
    if unknown:
        raise ValueError('Unknown fields: ' + ', '.join(sorted(unknown)))
    style = spec.get('style')
    if style != 'project':
        raise ValueError('Use project style with complete explicit project text')
    body = require_text(spec, 'body')
    binding = require_text(spec, 'binding')
    transitions = require_text(spec, 'transitions') if 'transitions' in spec else ''
    consistency = require_text(spec, 'consistency_tail')
    sound = require_text(spec, 'sound')
    metadata, asset_text, camera_fields = shot_fields(spec)
    if spec.get('camera_mode') not in (None, 'project'):
        raise ValueError('Use project photography with explicit camera fields')
    prefix = require_text(spec, 'prefix')
    camera = require_text(spec, 'camera_suffix') if 'camera_suffix' in spec else ''
    common_tail = require_text(spec, 'common_tail')
    camera_mode = 'project'

    if camera:
        camera_fields += '\n' + camera
    # Legacy end-state input joins the last action paragraph, never a separate section.
    action = body + (' ' + transitions if transitions else '')
    parts = [
        ('shot', metadata),
        ('style', '风格：' + prefix),
        ('binding', '参考图绑定与初态：' + asset_text + '。' + binding),
        ('action', '动作：\n' + action),
        ('photography', camera_fields),
        ('sound', '声音：' + sound),
        ('constraints', '必要约束：' + common_tail + '\n' + consistency),
    ]
    output = '\n\n'.join(text for _, text in parts) + '\n'
    report = {
        'style': style,
        'schema_version': 5,
        'unit': 'single_shot',
        'format': 'duration/aspect -> style -> reference binding/initial state -> action including final state -> shot size -> photography -> sound -> necessary constraints',
        'shot_id': spec['shot']['id'],
        'edit_seconds': spec['shot'].get('edit_seconds'),
        'legacy_transitions_merged': bool(transitions),
        'field_check_passed': True,
        'semantic_review': 'required: optics, action timing, project constraints, model support',
        'camera_mode': camera_mode,
        'adaptations': [],
        'blocks': [{'name': name, 'characters': len(text),
                    'sha256': hashlib.sha256(text.encode()).hexdigest()}
                   for name, text in parts],
        'media_generated': False,
    }
    return output, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('Input and output must be different files')
    if args.report and args.report.resolve() in (args.input.resolve(), args.output.resolve()):
        parser.error('Report must be a separate file')
    if args.output.exists() or (args.report and args.report.exists()):
        parser.error('Output/report already exists; choose a new versioned filename')
    try:
        text, report = assemble(json.loads(args.input.read_text()))
    except (ValueError, OSError, StopIteration) as error:
        parser.error(str(error))
    with args.output.open('x') as handle:
        handle.write(text)
    if args.report:
        with args.report.open('x') as handle:
            handle.write(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('Assembled labelled prompt for style ' + report['style'] + '; field checks passed, semantic review still required; no media generated.')


if __name__ == '__main__':
    main()
