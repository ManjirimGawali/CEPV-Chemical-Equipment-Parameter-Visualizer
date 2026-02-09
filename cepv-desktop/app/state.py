# app/state.py
class AppState:
    token = None
    user = None
    # dashboard
    dataset_id = None
    dataset_name = None
    summary = None
    preview = []
    charts = None
    # history (NEW)
    last_analyzed_id = None
    last_analyzed_summary = None
    last_analyzed_charts = None
    last_analyzed_preview = None

    @classmethod
    def set_token(cls, token):
        cls.token = token

    @classmethod
    def clear(cls):
        cls.token = None
        cls.user = None
