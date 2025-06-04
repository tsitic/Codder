from CoderInterface import CoderInterface


class MyCoder(CoderInterface):
    _shift = 3

    def run(self, coder_info: str, string_to_process: str) -> str:
        if coder_info == 'code':
            return self._code(string_to_process)
        elif coder_info == 'decode':
            return self._decode(string_to_process)
        else:
            raise ValueError('unknown coder option')

    def _shift_char(self, ch: str, shift: int) -> str:
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
        return ch

    def _code(self, string_to_code: str) -> str:
        return ''.join(self._shift_char(c, self._shift) for c in string_to_code)

    def _decode(self, string_to_decode: str) -> str:
        return ''.join(self._shift_char(c, -self._shift) for c in string_to_decode)
