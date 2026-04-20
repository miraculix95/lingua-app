from src.state import SessionState, init_session_state


def test_init_defaults():
    state = SessionState()
    assert state.vocab_list == []
    assert state.task_type is None
    assert state.num_runs == 0
    assert state.user_text == ""


def test_init_increments_run_counter():
    fake: dict = {}
    init_session_state(fake)
    assert fake["state"].num_runs == 1
    init_session_state(fake)
    assert fake["state"].num_runs == 2


def test_init_preserves_existing_state():
    fake: dict = {}
    init_session_state(fake)
    fake["state"].user_text = "Bonjour"
    init_session_state(fake)
    assert fake["state"].user_text == "Bonjour"
    assert fake["state"].num_runs == 2
