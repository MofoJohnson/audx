default: run

run path="." *options:
    uv run audx {{ path }} {{ options }}

test:
    uv run python -m unittest discover -s tests -v
