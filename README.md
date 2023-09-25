[![Github Actions Badge](https://github.com/joholl/sokratischer-weg-logo/actions/workflows/publish.yml/badge.svg)](https://github.com/joholl/sokratischer-weg-logo/actions/workflows/publish.yml)

# Sokratischer Weg - logo!

Render the Sokratischer Weg logo.

The logo in its original form is a scalable vector graphic (svg) created in
[inkscape](inkscape.org). To ensure a [WYSIWYG](de.wikipedia.org/wiki/WYSIWYG)
experience, we render them to a `.png` file using also inkscape.

## Dependencies

Install inkscape. To create your python environment:

```sh
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Usage

To generate all sorts of `.png` files, just call

```sh
python src/render.py -o build data/*
```

To be more specific, the usage is

```sh
render.py [-h] [--output-dir OUTPUT_DIR] [--resolutions RESOLUTIONS [RESOLUTIONS ...]] files [files ...]
```

For resolutions, you could pass e.g.
* `64x`: scales the width to 64 pixels, resulting in a 64x36 `.png` file
* `x64`: scales the height to 64 pixels, resulting in a 115x64 `.png` file
* `64x64`: scales the width to 64 pixels and centers the graphic vertically, resulting in a 64x64 `.png` file

## Download Logo

You can download the latest logo as rendered `.png` files: go to the [Github
Actions](https://github.com/joholl/sokratischer-weg-logo/actions/workflows/publish.yml),
select the latest run and download _Sokratischer Weg Logo_.

When a tag is pushed, GitHub Actions will also automatically release the
rendered logo.
