
class ThufirConfig(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ThufirConfig, cls).__new__(cls)
        return cls._instance


def get_thufir_config() -> ThufirConfig:
    """
    Returns a read-only view of the Thufir configuration.
    """
    # PLACEHOLDER: Replace with actual configuration loading logic
    return ThufirConfig()
