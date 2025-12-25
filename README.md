<div align="center">

# ZipZap

**A text file compressor built from scratch using Huffman coding**

[![Demo](https://asciinema.org/a/764041.svg)](https://asciinema.org/a/764041)

</div>

## About

ZipZap is CLI tool that compresses text files using Huffman coding.
It is made from scratch with custom data structures.

### Features

- **Lossless compression** using canonical Huffman coding
- **Custom data structures** implemented from scratch (no external DS libraries)
- **Rich CLI interface** with progress indicators and detailed output
- **Compression analysis** with file size reduction and time stats
- **Debug tools** to inspect codebooks, Huffman trees, and bitstreams

## Installation

### Requirements

- Python 3.10+
- Poetry (recommended) or pip

### From Source

```sh
# Clone the repository
git clone https://github.com/andrianllmm/zipzap.git
cd zipzap
```

```sh
# Install with Poetry
poetry install
```

```sh
# Or install with pip
pip install -e .
```

## Usage

### Basic Compression

Compress a text file to `.zz` format:

```sh
zipzap zip input.txt -o output.zz
```

Without specifying an output file, it creates `<filename>.zz`.

### Basic Decompression

Decompress a `.zz` file back to text:

```sh
zipzap zap compressed.zz -o output.txt
```

Without specifying an output file, it creates `<filename>_decoded.txt`:

### Advanced Options

#### View Time Stats

```sh
zipzap zip input.txt --time
# Shows encoding and writing times
```

#### Inspect the Codebook

```sh
zipzap zip input.txt --codebook
# Displays character-to-code mappings with frequencies
```

#### Visualize the Huffman Tree

```sh
zipzap zip input.txt --tree
# Shows the complete Huffman tree structure
```

#### Preview File Contents

```sh
zipzap zip input.txt --contents
# Displays the few first lines of the input and output files
```

## The `.zz` File Format

The `.zz` file format consists of:

```
[Header]
- Number of unique characters (2 bytes)
- For each character:
  - UTF-8 byte length (2 bytes)
  - UTF-8 character bytes (variable)
  - Code length in bits (2 bytes)

[Body]
- Total bit length (4 bytes)
- Packed bitstream (variable)
```

## Development

### Testing

Run tests with [pytest](https://docs.pytest.org/en/stable/):

```sh
poetry run pytest
```

## Contributing

Contributions are welcome! To get started:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## Issues

Found a bug or issue? Report it on the
[issues page](https://github.com/andrianllmm/zipzap/issues).
