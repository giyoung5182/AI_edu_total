# Jev Ultrafast 원문 소스와 교육 연결

정리일 2026-10-08 · [원 제작 저장소](https://github.com/browser-use/jev-ultrafast) · MIT.

## 무엇을 가져왔나요?

공식 저장소의 추적 파일을 `upstream/`에 원문 그대로 보존했습니다. [출처·고정 버전·파일 해시](source-manifest.json) · [원문 README](upstream/README.md) · [라이선스](upstream/LICENSE) · [핵심 루프](upstream/jev_ultrafast/agent.py) · [오프라인 테스트](upstream/tests/test_agent.py).

핵심은 페이지 관찰→번호가 붙은 요소 목록→행동·대상 선택→실행→다시 관찰입니다. 같은 입력에서 행동과 대상 질문을 함께 받고, 선택한 행동의 대상만 사용합니다. 글자를 입력할 때만 보조 언어 모델을 호출합니다. 오래된 페이지나 가려진 요소는 실행 전 다시 확인하며, DONE 응답과 실제 목표 달성은 별개로 검사합니다.

## 읽는 순서

1. README에서 목표와 범위를 봅니다.
2. questions.py와 model.py에서 판단 질문·허용 행동·텍스트 보조 모델 연결을 읽습니다.
3. agent.py와 browser.py에서 상태·재시도·실행·종료 조건을 읽습니다.
4. tests/test_agent.py에서 잘못된 선택·오래된 상태·중복 실행을 어떻게 막는지 확인합니다.
5. docs/performance.md의 측정 범위와 실패를 읽고 자신의 실습에 검수표를 붙입니다.

## 사용 조건과 확인 범위

이 묶음은 자료와 코드를 저장소에 정리한 것입니다. Python3.12 이상·browser-harness·HTTP 라이브러리와 Chrome 연결이 필요하고, 실제 AI 실행은 TypeSafe 및 텍스트 보조 모델 계정·키·비용 조건을 따릅니다. `.env.example`의 키는 빈칸이며 실제 자격증명을 포함하지 않습니다.

원문 README의 설치·실행 명령은 참고 설명입니다. 이번 작업에서 의존 설치·계정 연결·API 호출·원격 브라우저 작업을 실행하지 않았습니다. 원 제작자의 데모·성능 기록은 본 작업의 실행 성과가 아닙니다. 포함된 시연 이미지·영상은 MIT 공개 프로젝트의 원 자산이며 가상 수강생 실습 결과와 구분합니다.

[교육용 자료 분류 절차](../../methods/source-classification-workflow.md)와 연결해 요약 담당·판단 담당·실행 담당의 역할을 설명할 수 있습니다.
