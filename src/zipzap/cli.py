from pathlib import Path

import typer
from rich.console import Console

from zipzap.compressor.freq_counter import FreqCounter
from zipzap.compressor.huffman_coder import HuffmanEncoder, HuffmanDecoder
from zipzap.io.reader import ZzReader
from zipzap.io.writer import ZzWriter
from zipzap.utils.logger import Logger

app = typer.Typer(help="ZipZap: Compression CLI for text files.")

logger = Logger()
console = Console()


@app.command()
def zip(
    input_file: str,
    output_file: str = typer.Option(None, "--output", "-o"),
):
    """Compress a text file into a .zz file."""

    input_path = Path(input_file)

    if not input_path.exists():
        logger.error(f"The file {input_path} does not exist.")
        raise typer.Exit(code=1)

    output_path = (
        input_path.with_suffix(".zz") if output_file is None else Path(output_file)
    )

    text = input_path.read_text(encoding="utf-8-sig", errors="replace")

    encoder = HuffmanEncoder(text)
    encoded = encoder.encode(text)

    writer = ZzWriter(output_path)
    writer.write(FreqCounter(text), encoded)


@app.command()
def zap(
    input_file: str,
    output_file: str = typer.Option(None, "--output", "-o"),
):
    """Decompress a .zz file into a text file."""

    input_path = Path(input_file)

    if not input_path.exists():
        logger.error(f"The file {input_path} does not exist.")
        raise typer.Exit(code=1)

    output_path = (
        input_path.with_name(input_path.stem + "_decoded.txt")
        if output_file is None
        else Path(output_file)
    )

    reader = ZzReader(input_path)
    encoded, freq_table = reader.read()

    decoder = HuffmanDecoder(freq_table)
    decoded = decoder.decode(encoded)

    output_path.write_text(decoded, encoding="utf-8")


def main():
    app()


if __name__ == "__main__":
    main()
