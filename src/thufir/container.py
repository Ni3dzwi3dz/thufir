from dependency_injector.containers import DeclarativeContainer, providers


class Container(DeclarativeContainer):
    config = providers.Configuration()
