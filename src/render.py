# /bin/env python

import argparse
import io
import logging
import os
import subprocess

from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def render_svg(svg_file, resolutions, output_dir, formats=None):
    logger.info(f"Opening {svg_file}...")
    output = subprocess.check_output(
        ["inkscape", "--query-width", "--query-height", svg_file]
    )
    svg_width, svg_height = (
        float(s) for s in output.decode("utf-8").strip().splitlines()
    )

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Render SVG at different resolutions
    for width, height in resolutions:
        center_vertically = False
        center_horizontally = False

        if width is not None and height is not None:
            # both given, find out where to fit and where to center
            if width / svg_width < height / svg_height:
                center_vertically = True
                png_width = width
                png_height = round(svg_height * width / svg_width)
            else:
                center_horizontally = True
                png_width = round(svg_width * height / svg_height)
                png_height = height
        elif width is not None:
            png_width = width
            png_height = round(svg_height * width / svg_width)
        elif height is not None:
            png_width = round(svg_width * height / svg_height)
            png_height = height
        else:
            raise ValueError("Pass either width or height.")

        filename = os.path.splitext(os.path.basename(svg_file))[0]
        output_filename = f"{filename}_{png_width}x{png_height}.png"
        output_path = os.path.join(output_dir, output_filename)

        logger.info(f"{svg_file} | Writing to {output_path}...")
        subprocess.run(
            [
                "inkscape",
                "--export-type=png",
                f"--export-filename={output_path}",
                f"--export-width={png_width}",
                f"--export-height={png_height}",
                svg_file,
            ],
            check=True,
        )

        if center_vertically:
            image = Image.open(output_path)

            canvas = Image.new("RGBA", (width, height))
            y_offset = (height - png_height) // 2
            canvas.paste(image, (0, y_offset))

            new_filename = os.path.splitext(os.path.basename(svg_file))[0]
            new_output_filename = f"{filename}_{width}x{height}.png"
            new_output_path = os.path.join(output_dir, new_output_filename)

            logger.info(
                f"{svg_file} | Centering vertically. Writing to {new_output_path}..."
            )
            canvas.save(new_output_path)

        if center_horizontally:
            raise NotImplementedError(
                "This is trivially to implement but i was to lazy to test this."
            )


def main():
    # Define the default resolutions
    DEFAULT_RESOLUTIONS = [
        "x16",
        "x32",
        "x64",
        "x120",
        "x240",
        "x360",
        "x480",
        "x720",
        "x1080",
        "x2160",
        "32x32",
        "64x64",
        "360x360",
        "1080x1080",
    ]

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description="Render SVG files with specified format and resolutions."
    )

    # Add arguments
    # parser.add_argument("--format", "-f", required=False, help="Output format (e.g., google).")
    parser.add_argument("--output-dir", "-o", default="build", help="Output directory.")
    parser.add_argument(
        "--resolutions",
        "-r",
        nargs="+",
        default=DEFAULT_RESOLUTIONS,
        help="Resolution, i.e. rough height of png (e.g., 360 480 720).",
    )
    parser.add_argument("files", nargs="+", help="SVG files to render.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # to (width, height) tuples
    resolutions = [
        tuple(int(num) if num else None for num in resolution.split("x"))
        for resolution in args.resolutions
    ]

    logger.info(f"Input files: {' '.join(args.files)}")
    logger.info(f"Resolutions: {' '.join(str(r) for r in resolutions)}")
    logger.info(f"Output dir:  {args.output_dir}")

    # Process each SVG file
    for path_svg_file in args.files:
        render_svg(path_svg_file, resolutions=resolutions, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
