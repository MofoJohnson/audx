run way path *options:
    {{ if way == "docker" { "docker run --rm -v $PWD:/audx mofojohnson/audx '" + path + "' " + options } else if way == "uv" { "uv run audx " + path + " " + options } else { "echo way is not valid; exit 1" } }}

build way:
    {{ if way == "docker" { "docker build -t audx ." } else if way == "uv" { "uv build" } else { "echo way is not valid; exit 1" } }}

test:
    uv run python -m unittest discover -s tests -v
