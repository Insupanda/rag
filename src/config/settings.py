import os
from pathlib import Path

from options.enums import Sex, ProductType

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import BaseModel


load_dotenv()
PROJECT_ROOT = Path(__file__).parent.parent.resolve()


class UserState:
    def __init__(
        self,
        custom_name: str = "홍길동",
        insu_age: int = 25,
        insu_sex: Sex = Sex.MALE,
        product_type: ProductType = ProductType.NON_REFUND,
        expiry_year: str = "20y_100",
        expiry: int = 20,
        duration: int = 100,
    ):
        self.custom_name = custom_name
        self.insu_age = insu_age
        self.insu_sex = insu_sex
        self.product_type = product_type
        self.expiry_year = expiry_year
        self.expiry = expiry
        self.duration = duration

    @property
    def custom_name(self):
        return self.__custom_name

    @custom_name.setter
    def custom_name(self, user_name: str = "홍길동"):
        self.__custom_name = user_name

    @property
    def insu_age(self):
        return self.__insu_age

    @insu_age.setter
    def insu_age(self, user_age: int = 25):
        self.__insu_age = user_age

    @property
    def insu_sex(self):
        return self.__insu_sex

    @insu_sex.setter
    def insu_sex(self, user_sex: Sex = Sex.MALE):
        self.__insu_sex = user_sex

    @property
    def product_type(self):
        return self.__product_type

    @product_type.setter
    def product_type(self, product_type: ProductType = ProductType.NON_REFUND):
        self.__product_type = product_type

    @property
    def expiry_year(self):
        return self.__expiry_year

    @expiry_year.setter
    def expiry_year(self, user_year: str = "20y_100"):
        self.__expiry_year = user_year

    @property
    def expiry(self):
        return self.__expiry

    @expiry.setter
    def expiry(self, user_expiry: int = 20):
        self.__expiry = user_expiry

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, user_duration: int = 100):
        self.__duration = user_duration

    def model_dump(self) -> dict:
        return {
            "custom_name": self.custom_name,
            "insu_age": self.insu_age,
            "insu_sex": self.insu_sex,
            "product_type": self.product_type,
            "expiry_year": self.expiry_year,
            "expiry": self.expiry,
            "duration": self.duration,
        }

    def __repr__(self) -> str:
        gender = "남자" if self.__insu_sex == Sex.MALE else "여자"
        product_type = (
            "무해지형"
            if self.__product_type == ProductType.NON_REFUND
            else "해지환급형"
        )
        return (
            "\n=== 실행 결과 ===\n"
            "\n[설정값]\n"
            f"이름: {self.__custom_name}\n"
            f"나이: {self.__insu_age}세\n"
            f"성별: {gender}\n"
            f"상품유형: {product_type}\n"
            f"보험기간: {self.__expiry_year}"
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
