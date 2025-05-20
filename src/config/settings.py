import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from options.enums import ProductType, Sex

load_dotenv()
PROJECT_ROOT = Path(__file__).parent.parent.resolve()


@dataclass
class UserState:
    custom_name: str = "홍길동"
    insu_age: int = 25
    insu_sex: Sex = Sex.MALE
    product_type: ProductType = ProductType.NON_REFUND
    expiry_year: str = "20y_100"
    expiry: int = 20
    duration: int = 100

    def __repr__(self) -> str:
        gender = "남자" if self.insu_sex == Sex.MALE else "여자"
        product_type = "무해지형" if self.product_type == ProductType.NON_REFUND else "해지환급형"
        return (
            "\n=== 실행 결과 ===\n"
            "\n[설정값]\n"
            f"이름: {self.custom_name}\n"
            f"나이: {self.insu_age}세\n"
            f"성별: {gender}\n"
            f"상품유형: {product_type}\n"
            f"보험기간: {self.expiry_year}"
        )


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: str = "3306"
    db_user: str = "root"
    db_password: str = os.environ["DB_PASSWORD"]
    db_database: str = "insu"

    vector_path: str = "insu_data"
    openai_client: str = os.environ["OPENAI_API_KEY"]
    upstage_api_key: str = os.environ["UPSTAGE_API_KEY"]


settings = Settings()
user_state = UserState()
