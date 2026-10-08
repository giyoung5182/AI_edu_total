# 이미지 스타일 스킬: 원문 코드와 활용 요약

정리일: 2026-10-08. 출처: [freestylefly/awesome-gpt-image-2](https://github.com/freestylefly/awesome-gpt-image-2/tree/65a9c57a1968a13f2f1997c58409cac9aa146bc7). 당시 `main` HEAD는 `65a9c57a1968a13f2f1997c58409cac9aa146bc7`입니다.

이미지를 만들기 전에 목표 유형·구도·글자·재질·비율·실패 조건을 정리하는 스킬입니다. 이미지 생성 엔진이나 API 서버가 아닙니다. 한국어로 원하는 결과와 준비한 자료를 설명하고, 적합한 시각 유형을 고른 뒤 제작 요청문과 검수 항목을 구성하는 데 활용할 수 있습니다.

## 보존한 원문

- [SKILL.md](upstream/agents/skills/gpt-image-2-style-library/SKILL.md): 선택·구성·출력 절차.
- [설치 코드](upstream/agents/skills/gpt-image-2-style-library/bin/install.mjs): Node 기본 모듈을 이용한 복사 설치.
- [package.json](upstream/agents/skills/gpt-image-2-style-library/package.json), [에이전트 메타데이터](upstream/agents/skills/gpt-image-2-style-library/agents/openai.yaml).
- [원 MIT 라이선스](upstream/LICENSE), [파일 대조표](source-manifest.json).

## 제외와 실행 경계

원 저장소는 MIT 코드와 함께 커뮤니티 프롬프트·이미지를 모읍니다. [원문 권리 안내](https://github.com/freestylefly/awesome-gpt-image-2/blob/65a9c57a1968a13f2f1997c58409cac9aa146bc7/docs/disclaimer.md)는 해당 콘텐츠의 권리가 원저자·플랫폼에 있으며 개별 조건을 따라야 한다고 밝힙니다. 따라서 22개 템플릿의 프롬프트 본문, 사례 DB 전체, 생성 이미지, 데모 그림, 웹 서비스·결제 코드는 포함하지 않았습니다. [새 선택 요약](references/style-selection-summary.md)은 이름·분류와 새로 작성한 질문으로 구성했습니다.

원본 스킬이 요구하는 `references/style-library.md`와 `assets/city-life-system-map.png`는 빠져 있습니다. 그대로 설치해 정상 작동한다고 확인한 패키지가 아닙니다. 원문 링크를 살리려고 저작권이 불분명한 파일을 채워 넣거나 원문 지침을 수정하지 않았습니다.

설치 스크립트는 `SKILL.md / agents / assets / references`를 모두 요구하며, 선택한 전역 스킬 폴더를 삭제한 뒤 복사합니다. `assets`와 `references`가 없는 이번 소스 보존본에서는 실행할 수 없습니다. 이 코드의 동작을 이해하기 위한 보존이지 실행 권고가 아닙니다. 원문의 `npm run generate:style-skill`은 저장소 루트의 생성 도구·데이터가 필요합니다.

원 패키지 버전은 1.0.4이며 설치 코드는 Node.js 기본 모듈만 사용합니다. 별도 npm 의존성이 선언돼 있지 않지만 패키지 파일이 빠져 있는 이번 보존본은 완전 설치본이 아닙니다.

글꼴·이미지·생성 모델·계정·현재 요금·플랫폼 연동은 별도 조건입니다. 이번 작업은 원문 코드·라이선스·경로·해시를 확인했으며 설치나 이미지 생성 API를 실행하지 않았습니다.
