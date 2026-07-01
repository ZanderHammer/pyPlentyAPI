"""Version the CHANGELOG.md [Unreleased] section as part of `cz bump`.

Invoked as a commitizen pre_bump_hook; reads the new version from the
CZ_PRE_NEW_VERSION env var that commitizen injects into hook commands.
"""

import datetime
import os

CHANGELOG = "CHANGELOG.md"
UNRELEASED = "## [Unreleased]"


def main() -> None:
    new_version = os.environ["CZ_PRE_NEW_VERSION"]
    today = datetime.date.today().isoformat()

    with open(CHANGELOG) as f:
        content = f.read()

    if f"## [{new_version}]" in content:
        return

    content = content.replace(
        UNRELEASED, f"{UNRELEASED}\n\n## [{new_version}] - {today}", 1
    )

    with open(CHANGELOG, "w") as f:
        f.write(content)


if __name__ == "__main__":
    main()
