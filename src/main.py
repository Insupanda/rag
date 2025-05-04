from config.settings import PROJECT_ROOT, settings
from services.insurance_service import InsuranceService
from db.sql_utils import TemplateManager

from openai import OpenAI


# TODO: isort setting precommit setting

if __name__ == "__main__":
    print("\n=== 보험 상담 챗봇 ===")

    template_manager = TemplateManager(templates_dir=PROJECT_ROOT / "prompts")
    openai_client = OpenAI(api_key=settings.openai_client)

    insurance_service = InsuranceService(
        openai_client=openai_client, template_manager=template_manager
    )
    insurance_service.run()
