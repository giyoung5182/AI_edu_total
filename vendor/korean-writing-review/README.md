# 한글 글쓰기 검토 스킬과 지원 코드

정리일: 2026-10-08. 출처: [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai/tree/2f3d943d08056b612a92e12bfb72ea94dd2acd18). 당시 `main` HEAD는 `2f3d943d08056b612a92e12bfb72ea94dd2acd18`입니다.

번역투·기계적 병렬 구조 등 한글 문체 문제를 진단하고, 원문 의미를 유지하며 고친 뒤 변경률·보존 조건을 검토하는 스킬입니다. AI 작성 여부를 확정하거나 탐지기 우회를 보증하는 도구가 아닙니다. 원저자 README는 코드·스킬·에이전트 정의·분류 문서에 MIT가 적용된다고 명시합니다. [원 라이선스](upstream/LICENSE)를 함께 보존했습니다.

## 준비할 입력과 흐름

검토할 한국어 원문이 준비됐다면 독자·장르·유지할 의미·숫자·고유명사를 설명합니다. 원문을 별도로 보존하고 문체 진단 → 제한된 수정 → 결정적 게이트 → 사람 검토로 진행합니다. 수치가 경고를 표시하면 의미·문체를 다시 확인합니다. 변경률이 낮거나 높다는 사실만으로 좋은 글이라고 판정하지 않습니다.

[원문 사용 안내](upstream/README.md), [원 Codex 스킬](upstream/codex/skills/humanize-korean/SKILL.md), [한국어 규칙](upstream/skills/humanize-korean/references/quick-rules.md), [스크립트](upstream/scripts/verify_gates.py), [테스트](upstream/tests/test_verify_gates.py), [파일 대조표](source-manifest.json)를 함께 읽을 수 있습니다.

## 경로 보존과 지역 패키지

`upstream/`에는 Git 추적 텍스트를 원문 바이트로 보존했습니다. 이미지·`.git`·실제 인증·개인 설정은 넣지 않았습니다. `install.sh / update.sh / uninstall.sh / .githooks`는 읽기용 원문으로 보존했으며 실행·등록하지 않았습니다. upstream의 CLAUDE.md·GEMINI.md·역할 정의도 참고 원문입니다.

원 Codex 패키지의 `references`는 Git 심볼릭 링크입니다. 이 보존본의 해당 파일은 원래 링크 대상 문자열을 담는 일반 텍스트 파일입니다. Windows에서 그대로 읽으면 디렉터리처럼 작동하지 않습니다. 원 wrapper 4개는 개발 저장소의 `parents[4]/scripts`를 호출하며, upstream 구조를 통째로 유지한 경우에만 경로가 맞습니다.

[local-skill/SKILL.md](local-skill/SKILL.md)는 전역에 설치하지 않은 지역 패키징 사본입니다. 공유 reference를 일반 파일로 복사하고, wrapper 4개가 이 vendor 폴더의 `upstream/scripts`를 가리키도록 경로만 조정했습니다. 원본 파일은 바꾸지 않았습니다. 이 지역 사본의 추가 안내는 upstream 원문이 아닙니다. 설치 준비가 됐다는 사실과 실제 윤문 결과가 검증됐다는 사실은 구분해야 합니다.

## 의존성과 확인 수준

Python 스크립트·규칙·테스트 파일을 포함했습니다. upstream CI는 핵심 런타임이 표준 라이브러리 기반이고 테스트 의존성은 pytest라고 밝힙니다. 미리보기 생성 스크립트의 Pillow(PIL)는 선택 기능이며 실제 미리보기 제작은 하지 않았습니다. 스킬의 진단·윤문·최종 판정은 이용하는 에이전트 실행 환경이 필요합니다. 플랫폼별 플러그인·슬래시 명령·모델 호출 지원은 별도이며, 문서에 있는 모델 이름을 설치나 실행 설정으로 활성화하지 않았습니다. 선택 기능과 이미지 미리보기 제작에는 추가 패키지가 필요할 수 있습니다.

이번 검증은 고정 커밋, MIT 원문, 파일 해시·재열기, Python 구문, 지역 wrapper의 대상 경로입니다. 설치·hooks·자동 에이전트·외부 API·실제 글 윤문·전체 테스트 실행을 완료했다고 주장하지 않습니다. 회귀 테스트를 새로 실행할 때는 설치·외부 호출·LIVE 환경을 요구하는 테스트와 로컬 계산 테스트를 먼저 구분해야 합니다.
