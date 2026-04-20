from tests.fake_openai import FakeOpenAIClient


def test_fake_returns_configured_content():
    client = FakeOpenAIClient(responses=["hello back"])
    result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "hi"}],
    )
    assert result.choices[0].message.content == "hello back"


def test_fake_records_call_arguments():
    client = FakeOpenAIClient(responses=["ok"])
    client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "hi"}],
    )
    assert len(client.calls) == 1
    assert client.calls[0]["model"] == "gpt-4o-mini"
    assert client.calls[0]["messages"][0]["content"] == "hi"


def test_fake_cycles_through_responses():
    client = FakeOpenAIClient(responses=["a", "b"])
    r1 = client.chat.completions.create(model="x", messages=[])
    r2 = client.chat.completions.create(model="x", messages=[])
    assert r1.choices[0].message.content == "a"
    assert r2.choices[0].message.content == "b"


def test_fake_supports_function_call_arguments():
    client = FakeOpenAIClient(
        responses=[{"function_arguments": '{"vocabulary": ["a","b"]}'}]
    )
    r = client.chat.completions.create(model="x", messages=[])
    assert r.choices[0].message.function_call.arguments == '{"vocabulary": ["a","b"]}'
