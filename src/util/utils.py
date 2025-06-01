import copy
import re

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

from config.settings import UserState, settings
from options.enums import ModelType, ProductType, Sex, product_type_mapping_table
from options.insu_name import insu_match

InsuCompanyName = str
InsuKeywords = list[str]
InsuFileName = str
CANCER = "암"


class QueryInfoExtract:
    def __init__(self, user_input: str, user_state: UserState):
        self.user_input = user_input
        self.current_state = copy.copy(user_state)

    def extract_age(self) -> None:
        age_match = re.search(r"(\d+)세", self.user_input)
        if age_match:
            self.current_state.insu_age = int(age_match.group(1))

    def extract_sex(self) -> None:
        if re.search(r"(남성|남자)", self.user_input):
            self.current_state.insu_sex = Sex.MALE
        elif re.search(r"(여성|여자)", self.user_input):
            self.current_state.insu_sex = Sex.FEMALE

    def extract_product_type(self) -> None:
        if product_type_mapping_table[ProductType.NON_REFUND] in self.user_input:
            self.current_state.product_type = ProductType.NON_REFUND
        elif product_type_mapping_table[ProductType.REFUND] in self.user_input:
            self.current_state.product_type = ProductType.REFUND

    def extract_insu_period(self) -> None:
        period_match = re.search(r"(\d+)년[/\s](\d+)세", self.user_input)
        if period_match:
            years = period_match.group(1)
            age = period_match.group(2)
            self.current_state.expiry_year = f"{years}y_{age}"

    def process(self) -> tuple[str, UserState]:
        self.extract_age()
        self.extract_sex()
        self.extract_product_type()
        self.extract_insu_period()
        return self.user_input, self.current_state


def insurance_keywords_mapping() -> dict[InsuCompanyName, InsuKeywords]:
    insu_filename = insu_match.values()
    gpt4o = ChatOpenAI(model_name=ModelType.KEYWORD_MODEL, temperature=0.1, api_key=settings.openai_api_key)

    keyword_chain_template = PromptTemplate.from_template(
        """
    {insu_filename}를 참고해서 각 키워드마다 해당하는 패턴을 value로 채워주세요.
    반드시 value는 영어약자가 포함됩니다. key는 반드시 한글로 출력하세요.
    영어약자는 {insu_filename}에서 _기준으로 앞부분을 참고하세요.
    반환 형태를 key: value 형식인 JSON 형식으로 출력하세요.

    "NH농협손해보험": ["NH농협손해보험", "NH손해보험", "농협손해보험", "NH손보", "농협손보", "NH", "농협"],
    "DB손해보험": ["db손해보험", "db손해", "db보험", "db", "디비손해보험", "디비"],
    {keywords}:
    """.strip()
    )

    result = keyword_chain_template | gpt4o | JsonOutputParser()
    mapping_dict = result.invoke(
        {"insu_filename": insu_filename, "keywords": lambda obj: [print(k) for k in obj.__dict__.keys()]}
    )
    return mapping_dict


def find_detected_keywords(user_input: str) -> tuple[list[InsuCompanyName], bool, list[str]]:
    insurance_company_keywords = insurance_keywords_mapping()
    insurance_type_keywords = ["암", "상해", "질병", "재물", "화재", "운전자", "자동차", "실손"]
    comparison_keywords = ["비교", "차이", "다른", "다른점", "비교해", "비교해줘", "차이점", "알려줘", "뭐가 더 나은가"]

    mentioned_companies: list[InsuCompanyName] = []
    for company, keywords in insurance_company_keywords.items():
        if re.search("|".join(keywords), user_input):
            mentioned_companies.append(company)

    is_comparison_module = re.search("|".join(comparison_keywords), user_input) is not None
    detected_insurance_types = [keyword for keyword in insurance_type_keywords if keyword in user_input]

    if detected_insurance_types:
        print(f"보험 종류 키워드 감지: {detected_insurance_types}")

    return mentioned_companies, is_comparison_module, detected_insurance_types


def find_matching_collections(user_input: str, available_collections: list[InsuFileName]) -> list[InsuFileName]:
    """
    사용자 질문에서 보험사 관련 키워드를 검출하여 일치하는 컬렉션 이름 목록 반환
    비교 질문인 경우 관련된 모든 보험사 컬렉션 반환
    """
    if not user_input or not available_collections:
        print("질문이 비어있거나 사용 가능한 컬렉션이 없음")
        print("-------- 컬렉션 매칭 실패 --------\n")
        raise ValueError("질문이 없거나 사용 가능한 컬렉션이 없습니다.")

    normalized_question = user_input.lower().replace(" ", "")

    mentioned_companies, is_comparison_module, detected_insurance_types = find_detected_keywords(normalized_question)

    # 두 개 이상 보험사가 언급되었거나 비교 요청이 있는 경우
    # '암' 키워드가 언급된 경우에도 모든 보험사 정보가 필요할 수 있음
    matched_collections: set[InsuFileName] = set()
    if len(mentioned_companies) > 1 or is_comparison_module or CANCER in detected_insurance_types:
        # 모든 보험사 컬렉션 추가
        matched_collections.update(list(insu_match.values()))
    else:
        for insu_company in mentioned_companies:
            if insu_company in insu_match:
                matched_collections.add(insu_match[insu_company])
        if len(mentioned_companies) == 0:
            matched_collections.update(list(insu_match.values()))

    # 중복 제거
    matched_collections: list[str] = list(matched_collections)

    print(f"최종 매칭된 컬렉션: {matched_collections}")
    print("-------- 컬렉션 매칭 완료 --------\n")

    return matched_collections
