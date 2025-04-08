import re

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_client = OpenAI()


def process_query(prompt: str, config):
    # 현재 사용되는 설정값 저장
    current_config = config.copy()

    # 나이 추출 (숫자 + "세" 패턴)
    age_match = re.search(r"(\d+)세", prompt)
    if age_match:
        current_config["insu_age"] = int(age_match.group(1))

    # 성별 추출
    if "남성" in prompt or "남자" in prompt:
        current_config["sex"] = 1
    elif "여성" in prompt or "여자" in prompt:
        current_config["sex"] = 0

    # 상품유형 추출
    if "무해지" in prompt:
        current_config["product_type"] = "nr"
    elif "해지환급" in prompt:
        current_config["product_type"] = "r"

    # 보험기간 추출
    period_match = re.search(r"(\d+)년[/\s](\d+)세", prompt)
    if period_match:
        years = period_match.group(1)
        age = period_match.group(2)
        current_config["expiry_year"] = f"{years}y_{age}"

    # 보험사 추출 (옵션)
    if "삼성" in prompt:
        current_config["company_id"] = "01"
    elif "한화" in prompt:
        current_config["company_id"] = "02"
    # 다른 보험사들에 대한 매핑도 추가 가능

    return prompt, current_config


def find_matching_collections(question, available_collections):
    """
    사용자 질문에서 보험사 관련 키워드를 검출하여 일치하는 컬렉션 이름 목록 반환
    비교 질문인 경우 관련된 모든 보험사 컬렉션 반환
    """
    print(f"\n-------- 컬렉션 매칭 시작 --------")
    print(f"질문: '{question}'")
    print(f"사용 가능한 컬렉션: {available_collections}")

    if not question or not available_collections:
        print(f"질문이 비어있거나 사용 가능한 컬렉션이 없음")
        print("-------- 컬렉션 매칭 실패 --------\n")
        return []

    # 정규화된 질문 (소문자, 공백 제거)
    normalized_question = question.lower().replace(" ", "")

    # 보험사 키워드 매핑
    insurance_company_keywords = {
        "삼성화재": ["삼성화재", "삼성", "samsung"],
        "DB손해보험": [
            "db손해보험",
            "db손해",
            "db보험",
            "db",
            "디비손해보험",
            "디비",
        ],
        "하나손해보험": ["하나손해보험", "하나손보", "하나", "hana"],
        "한화손해보험": ["한화손해보험", "한화손보", "한화", "hanwha"],
        "흥국화재": ["흥국화재", "흥국", "heung", "흥국생명"],
        "현대해상": ["현대해상", "현대", "hyundai"],
        "KB손해보험": ["KB손해보험", "KB손보", "KB", "케이비"],
        "롯데손해보험": ["롯데손해보험", "롯데손보", "롯데", "lotte"],
        "MG손해보험": ["MG손해보험", "MG손보", "MG", "엠지"],
        "메리츠화재": ["메리츠화재", "메리츠", "meritz"],
        "NH농협손해보험": [
            "NH농협손해보험",
            "NH손해보험",
            "농협손해보험",
            "NH손보",
            "농협손보",
            "NH",
            "농협",
        ],
    }

    # 보험 종류 키워드
    insurance_type_keywords = [
        "암",
        "상해",
        "질병",
        "재물",
        "화재",
        "운전자",
        "자동차",
        "실손",
    ]

    # 비교 요청 키워드
    comparison_keywords = [
        "비교",
        "차이",
        "다른",
        "다른점",
        "비교해",
        "비교해줘",
        "차이점",
        "알려줘",
        "뭐가 더 나은가",
    ]

    # 언급된 보험사 추적
    mentioned_companies = []
    for company, keywords in insurance_company_keywords.items():
        if any(keyword in normalized_question for keyword in keywords):
            mentioned_companies.append(company)
            print(f"보험사 키워드 감지: {company}")

    # 비교 요청 감지
    is_comparison_request = any(
        keyword in normalized_question for keyword in comparison_keywords
    )
    if is_comparison_request:
        detected_keywords = [
            keyword for keyword in comparison_keywords if keyword in normalized_question
        ]
        print(f"비교 키워드 감지: {detected_keywords}")

    # 보험 종류 키워드 감지
    detected_insurance_types = [
        keyword for keyword in insurance_type_keywords if keyword in normalized_question
    ]
    if detected_insurance_types:
        print(f"보험 종류 키워드 감지: {detected_insurance_types}")

    # 컬렉션 매칭 로직
    matched_collections = []

    # 두 개 이상 보험사가 언급되었거나 비교 요청이 있는 경우
    # '암' 키워드가 언급된 경우에도 모든 보험사 정보가 필요할 수 있음
    if (
        len(mentioned_companies) > 1
        or is_comparison_request
        or "암" in detected_insurance_types
    ):
        print(f"다중 보험사 비교 또는 암 관련 질문 감지됨")
        # 모든 보험사 컬렉션 추가
        for collection in available_collections:
            is_relevant = False

            # 삼성화재 컬렉션 매칭
            if "samsung" in collection.lower() or "삼성" in collection:
                matched_collections.append(collection)
                is_relevant = True
                print(f"삼성화재 컬렉션 매칭: {collection}")

            # DB손해보험 컬렉션 매칭
            elif (
                "db" in collection.lower()
                or "디비" in collection
                or "sonbo" in collection.lower()
            ):
                matched_collections.append(collection)
                is_relevant = True
                print(f"DB손해보험 컬렉션 매칭: {collection}")

            # 하나손해보험 컬렉션 매칭
            elif (
                "hana" in collection.lower()
                or "하나" in collection
                or "ha" in collection.lower()
            ):
                matched_collections.append(collection)
                is_relevant = True
                print(f"하나손해보험 컬렉션 매칭: {collection}")

            # 한화손해보험 컬렉션 매칭
            elif (
                "hanwha" in collection.lower()
                or "한화" in collection
                or "hw" in collection.lower()
            ):
                matched_collections.append(collection)
                is_relevant = True
                print(f"한화손해보험 컬렉션 매칭: {collection}")

            # 흥국화재 컬렉션 매칭
            elif (
                "heung" in collection.lower()
                or "흥국" in collection
                or "hg" in collection.lower()
            ):
                matched_collections.append(collection)
                is_relevant = True
                print(f"흥국화재 컬렉션 매칭: {collection}")

            # 현대해상 컬렉션 매칭
            elif (
                "hyundai" in collection.lower()
                or "현대" in collection
                or "hd" in collection.lower()
            ):
                matched_collections.append(collection)
                is_relevant = True
                print(f"현대해상 컬렉션 매칭: {collection}")

            # KB손해보험 컬렉션 매칭
            elif (
                "kb" in collection.lower()
                or "KB" in collection
                or "케이비" in collection
            ):
                matched_collections.append(collection)
                is_relevant = True
                print(f"KB손해보험 컬렉션 매칭: {collection}")

            # 롯데손해보험 컬렉션 매칭
            elif (
                "lotte" in collection.lower()
                or "롯데" in collection
                or "lt" in collection.lower()
            ):
                matched_collections.append(collection)
                is_relevant = True
                print(f"롯데손해보험 컬렉션 매칭: {collection}")

            # MG손해보험 컬렉션 매칭
            elif (
                "mg" in collection.lower() or "MG" in collection or "엠지" in collection
            ):
                matched_collections.append(collection)
                is_relevant = True
                print(f"MG손해보험 컬렉션 매칭: {collection}")

            # 메리츠화재 컬렉션 매칭
            elif (
                "meritz" in collection.lower()
                or "메리츠" in collection
                or "mz" in collection.lower()
            ):
                matched_collections.append(collection)
                is_relevant = True
                print(f"메리츠화재 컬렉션 매칭: {collection}")

            # NH농협손해보험 컬렉션 매칭
            elif (
                "nh" in collection.lower() or "NH" in collection or "농협" in collection
            ):
                matched_collections.append(collection)
                is_relevant = True
                print(f"NH농협손해보험 컬렉션 매칭: {collection}")

            if not is_relevant and len(mentioned_companies) == 0:
                # 특정 보험사가 언급되지 않은 경우 모든 컬렉션 추가
                matched_collections.append(collection)
                print(f"기본 컬렉션 매칭: {collection}")
    else:
        # 단일 보험사만 언급된 경우
        for collection in available_collections:
            if "삼성화재" in mentioned_companies and (
                "samsung" in collection.lower() or "삼성" in collection
            ):
                matched_collections.append(collection)
                print(f"삼성화재 컬렉션 매칭: {collection}")

            elif "DB손해보험" in mentioned_companies and (
                "db" in collection.lower()
                or "디비" in collection
                or "sonbo" in collection.lower()
            ):
                matched_collections.append(collection)
                print(f"DB손해보험 컬렉션 매칭: {collection}")

            elif "하나손해보험" in mentioned_companies and (
                "hana" in collection.lower()
                or "하나" in collection
                or "ha" in collection.lower()
            ):
                matched_collections.append(collection)
                print(f"하나손해보험 컬렉션 매칭: {collection}")

            elif "한화손해보험" in mentioned_companies and (
                "hanwha" in collection.lower()
                or "한화" in collection
                or "hw" in collection.lower()
            ):
                matched_collections.append(collection)
                print(f"한화손해보험 컬렉션 매칭: {collection}")

            elif "흥국화재" in mentioned_companies and (
                "heung" in collection.lower()
                or "흥국" in collection
                or "hg" in collection.lower()
            ):
                matched_collections.append(collection)
                print(f"흥국화재 컬렉션 매칭: {collection}")

            elif "현대해상" in mentioned_companies and (
                "hyundai" in collection.lower()
                or "현대" in collection
                or "hd" in collection.lower()
            ):
                matched_collections.append(collection)
                print(f"현대해상 컬렉션 매칭: {collection}")

            elif "KB손해보험" in mentioned_companies and (
                "kb" in collection.lower()
                or "KB" in collection
                or "케이비" in collection
            ):
                matched_collections.append(collection)
                print(f"KB손해보험 컬렉션 매칭: {collection}")

            elif "롯데손해보험" in mentioned_companies and (
                "lotte" in collection.lower()
                or "롯데" in collection
                or "lt" in collection.lower()
            ):
                matched_collections.append(collection)
                print(f"롯데손해보험 컬렉션 매칭: {collection}")

            elif "MG손해보험" in mentioned_companies and (
                "mg" in collection.lower() or "MG" in collection or "엠지" in collection
            ):
                matched_collections.append(collection)
                print(f"MG손해보험 컬렉션 매칭: {collection}")

            elif "메리츠화재" in mentioned_companies and (
                "meritz" in collection.lower()
                or "메리츠" in collection
                or "mz" in collection.lower()
            ):
                matched_collections.append(collection)
                print(f"메리츠화재 컬렉션 매칭: {collection}")

            elif "NH농협손해보험" in mentioned_companies and (
                "nh" in collection.lower() or "NH" in collection or "농협" in collection
            ):
                matched_collections.append(collection)
                print(f"NH농협손해보험 컬렉션 매칭: {collection}")

            # 보험사가 언급되지 않은 경우 모든 컬렉션 추가
            elif len(mentioned_companies) == 0:
                matched_collections.append(collection)
                print(f"기본 컬렉션 매칭: {collection}")

    # 중복 제거
    matched_collections = list(set(matched_collections))

    print(f"최종 매칭된 컬렉션: {matched_collections}")
    print(f"-------- 컬렉션 매칭 완료 --------\n")

    return matched_collections
