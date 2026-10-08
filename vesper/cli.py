import argparse
import sys

from vesper.check import check_username


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Vê se um username existe em perfis públicos de plataformas de código."
    )
    parser.add_argument("username")
    args = parser.parse_args()
    try:
        report = check_username(args.username)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        sys.exit(2)
    print(report["username"])
    for item in report["results"]:
        label = {"found": "existe", "missing": "não achei", "unknown": "inconclusivo"}[item["state"]]
        print(f"  {item['site']:<16} {label:<14} {item['ms']:>5} ms  {item['url']}")


if __name__ == "__main__":
    main()
