"""교육용 견적 기준 v1. Python 표준 라이브러리만 사용. 실제 회사 정책 검증 아님."""
from pathlib import Path
from decimal import Decimal,InvalidOperation
import csv,json,argparse

HEADERS=['유형','항목','수량','단가','개월','참여율','근거']
def inspect(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if reader.fieldnames!=HEADERS:raise ValueError('CSV 열 순서가 기준과 다릅니다: '+','.join(HEADERS))
        rows=list(reader)
    issues=[];seen=set();amounts=[]
    for rowno,row in enumerate(rows,2):
        before=len(issues)
        def add(field,msg):issues.append({'csv_line':rowno,'field':field,'issue':msg})
        if row.get('유형') not in ['인건비','외주','경비']:add('유형','지원하지 않는 유형')
        if not (row.get('항목') or '').strip():add('항목','항목 누락')
        if not (row.get('근거') or '').strip():add('근거','근거 누락·담당자 확인 필요')
        key=(row.get('유형'),row.get('항목'))
        if key in seen:add('항목','같은 유형·항목의 중복 의심·자동 삭제 금지')
        seen.add(key);values={}
        for field in ['수량','단가','개월','참여율']:
            try:
                value=Decimal(row.get(field) or '')
                if not value.is_finite():raise InvalidOperation()
                values[field]=value
            except (InvalidOperation,ValueError):add(field,'유효한 숫자가 아님')
        for field in ['수량','단가']:
            if field in values and values[field]<=0:add(field,'0보다 커야 함')
        if row.get('유형')=='인건비':
            if '개월' in values and values['개월']<=0:add('개월','0보다 커야 함')
            if '참여율' in values and not Decimal(0)<values['참여율']<=Decimal(1):add('참여율','0보다 크고 1 이하여야 함')
        if len(issues)==before:
            cost=values['수량']*values['단가']
            if row['유형']=='인건비':cost*=values['개월']*values['참여율']
            amounts.append({'csv_line':rowno,'item':row['항목'],'amount':str(cost)})
    base=sum((Decimal(x['amount']) for x in amounts),Decimal(0))
    fee=base*Decimal('.1');subtotal=base+fee;vat=subtotal*Decimal('.1');total=subtotal+vat
    return {'criteria':'교육용 검수기준 v1·2026-10-07','source':Path(path).name,'rows':len(rows),'issues':issues,'status':'보류' if issues else '기본 규칙 통과','calculation_is_final':not bool(issues),'valid_rows':amounts,'direct_cost':str(base),'fee':str(fee),'subtotal':str(subtotal),'vat':str(vat),'total':str(total),'budget':13000000,'budget_remaining':str(Decimal(13000000)-total),'meaning_review':'제작 범위·단가 현실성·증빙 여부는 AI 검토와 사람 확인이 필요함'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('csv');parser.add_argument('--out');args=parser.parse_args()
    try:
        result=inspect(args.csv)
        payload=json.dumps(result,ensure_ascii=False,indent=2)
        if args.out:
            target=Path(args.out)
            if target.resolve()==Path(args.csv).resolve():raise ValueError('원본 CSV를 출력 위치로 지정할 수 없습니다.')
            target.parent.mkdir(parents=True,exist_ok=True);target.write_text(payload,encoding='utf-8')
        print(payload)
        raise SystemExit(2 if result['issues'] else 0)
    except (OSError,ValueError,csv.Error) as e:
        print(json.dumps({'status':'입력 오류','reason':str(e)},ensure_ascii=False));raise SystemExit(1)
