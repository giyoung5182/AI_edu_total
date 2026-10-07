#!/usr/bin/env python3
"""Build a question-free dashboard, individual cards, and historical weekly records.

Standard library only. Run: python build_dashboard.py
Source: ../../knowledge/cards.json. Outputs: index.html and knowledge/cards, weekly.
"""
import collections, datetime, html, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
KNOWLEDGE = HERE.parent.parent / 'knowledge'
STATUSES = ['공식확인', '부분확인', '커뮤니티경험', '정정', '미확인']

def main():
    cards = json.loads((KNOWLEDGE / 'cards.json').read_text(encoding='utf-8'))
    ids = set()
    for c in cards:
        assert c['id'] not in ids, 'Duplicate ID'
        ids.add(c['id'])
        assert c['status'] in STATUSES, 'Unknown status'
        assert all(k in c for k in ['knowledge', 'correction', 'lesson', 'checked_on', 'first_date', 'last_date'])
        for key in ['first_date', 'last_date']:
            datetime.date.fromisoformat(c[key])
        assert not ({'asker', 'q', 'a', 'source_qids', 'room', 'community_answer', 'situation'} & c.keys()), 'Private schema rejected'
        assert c['status'] != '공식확인' or c['official_links'], 'Official source missing'
        assert c['status'] != '정정' or c['correction'], 'Correction missing'
        for link in c['official_links'] + c['ref_links']:
            assert link['url'].startswith(('https://', 'http://')), 'Only web source URLs allowed'
    output = KNOWLEDGE / 'cards'
    output.mkdir(exist_ok=True)
    for c in cards:
        lines = [f'# {c["title"]}', '', '> 역사 자료. 확인 수준과 확인일은 원본 기록을 보존한 값입니다. 공개 편집일의 최신 기능·가격·법률 확인을 의미하지 않습니다.', '', f'- 카드: {c["id"]}', f'- 분류: {c["category"]}', f'- 기록 기간: {c["first_date"]} ~ {c["last_date"]}', f'- 원본 확인일: {c["checked_on"] or "미기록"}', f'- 원본 상태: **{c["status"]}**', '- 공개 편집일: 2026-10-08', '', '## 정리된 지식', '', c['knowledge'], '', '## 교육과 업무에 활용', '', c['lesson']]
        if c['correction']: lines += ['', '## 정정과 한계', '', c['correction']]
        lines += ['', '## 출처', '']
        for links, kind in [(c['official_links'], '원본의 공식 근거'), (c['ref_links'], '보도·외부 참고')]:
            for link in links: lines.append(f'- {kind}: [{link.get("title", "출처")}](<{link["url"]}>)')
        if not c['official_links'] and not c['ref_links']: lines.append('공개 외부 출처 없음. 원본의 경험·관점 요약을 보존했으며 사실 또는 효과의 입증으로 취급하지 않습니다.')
        lines += ['', c['evidence_note'], '', '[전체 주제 목록](../topics.md)']
        (output / (c['id'] + '.md')).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    weekly = KNOWLEDGE / 'weekly'
    weekly.mkdir(exist_ok=True)
    weeks = sorted({w for c in cards for w in c['weeks']})
    for week in weeks:
        selected = [c for c in cards if week in c['weeks']]
        lines = [f'# {week} 지식 기록', '', '주차는 기록의 등장 시점입니다. 출시일이나 새 검증일을 뜻하지 않습니다. 원본 대화와 질문자는 공개하지 않습니다.', '', '| 지식 | 원본 상태 | 원본 확인일 |', '|---|---|---|']
        for c in selected: lines.append(f'| [{c["title"].replace("|", "／")}](../cards/{c["id"]}.md) | {c["status"]} | {c["checked_on"] or "미기록"} |')
        (weekly / (week + '.md')).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    blob = json.dumps(cards, ensure_ascii=False).replace('</', '<\\/')
    template = (HERE / 'template.html').read_text(encoding='utf-8')
    assert template.count('/*__DATA__*/') == 1
    (HERE / 'index.html').write_text(template.replace('/*__DATA__*/', 'const CARDS = ' + blob + ';'), encoding='utf-8')
    print(json.dumps({'cards': len(cards), 'weekly': len(weeks), 'status_counts': dict(collections.Counter(c['status'] for c in cards)), 'output': 'index.html'}, ensure_ascii=False))

if __name__ == '__main__': main()
