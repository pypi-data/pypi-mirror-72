from typing import Set, Dict, List, Union, Tuple


__all__ = 'TransliterationBruteForcer'


class TransliterationBruteForcer:
    dictionary = (
        u'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
        u'abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA'
    )

    def __init__(
            self,
            custom_dictionary: Union[List[str], Tuple[str, str]] = None,
            custom_mapping: Dict[str, List[str]] = None
    ):
        """
        :param custom_dictionary: You can pass custom dictionary.
            The default is RU -> EN.
        :param custom_mapping: This is need to replace substr
            or pass multiple variants of transliteration.

            .. code-block:: python
                :caption: Example

                mapping = {
                    'Ю': ['Yu', 'Iy'],
                    'ю': ['yu', 'iy'],
                    'й': ['ii', 'iy', 'yy', 'yu'],
                    'х': ['kh']
                }
        """
        if custom_dictionary:
            assert (
                isinstance(custom_dictionary, (list, str))
                and len(custom_dictionary) == 2
            )
            self.dictionary = custom_dictionary

        self.custom_mapping = {}
        if custom_mapping:
            assert isinstance(custom_mapping, dict)
            self.custom_mapping = custom_mapping

    def run(self, name: str) -> Set[str]:
        """BruteForce name"""
        names = name.split()
        if len(names) == 1:
            return self._name(name)
        if len(names) == 2:
            return self._fullname(name)
        else:
            raise ValueError('You should pass first, last or fullname')

    def _name(self, name: str) -> Set[str]:
        results = set()
        translate_variants = {ord(a): ord(b) for a, b in zip(*self.dictionary)}
        results.add(name.translate(translate_variants))

        for i in range(len(name)):
            for j in range(len(name)):
                if j > i:
                    continue

                substring = name[j:i + 1]
                if substring not in self.custom_mapping:
                    continue

                for mapping_variant in self.custom_mapping[substring]:
                    new_name = name[:j] + mapping_variant + name[i + 1:]
                    results.add(new_name.translate(translate_variants))
                    results.update(self._name(new_name))

        return results

    def _fullname(self, fullname: str) -> Set[str]:
        """Brute force fullname (first name and last name)"""
        assert 1 <= len(fullname.split()) <= 2, (
            'You should pass first name and/or last name in str')

        first_name, last_name = fullname.split()
        names: dict = {
            first_name: self._name(first_name),
            last_name: self._name(last_name)
        }
        results = set()
        for first_name_variant in names[first_name]:
            for last_name_variant in names[last_name]:
                results.add(' '.join((first_name_variant, last_name_variant)))
        return results
