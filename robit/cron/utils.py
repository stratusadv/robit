import re

from robit.cron.enums import CronFieldTypeEnum


class CronFieldIdentifier:
    def __init__(self, cron_field_value: 'str'):
        self.value = cron_field_value
        self._identifiers = [self._is_every, self._is_range, self._is_step, self._is_list, self._is_specific]

    def identify(self) -> CronFieldTypeEnum:
        for identifier in self._identifiers:
            identity = identifier()
            if isinstance(identity, CronFieldTypeEnum):
                return identity

        raise ValueError(f'{self.value} is not a valid cron field pattern.')

    def _is_every(self):
        if self.value == '*':
            return CronFieldTypeEnum.EVERY

    def _is_range(self):
        pattern = r'^\d+-\d+$'
        if bool(re.match(pattern, self.value)):
            return CronFieldTypeEnum.RANGE

    def _is_step(self):
        if '/' in self.value:
            return CronFieldTypeEnum.STEP

    def _is_list(self):
        if ',' in self.value:
            return CronFieldTypeEnum.LIST

    def _is_specific(self):
        pattern = re.compile(r'^\d+$')
        if bool(pattern.match(self.value)):
            return CronFieldTypeEnum.SPECIFIC


class CronRangeFinder:
    def __init__(self, cron_field: 'CronField'):
        self.cron_field = cron_field

    def possible_values(self):
        cron_type = self.cron_field.type
        if cron_type == CronFieldTypeEnum.EVERY:
            return self._every()
        elif cron_type == CronFieldTypeEnum.SPECIFIC:
            return self._specific()
        elif cron_type == CronFieldTypeEnum.STEP:
            return self._step()
        elif cron_type == CronFieldTypeEnum.LIST:
            return self._list()
        elif cron_type == CronFieldTypeEnum.RANGE:
            return self._range()

        raise ValueError(f'Cannot find valid range for {self.cron_field}. Is it a valid pattern?')

    def _every(self):
        return list(range(self.cron_field.value_range.start, self.cron_field.value_range.stop))

    def _specific(self):
        if int(self.cron_field.value) not in self.cron_field.value_range:
            raise ValueError(f'Value {self.cron_field.value} is not withing the range {self.cron_field.value_range}')

        return [int(self.cron_field.value)]

    def _step(self):
        cron_segment = self.cron_field.value.split('/')

        cron_field_value = cron_segment[0]
        step_value = int(cron_segment[-1])

        field_class = type(self.cron_field)
        possible_step_values = field_class(cron_field_value).possible_values

        return possible_step_values[::step_value]

    def _list(self):
        valid_values = [int(value) for value in self.cron_field.value.split(',')]

        for value in valid_values:
            if value not in self.cron_field.value_range:
                raise ValueError(
                        f'''Value {value} is not withing the range {self.cron_field.value_range.start}
                        to {self.cron_field.value_range.stop}. '''
                )

            return valid_values

    def _range(self):
        value_list = self.cron_field.value.split('-')
        start_value = int(value_list[0])
        end_value = int(value_list[1])

        if start_value not in self.cron_field.value_range:
            raise ValueError(
                f'Start value is not withing the range {self.cron_field.value_range.start} to {self.cron_field.value_range.stop}.')

        print(end_value)
        if end_value not in self.cron_field.value_range:
            raise ValueError(f'End value is not withing the range {self.cron_field.value_range.start} to {self.cron_field.value_range.stop}.')

        # Need to increase end_value by 1 to include it in the range
        return [value for value in range(start_value, end_value + 1)]
