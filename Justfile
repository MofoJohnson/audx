run way path *options:
    {{ if way == "docker" { "docker run --rm -v $PWD:/audx audx " + path + " " + options } else if way == "uv" { "uv run audx " + path + " " + options } else { "echo way is not valid; exit 1" } }}

test:
    uv run python -m unittest discover -s tests -v
