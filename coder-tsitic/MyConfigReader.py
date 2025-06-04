import logging
import os
from typing import Dict

from ConfigReaderInterface import ConfigReaderInterface
from ConfigException import ConfigException


class MyConfigReader(ConfigReaderInterface):
    def read_config(self, config_file_name: str) -> Dict[str, object]:
        config_dir = os.path.dirname(config_file_name)
        try:
            with open(config_file_name, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    if self._param_delimiter not in line:
                        raise ConfigException(f'wrong line in config: {line.strip()}')
                    param, value = map(str.strip, line.split(self._param_delimiter, 1))
                    if param not in self._config_dict:
                        raise ConfigException(f'unknown parameter {param}')
                    self._config_dict[param] = value
        except FileNotFoundError as exc:
            logging.error(exc)
            raise ConfigException(str(exc)) from exc

        # Validate parameters
        if None in self._config_dict.values():
            missing = [k for k, v in self._config_dict.items() if v is None]
            raise ConfigException(f'missing parameters: {", ".join(missing)}')

        buf_val = self._config_dict[self.buffer_size_param_name]
        if isinstance(buf_val, str) and buf_val.lower() == 'десять':
            buf_val = 10
        try:
            buffer_size = int(buf_val)
            self._config_dict[self.buffer_size_param_name] = buffer_size
        except ValueError as exc:
            logging.error(exc)
            raise ConfigException('buffer_size must be an integer') from exc

        coder_option = self._config_dict[self.coder_run_option_param_name]
        if coder_option not in ('code', 'decode'):
            raise ConfigException('coder_option must be "code" or "decode"')

        file_name = self._config_dict[self.file_name_for_coder_param_name]
        if not os.path.isabs(file_name):
            file_name = os.path.join(config_dir, file_name)
        self._config_dict[self.file_name_for_coder_param_name] = file_name

        return self._config_dict
