from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from zipzap.compressor.huffman_tree import HuffmanTree
from zipzap.ds.bits.bit_stream import BitStream
from zipzap.ds.maps.map import Map
from zipzap.ui.progress_timer import Timer


def file_stats(input_file: Path, output_file: Path) -> Panel:
    """Create a Rich Panel showing file stats."""

    original_size = input_file.stat().st_size
    compressed_size = output_file.stat().st_size

    reduction = (
        100 * (original_size - compressed_size) / original_size if original_size else 0
    )

    table = Table.grid(padding=(0, 2))
    table.add_column(justify="left")
    table.add_column(justify="right")

    table.add_row("[cyan]Size reduction:[/cyan]", f"{reduction:.2f}%")
    table.add_row("[cyan]Original size:[/cyan]", f"{original_size} bytes")
    table.add_row("[cyan]Compressed size:[/cyan]", f"{compressed_size} bytes")

    return Panel(table, expand=False)


def time_stats(*timers: Timer) -> Panel:
    """Create a Rich Panel showing timing stats as a single line."""

    parts = [f"[cyan]{timer.task}:[/cyan] {timer.duration:.4f} s" for timer in timers]
    text = " | ".join(parts)
    return Panel(Text.from_markup(text), expand=False)


def file_content(
    text: str,
    title: str,
    file_name: Optional[str] = None,
    line_width: int = 50,
    max_lines: int = 5,
) -> Panel:
    """Create a Rich Panel showing a file's content."""

    # Split text into fixed-width lines
    lines = [text[i : i + line_width] for i in range(0, len(text), line_width)]
    truncated_lines = lines[:max_lines]
    if len(lines) > max_lines:
        truncated_lines.append("...")

    display_text = "\n".join(truncated_lines)

    syntax = Syntax(
        display_text,
        "text",
        line_numbers=True,
        word_wrap=True,
        indent_guides=True,
    )

    panel_title = f"{file_name or 'File'} - {title}"
    return Panel(syntax, title=panel_title, expand=False)


def frequency_table(freq_table: Map[str, int]) -> Table:
    """Create a Rich Table showing the character frequency."""

    table = Table(title="Character Frequency & Huffman Codes")

    table.add_column("Character", justify="center")
    table.add_column("Frequency", justify="right")

    sorted_entries = sorted(freq_table.entries(), key=lambda x: x.value, reverse=True)

    for char, freq in sorted_entries:
        table.add_row(repr(char), str(freq))

    return table


def huffman_tree_diagram(tree: HuffmanTree) -> Tree:
    """Convert a HuffmanTree into a Rich.Tree."""

    def _build_huffman_subtree(tree: HuffmanTree, position) -> Tree:
        """Recursive helper that converts each subtree into a Rich Tree node."""
        node = position.element()
        label = (
            f"[bold cyan]{repr(node.char)}[/] : {node.freq}"
            if node.char is not None
            else f"[bold yellow]•[/] : {node.freq}"
        )
        rich_node = Tree(label)

        left = tree.left(position)
        right = tree.right(position)

        if left is not None:
            rich_node.add(_build_huffman_subtree(tree, left))

        if right is not None:
            rich_node.add(_build_huffman_subtree(tree, right))

        return rich_node

    root = tree.root()

    if root is None:
        return Tree("[red]Empty Huffman Tree")

    return _build_huffman_subtree(tree, root)


def show_success(console: Console, output_path: Path, action: str):
    """Show a success message with a link to the output file."""

    console.print(f"[bold yellow]\n⚡ {action}! ⚡[/bold yellow]")
    console.print(f"[dim italic]to [underline]{output_path}[/underline][/dim italic]\n")
