# [curlylint](https://www.curlylint.org/) [<img src="https://raw.githubusercontent.com/thibaudcolas/curlylint/master/.github/curlylint-logo.svg?sanitize=true" width="250" height="100" align="right" alt="">](https://www.curlylint.org/)

[![PyPI](https://img.shields.io/pypi/v/curlylint.svg)](https://pypi.org/project/curlylint/) [![PyPI downloads](https://img.shields.io/pypi/dm/curlylint.svg)](https://pypi.org/project/curlylint/) [![Travis](https://travis-ci.com/thibaudcolas/curlylint.svg?branch=master)](https://travis-ci.com/thibaudcolas/curlylint) [![Total alerts](https://img.shields.io/lgtm/alerts/g/thibaudcolas/curlylint.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/thibaudcolas/curlylint/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/thibaudcolas/curlylint.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/thibaudcolas/curlylint/context:python) [![Netlify Status](https://api.netlify.com/api/v1/badges/6830546d-b21d-4067-9ca2-7288b4aedbaa/deploy-status)](https://app.netlify.com/sites/elegant-engelbart-bc2c51/deploys)

> **{{ 🎀}}** Experimental linter for [Jinja](https://jinja.palletsprojects.com/), [Nunjucks](https://mozilla.github.io/nunjucks/), [Django templates](https://docs.djangoproject.com/en/dev/topics/templates/), [Twig](https://twig.symfony.com/), [Liquid](https://shopify.github.io/liquid/).
> Forked from [jinjalint](https://github.com/motet-a/jinjalint).

## Features

curlylint is an experimental linter for [“curly braces”](tests/README.md) templates, and their HTML. It supports:

- Linting invalid template / HTML syntax due to mismatched tags – while template errors are easy enough to spot, it’s not rare for HTML issues to make their way to live sites.
- Indentation inconsistencies – Usage of tabs vs spaces, line breaks, indentation size.
- [Rules](#rules) to check for common accessibility issues.

![Screenshot of the curlylint CLI, with an example invocation raising a parsing issue and a rule error](.github/curlylint-screenshot.png)

In the future, we’d like to lint for:

- Common accessibility issues in HTML – misuse of ARIA `role`, and making sure alternative text is used where appropriate.
- Common security issues – e.g. `rel="noopener noreferrer"`, or preventing usage of HTTP URLs.
- General HTML code smells – duplicate attributes, invalid attributes, etc.
- More [ideas welcome](docs/README.md)!

## Usage

curlylint is available on [PyPI](<(https://pypi.org/project/curlylint/)>). To install it,

```sh
pip install curlylint
```

We support the following Python versions: 3.6, 3.7, 3.8.

Make sure curlylint is correctly installed by running:

```sh
curlylint --version
curlylint --help
```

You can start linting!

```sh
curlylint template-directory/
# Or,
curlylint some-file.html some-other-file.html
```

Have a look at the [CLI flags](#cli-flags), [Configuration](#configuration), and [Rules](#rules) below to make the most of it.

### CLI flags

#### `--verbose`

Turns on verbose mode. This makes it easier to troubleshoot what configuration is used, and what files are being linted.

```sh
curlylint --verbose template-directory/
```

#### `--quiet`

Don’t emit non-error messages to stderr. Errors are still emitted; silence those with `2>/dev/null`.

```sh
curlylint --quiet template-directory/
```

#### `--parse-only`

Don’t lint, check for syntax errors and exit.

```sh
curlylint --parse-only template-directory/
```

#### `--print-config`

Print the configuration for the given file, and exit.

```sh
curlylint --print-config some-file.html
```

#### `--rule`

Specify rules, with the syntax `--rule 'code: {"json": "value"}'`. Can be provided multiple times to configure multiple rules.

```sh
curlylint --rule 'indent: 2' --rule 'html_has_lang: true' template-directory/
```

#### Reading from standard input

Pipe the template to curlylint and use a path of `-` so curlylint reads from stdin:

```sh
cat some-file.html | curlylint -
```

The `--stdin-filepath` flag can be used to provide a fake path corresponding to the piped template for linting and reporting:

```sh
cat some-file.html | curlylint - --stdin-filepath some-file.html
```

## Configuration

_curlylint_ is able to read project-specific default values for its command line options from a [PEP 518](https://www.python.org/dev/peps/pep-0518/) `pyproject.toml` file.

### Where _curlylint_ looks for the file

By default _curlylint_ looks for `pyproject.toml` starting from the common base directory of all files and directories passed on the command line. If it's not there, it looks in parent directories. It stops looking when it finds the file, or a `.git` directory, or a `.hg` directory, or the root of the file system, whichever comes first.

You can also explicitly specify the path to a particular file that you want with `--config`. In this situation _curlylint_ will not look for any other file.

If you're running with `--verbose`, you will see a blue message if a file was found and used.

### Configuration format

As the file extension suggests, `pyproject.toml` is a
[TOML](https://github.com/toml-lang/toml) file. It contains separate sections for
different tools. _curlylint_ is using the `[tool.curlylint]` section. The option keys are the same as long names of options on the command line.

<details>

<summary>Example `pyproject.toml`</summary>

```ini
[tool.curlylint]
# Specify additional Jinja elements which can wrap HTML here. You
# don't neet to specify simple elements which can't wrap anything like
# {% extends %} or {% include %}.
jinja-custom-elements-names = [
  ["cache", "endcache"],
  ["captureas", "endcaptureas"]
]
include = '\.(html|jinja)$'
exclude = '''
(
  /(
      \.eggs           # exclude a few common directories in the root of the project
    | \.git
    | \.venv
    | build
    | dist
  )/
  | webpack-stats.html # also separately exclude a file named webpack-stats.html in the root of the project
)
'''

[tool.curlylint.rules]
# How many spaces
indent = 4
html_has_lang = 'en-GB'
```

</details>

### Lookup hierarchy

Command-line options have defaults that you can see in `--help`. A `pyproject.toml` can override those defaults. Finally, options provided by the user on the command line override both.

_curlylint_ will only ever use one `pyproject.toml` file during an entire run. It doesn't look for multiple files, and doesn't compose configuration from different levels of the file hierarchy.

## Rules

### `indent`

Enforces consistent indentation. Options:

```ini
# Use the given number of spaces.
indent = 4
# Use tabs.
indent = "tab"
```

### `html_has_lang`

Checks all `html` elements have a `lang` attributes. Options:

```ini
# The `lang` attribute must be present.
html_has_lang = true
# The `lang` attribute must be a specific value.
html_has_lang = "en-US"
# The `lang` attribute must be one of the possible values.
html_has_lang = ["en", "en-GB", "en-US"]
```

### `aria_role`

Checks all `role` attributes use valid values. Options:

```ini
# The role attribute must be a valid ARIA role.
aria_role = true
# The role attribute must be one of the whitelisted options.
aria_role = ["region", "search", "alert", "dialog"]
```

## Usage with [pre-commit](https://pre-commit.com) git hooks framework

Add to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/thibaudcolas/curlylint
  rev: "" # select a tag / sha to point at
  hooks:
    - id: curlylint
```

Make sure to fill in the `rev` with a valid revision.

_Note_: by default this configuration will only match `.jinja` and `.jinja2`
files. To match by regex pattern instead, override `types` and `files` as
follows:

```yaml
- id: curlylint
  types: [file] # restore the default `types` matching
  files: \.(html|sls)$
```

## Contributing

See anything you like in here? Anything missing? We welcome all support, whether on bug reports, feature requests, code, design, reviews, tests, documentation, and more. Please have a look at our [contribution guidelines](CONTRIBUTING.md).

If you just want to set up the project on your own computer, the contribution guidelines also contain all of the setup commands.

## Credits

This project is a fork of [jinjalint](https://github.com/motet-a/jinjalint).

Image credit: [FxEmojis](https://github.com/mozilla/fxemoji).

Test templates extracted from third-party projects. View the full list in [`tests/README.md`](tests/README.md).

View the full list of [contributors](https://github.com/thibaudcolas/curlylint/graphs/contributors). [MIT](https://github.com/thibaudcolas/curlylint/blob/master/LICENSE) licensed. Website content available as [CC0](https://creativecommons.org/share-your-work/public-domain/cc0/).
