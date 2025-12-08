from pathlib import Path

import typer

from zipzap.utils.logger import Logger

logger = Logger()


def confirm_overwrite(path: Path) -> None:
    """Prompt before overwriting an existing file, logging the warning."""
    if path.exists():
        logger.warning(f"File '{path}' already exists.")

        overwrite = typer.confirm("Do you want to overwrite it?", default=False)
        if not overwrite:
            raise typer.Exit(code=1)
