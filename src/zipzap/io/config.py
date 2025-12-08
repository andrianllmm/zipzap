class ZzConfig:
    """Shared configuration for .zz file format."""

    NUM_CHARS_SIZE = 2  # bytes to store number of unique characters
    CHAR_LEN_SIZE = 2  # bytes to store UTF-8 length of a character
    CODE_LEN_SIZE = 2  # bytes to store bit length of the character's canonical code
    BIT_LEN_SIZE = 4  # bytes to store total bits of encoded data
