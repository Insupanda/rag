from typing import Any

from openai import OpenAI

from db.sql_utils import TemplateManager
from modules.handler import HandlerFactory, IntentHandler


class InsuranceService:
    def __init__(self, openai_client: OpenAI, template_manager: TemplateManager):
        self.openai_client = openai_client
        self.template_manager = template_manager

    def __handle_user_input(self, user_input: str) -> Any:
        intent_handler = IntentHandler(self.openai_client, self.template_manager)
        intent = intent_handler.handle(user_input)

        handler = HandlerFactory.get_handler(intent, self.openai_client, self.template_manager)
        response = handler.handle(user_input)
        print(response)
        return response

    def run(self, user_input: str) -> Any:
        return self.__handle_user_input(user_input)
