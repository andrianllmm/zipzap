from zipzap.compressor.huffman_coder import HuffmanEncoder, HuffmanDecoder
from zipzap.ds.bits.bit_stream import BitStream


def test_empty_string_encoding_decoding():
    text = ""
    encoder = HuffmanEncoder(text)
    encoded = encoder.encode(text)

    assert len(encoded) == 0
    assert len(encoder.codebook) == 0

    decoder = HuffmanDecoder(encoder.code_lengths)
    decoded = decoder.decode(encoded)
    assert decoded == ""


def test_single_character_string():
    text = "a"
    encoder = HuffmanEncoder(text)
    encoded = encoder.encode(text)

    assert len(encoder.codebook) == 1

    # Encoding of single char should be "0"
    assert encoded == BitStream("0")
    assert encoder.codebook.get("a") == BitStream("0")

    decoder = HuffmanDecoder(encoder.code_lengths)
    decoded = decoder.decode(encoded)
    assert decoded == text


def test_repeated_characters():
    text = "aaaaa"
    encoder = HuffmanEncoder(text)
    encoded = encoder.encode(text)

    assert len(encoder.codebook) == 1

    # Encoding repeated character should be consistent
    code = encoder.codebook.get("a")
    assert code is not None
    assert encoded == BitStream(str(code) * len(text))

    decoder = HuffmanDecoder(encoder.code_lengths)
    decoded = decoder.decode(encoded)
    assert decoded == text


def test_multiple_unique_characters():
    text = "abcde"
    encoder = HuffmanEncoder(text)
    encoded = encoder.encode(text)

    # Each character should have a code
    for c in text:
        assert encoder.codebook.get(c) is not None

    decoder = HuffmanDecoder(encoder.code_lengths)
    decoded = decoder.decode(encoded)
    assert decoded == text


def test_normal_text():
    text = "this is a huffman test"
    encoder = HuffmanEncoder(text)
    encoded = encoder.encode(text)

    decoder = HuffmanDecoder(encoder.code_lengths)
    decoded = decoder.decode(encoded)
    assert decoded == text


def test_non_alpha():
    text = "1!!!!!@@@@###$$%^^&&&****()[]{}<>-_=+;:'\",./?!"
    encoder = HuffmanEncoder(text)
    encoded = encoder.encode(text)

    decoder = HuffmanDecoder(encoder.code_lengths)
    decoded = decoder.decode(encoded)

    assert decoded == text


def test_unicode():
    text = "😀😁😂🤣😃😄😅😆😉😊😋😎😍😘🥰😗😙😚"
    encoder = HuffmanEncoder(text)
    encoded = encoder.encode(text)

    decoder = HuffmanDecoder(encoder.code_lengths)
    decoded = decoder.decode(encoded)

    assert decoded == text


def test_repeated_long_text():
    text = "this is a huffman test " * 1_000
    encoder = HuffmanEncoder(text)
    encoded = encoder.encode(text)

    decoder = HuffmanDecoder(encoder.code_lengths)
    decoded = decoder.decode(encoded)

    assert decoded == text


def test_long_text():
    with open("test_data/alice_wonderland.txt", "r") as f:
        text = f.read()

    encoder = HuffmanEncoder(text)
    encoded = encoder.encode(text)

    decoder = HuffmanDecoder(encoder.code_lengths)
    decoded = decoder.decode(encoded)

    assert decoded == text


def test_consistency_multiple_encodes():
    text = "this is a huffman test"

    encoder1 = HuffmanEncoder(text)
    encoded1 = encoder1.encode(text)
    encoder2 = HuffmanEncoder(text)
    encoded2 = encoder2.encode(text)

    decoder1 = HuffmanDecoder(encoder1.code_lengths)
    decoded1 = decoder1.decode(encoded1)
    decoder2 = HuffmanDecoder(encoder2.code_lengths)
    decoded2 = decoder2.decode(encoded2)

    # Decoded result must match (though codebooks may differ)
    assert decoded1 == text
    assert decoded2 == text
