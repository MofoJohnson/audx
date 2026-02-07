run way path *options:
    {{ if way == "docker" { "docker run --rm -t -v $PWD:/audx mofojohnson/audx '" + path + "' " + options } else if way == "uv" { "uv run audx " + path + " " + options } else { "echo way is not valid; exit 1" } }}

build way tag="latest":
    {{ if way == "docker" { "docker build -t mofojohnson/audx:" + tag + " ." } else if way == "uv" { "uv build" } else { "echo way is not valid; exit 1" } }}

test:
    uv run python -m unittest discover -s tests -v
