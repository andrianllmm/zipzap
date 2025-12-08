from pathlib import Path

import typer
from rich.console import Console

from zipzap.compressor.freq_counter import FreqCounter
from zipzap.compressor.huffman_coder import HuffmanEncoder, HuffmanDecoder
from zipzap.compressor.huffman_tree import HuffmanTreeBuilder
from zipzap.io.reader import ZzReader
from zipzap.io.writer import ZzWriter
from zipzap.ui.components import (
    frequency_table,
    file_content,
    file_stats,
    huffman_tree_diagram,
    show_success,
    time_stats,
)
from zipzap.ui.progress_timer import timed_progress
from zipzap.ui.prompts import confirm_overwrite
from zipzap.utils.logger import Logger

app = typer.Typer(help="ZipZap: Compression CLI for text files.")

logger = Logger()
console = Console()


@app.command()
def zip(
    input_file: str,
    output_file: str = typer.Option(None, "--output", "-o"),
    show_stats: bool = typer.Option(True, "--stats", help="Show file stats"),
    show_time: bool = typer.Option(False, "--time", help="Show encode/write timing"),
    show_contents: bool = typer.Option(False, "--contents", help="Show file contents"),
    show_freq: bool = typer.Option(False, "--freq", help="Show frequency table"),
    show_tree: bool = typer.Option(False, "--tree", help="Show Huffman tree"),
):
    """Compress a text file into a .zz file."""

    SMALL_FILE_THRESHOLD = 50

    if input_file.endswith(".zz"):
        logger.warning("Compressing a .zz file")

    input_path = Path(input_file)

    if not input_path.exists():
        logger.error(f"The file {input_path} does not exist.")
        raise typer.Exit(code=1)

    output_path = (
        input_path.with_suffix(".zz") if output_file is None else Path(output_file)
    )
    confirm_overwrite(output_path)

    text = input_path.read_text(encoding="utf-8-sig", errors="replace")

    if len(text) < SMALL_FILE_THRESHOLD:
        logger.warning("Very small files may compress poorly.")

    with timed_progress("Encode", "Encoding text...") as encode_timer:
        encoder = HuffmanEncoder(text)
        encoded = encoder.encode(text)

    with timed_progress("Write", "Writing compressed file...") as write_timer:
        writer = ZzWriter(output_path)
        writer.write(FreqCounter(text), encoded)

    show_success(console, output_path, "Zipped!")

    if show_stats:
        console.print(file_stats(input_path, output_path))
    if show_time:
        console.print(time_stats(encode_timer, write_timer))
    if show_contents:
        console.print(file_content(text, "Original Text", input_path.name))
        console.print(file_content(str(encoded), "Encoded Bits", output_path.name))
    if show_freq:
        table = frequency_table(encoder.freq_table)
        with console.pager(styles=True):
            console.print(table)
    if show_tree:
        with console.pager(styles=True):
            console.print(
                huffman_tree_diagram(
                    HuffmanTreeBuilder.from_freq_table(encoder.freq_table)
                )
            )


@app.command()
def zap(
    input_file: str,
    output_file: str = typer.Option(None, "--output", "-o"),
    show_stats: bool = typer.Option(True, "--stats", help="Show file stats"),
    show_time: bool = typer.Option(False, "--time", help="Show encode/write timing"),
    show_contents: bool = typer.Option(False, "--contents", help="Show file contents"),
    show_freq: bool = typer.Option(False, "--freq", help="Show frequency table"),
    show_tree: bool = typer.Option(False, "--tree", help="Show Huffman tree"),
):
    """Decompress a .zz file into a text file."""

    if not input_file.endswith(".zz"):
        logger.warning("Decompressing a non-.zz file")

    input_path = Path(input_file)

    if not input_path.exists():
        logger.error(f"The file {input_path} does not exist.")
        raise typer.Exit(code=1)

    output_path = (
        input_path.with_name(input_path.stem + "_decoded.txt")
        if output_file is None
        else Path(output_file)
    )
    confirm_overwrite(output_path)

    with timed_progress("Read", "Reading compressed file...") as read_timer:
        reader = ZzReader(input_path)
        encoded, freq_table = reader.read()

    with timed_progress("Decode", "Decoding text...") as decode_timer:
        decoder = HuffmanDecoder(freq_table)
        decoded = decoder.decode(encoded)

    output_path.write_text(decoded, encoding="utf-8")

    show_success(console, output_path, "Zapped!")

    if show_stats:
        console.print(file_stats(input_path, output_path))
    if show_time:
        console.print(time_stats(read_timer, decode_timer))
    if show_contents:
        console.print(file_content(str(encoded), "Encoded Bits", input_path.name))
        console.print(file_content(decoded, "Decoded Text", output_path.name))
    if show_freq:
        table = frequency_table(decoder.freq_table)
        with console.pager(styles=True):
            console.print(table)
    if show_tree:
        with console.pager(styles=True):
            console.print(
                huffman_tree_diagram(
                    HuffmanTreeBuilder.from_freq_table(decoder.freq_table)
                )
            )


def main():
    app()


if __name__ == "__main__":
    main()
