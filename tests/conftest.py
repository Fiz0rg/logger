from tests.const import DEFAULT_LOG_VALUES, LOG_TEMPLATE


def make_log(overrides: dict[str, str] | None = None, exclude: list[str] | None = None) -> str:
    values = DEFAULT_LOG_VALUES.copy()
    if overrides:
        values.update(overrides)
    if exclude:
        for k in exclude:
            values[k] = ""
    return LOG_TEMPLATE.format(**values)
