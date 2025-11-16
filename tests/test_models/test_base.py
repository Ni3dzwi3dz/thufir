from src.thufir.models.base_model import ThufirModel
from src.thufir.exceptions.models import DatabaseModelNotSet


def test_if_error_is_raised_when_model_not_set():
    class TestModel(ThufirModel):
        pass

    model = TestModel()

    try:
        model.to_db_model()
    except DatabaseModelNotSet as e:
        assert str(e) == "Database model not set for class: TestModel"
    else:
        assert False, "Expected DatabaseModelNotSet exception was not raised."
