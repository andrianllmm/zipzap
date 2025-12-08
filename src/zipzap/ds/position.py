from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Position(ABC, Generic[T]):
    """Abstract location of a single element."""

    @abstractmethod
    def element(self) -> T:
        """Return the element stored at this Position."""
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Return True if other represents the same position."""
        ...

    def __ne__(self, other: object) -> bool:
        """Return True if other does not represent the same position."""
        return not self == other
