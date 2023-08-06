import collections

import nlp

from textattack.datasets import HuggingFaceNLPDataset


class TedMultiTranslationDataset(HuggingFaceNLPDataset):
    """ Loads examples from the Ted Talk translation dataset using the `nlp`
        package.
        
        dataset source: http://www.cs.jhu.edu/~kevinduh/a/multitarget-tedtalks/
    """

    def __init__(self, source_lang="en", target_lang="de", split="test"):
        self._dataset = nlp.load_dataset("ted_multi")[split]
        self.examples = self._dataset["translations"]
        language_options = set(self.examples[0]["language"])
        if source_lang not in language_options:
            raise ValueError(
                f"Source language {source_lang} invalid. Choices: {sorted(language_options)}"
            )
        if target_lang not in language_options:
            raise ValueError(
                f"Target language {target_lang} invalid. Choices: {sorted(language_options)}"
            )
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.label_names = ("Translation",)

    def _format_raw_example(self, raw_example):
        source = raw_example["translation"][
            raw_example["language"] == self.source_lang
        ][0]
        target = raw_example["translation"][
            raw_example["language"] == self.target_lang
        ][0]
        source_dict = collections.OrderedDict([("Source", source)])
        return (source_dict, target)
