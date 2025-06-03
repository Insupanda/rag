import re
from typing import Optional

from options.enums import ProductType, Sex, product_type_mapping_table, sex_mapping_table

EXPIRY = int
DURATION = int


class UserState:
    def __init__(self):
        self.custom_name: str = "홍길동"
        self.insu_age: int = 25
        self.insu_sex: Sex = Sex.MALE
        self.product_type: ProductType = ProductType.NON_REFUND
        self.expiry: int = 20
        self.duration: int = 100

    def __repr__(self) -> str:
        sex = "남자" if self.insu_sex == Sex.MALE else "여자"
        product_type = "무해지형" if self.product_type == ProductType.NON_REFUND else "해지환급형"
        return (
            "\n=== 실행 결과 ===\n"
            "\n[설정값]\n"
            f"이름: {self.custom_name}\n"
            f"나이: {self.insu_age}세\n"
            f"성별: {sex}\n"
            f"상품유형: {product_type}\n"
            f"보험기간: {self.expiry_year}"
        )

    @property
    def display_insu_sex(self) -> str:
        return sex_mapping_table[Sex.MALE] if self.insu_sex == Sex.MALE else sex_mapping_table[Sex.FEMALE]

    @property
    def display_product_type(self) -> str:
        return (
            product_type_mapping_table[ProductType.NON_REFUND]
            if self.product_type == ProductType.NON_REFUND
            else product_type_mapping_table[ProductType.REFUND]
        )

    @property
    def expiry_year(self) -> str:
        return f"{self.expiry}y_{self.duration}"

    @classmethod
    def extract_age(cls, user_input: str) -> Optional[int]:
        age_match = re.search(r"(\d+)세", user_input)
        if age_match:
            return int(age_match.group(1))

    @classmethod
    def extract_sex(cls, user_input: str) -> Optional[Sex]:
        if re.search(r"(남성|남자)", user_input):
            return Sex.MALE
        if re.search(r"(여성|여자)", user_input):
            return Sex.FEMALE

    @classmethod
    def extract_product_type(cls, user_input: str) -> Optional[ProductType]:
        if product_type_mapping_table[ProductType.NON_REFUND] in user_input:
            return ProductType.NON_REFUND
        if product_type_mapping_table[ProductType.REFUND] in user_input:
            return ProductType.REFUND

    @classmethod
    def extract_expiry_and_duration(cls, user_input: str) -> tuple[EXPIRY, DURATION]:
        period_match = re.search(r"(\d+)년[/\s](\d+)세", user_input)
        if period_match:
            expiry: EXPIRY = period_match.group(1)
            duration: DURATION = period_match.group(2)
            return expiry, duration

    def update_by_user_input(self, user_input: str) -> None:
        self.insu_age = UserState.extract_age(user_input)
        self.insu_sex = UserState.extract_sex(user_input)
        self.product_type = UserState.extract_product_type(user_input)
        self.expiry, self.duration = UserState.extract_expiry_and_duration(user_input)


user_state = UserState()
