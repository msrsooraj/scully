import argparse
import csv
import sys
from pathlib import Path

from tqdm import tqdm

from scully.duplicates import group_duplicates
from scully.pipeline import PipelineOptions, discover, process


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cull RAW images by sharpness and duplicate detection."
    )
    parser.add_argument("directory", type=Path, help="Directory containing RAW images")
    parser.add_argument(
        "--output", type=Path, default=Path("report.csv"), help="Output CSV path (default: report.csv)"
    )
    parser.add_argument(
        "--sharpness", action="store_true", help="Run sharpness scoring"
    )
    parser.add_argument(
        "--duplicates", action="store_true", help="Run duplicate detection"
    )
    parser.add_argument(
        "--duplicate-threshold",
        type=int,
        default=10,
        metavar="N",
        help="Max perceptual hash distance to consider two images duplicates (default: 10)",
    )
    args = parser.parse_args()

    if not args.directory.is_dir():
        print(f"error: {args.directory} is not a directory", file=sys.stderr)
        sys.exit(1)

    # No step flags = run everything
    run_all = not args.sharpness and not args.duplicates
    options = PipelineOptions(
        sharpness=run_all or args.sharpness,
        duplicates=run_all or args.duplicates,
        duplicate_threshold=args.duplicate_threshold,
    )

    paths = discover(args.directory)
    if not paths:
        print("No RAW files found.", file=sys.stderr)
        sys.exit(0)

    results = []
    errors = 0
    for path in tqdm(paths, desc="Processing", unit="file"):
        try:
            results.append(process(path, options))
        except Exception as e:
            tqdm.write(f"  skipped {path.name}: {e}", file=sys.stderr)
            errors += 1

    if options.duplicates:
        group_duplicates(results, threshold=options.duplicate_threshold)

    with args.output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["path", "sharpness", "duplicate_group"])
        writer.writeheader()
        for img in results:
            writer.writerow({
                "path": img.path,
                "sharpness": f"{img.sharpness:.4f}" if img.sharpness is not None else "",
                "duplicate_group": img.duplicate_group if img.duplicate_group is not None else "",
            })

    if options.duplicates:
        duplicates = sum(1 for img in results if img.duplicate_group is not None)
        print(f"Duplicates found: {duplicates}")
    print(f"Processed {len(results)} images ({errors} skipped).")
    print(f"Report saved to: {args.output}")


if __name__ == "__main__":
    main()
