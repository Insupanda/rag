import langchain_core.output_parsers
import pytest

from src.config.settings import settings
from src.models.generate_answer import PolicyResponse


class DummyRunnable:
    def __or__(self, other):
        return self

    def invoke(self, inputs: dict) -> str:
        return "DUMMY_ANSWER"


@pytest.fixture(autouse=True)
def patch_chain(monkeypatch) -> None:
    monkeypatch.setattr(langchain_core.output_parsers, "StrOutputParser", DummyRunnable)
    monkeypatch.setattr(PolicyResponse, "prompt_system", lambda self: DummyRunnable())
    monkeypatch.setattr(PolicyResponse, "policy_model", lambda self: DummyRunnable())
    monkeypatch.setattr(settings, "openai_api_key", "test-key")


def test_init_without_key_raises() -> None:
    with pytest.raises(RuntimeError) as exc:
        PolicyResponse(openai_client="")
    assert "OpenAI API key가 제공되지 않았습니다" in str(exc.value)


def test_extract_company_info_single() -> None:
    response_policy = PolicyResponse(openai_client="key")
    results = [
        {"collection": "A", "metadata": {"text": "foo"}},
        {"collection": "A", "metadata": {"text": "bar"}},
    ]
    context = response_policy.extract_company_info(results)
    assert response_policy.company_results == {"A": results}
    assert response_policy.multiple_companies is False
    assert "foo" in context and "bar" in context


def test_extract_company_info_multiple() -> None:
    response_policy = PolicyResponse(openai_client="key")
    results = [
        {"collection": "A", "metadata": {"text": "foo"}},
        {"collection": "B", "metadata": {"text": "baz"}},
    ]
    context = response_policy.extract_company_info(results)
    assert set(response_policy.company_results.keys()) == {"A", "B"}
    assert response_policy.multiple_companies is True
    assert "## A 정보:" in context
    assert "## B 정보:" in context
    assert "foo" in context and "baz" in context


def test_generate_answer_no_results() -> None:
    response_policy = PolicyResponse(openai_client="key")
    response = response_policy.generate_answer("질문", [])
    assert response == "검색 결과가 없습니다. 다른 질문을 시도해보세요."


def test_generate_answer_no_context() -> None:
    response_policy = PolicyResponse(openai_client="key")
    results = [{"collection": "A", "metadata": {}}]
    response = response_policy.generate_answer("질문", results)
    assert "관련 정보를 찾을 수 없습니다" in response


def test_generate_answer_valid_flow() -> None:
    response_policy = PolicyResponse(openai_client="key")
    results = [{"collection": "A", "metadata": {"text": "foo"}}]
    response = response_policy.generate_answer("질문", results)
    assert response == "DUMMY_ANSWER"
    assert response_policy.company_results == {"A": results}
    assert response_policy.multiple_companies is False
