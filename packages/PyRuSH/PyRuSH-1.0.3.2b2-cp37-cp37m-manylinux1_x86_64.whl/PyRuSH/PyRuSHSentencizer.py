from spacy.pipeline import Sentencizer
from PyRuSH import RuSH

from .StaticSentencizerFun import cpredict, cset_annotations, csegment


class PyRuSHSentencizer(Sentencizer):
    def __init__(self, rules_path: str = '', max_repeat: int = 50, auto_fix_gaps: bool = True,
                 token_compatible: bool = True) -> Sentencizer:
        """

        @param rules_path: The string of the rule file path or rules themselves.
        @param max_repeat: Total number of replicates that allows to be handled by "+" wildcard.
        @param auto_fix_gaps: If gaps are caused by malcrafted rules, try to fix them.
        @param token_compatible: when true, this approach only works for spacy >=2.2.3.
            However, this has no control of sentence end, TODO: need to see how the downsteam spacy components make use of doc.c
        """
        self.rules_path = rules_path
        self.token_compatible = token_compatible
        self.rush = RuSH(rule_str=rules_path, max_repeat=max_repeat, auto_fix_gaps=auto_fix_gaps)

    @classmethod
    def from_nlp(cls, nlp, **cfg):
        return cls(**cfg)

    def __call__(self, doc):
        if self.token_compatible:

            tags = self.predict([doc])
            self.set_annotations([doc], tags)
            return doc
        else:
            doc = csegment(doc, self.rush.segToSentenceSpans(doc.text))
            return doc


    def predict(self, docs):
        """Apply the pipeline's model to a batch of docs, without
        modifying them.
        """
        guesses = cpredict(docs, self.rush.segToSentenceSpans)
        return guesses

    def set_annotations(self, docs, batch_tag_ids, tensors=None):
        """
        This function overwrite spacy's Sentencizer.

        @param batch_tag_ids: a list of doc's tags (a list of boolean values)
        @param tensors: a place holder for future extensions
        """
        cset_annotations(docs, batch_tag_ids, tensors)
