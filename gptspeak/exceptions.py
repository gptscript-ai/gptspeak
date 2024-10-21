class GPTSpeakError(Exception):
    """Base exception for GPTSpeak"""


class ConversionError(GPTSpeakError):
    """Raised when there's an error during text-to-speech conversion"""


class PlaybackError(GPTSpeakError):
    """Raised when there's an error during audio playback"""


class FileValidationError(GPTSpeakError):
    """Raised when there's an error validating input or output files"""


class APIConfigError(GPTSpeakError):
    """Raised when there's an error with API configuration"""


class ConcatenationError(GPTSpeakError):
    """Raised when there's an error during audio file concatenation"""
