import re
import sys
import logging

logger = logging.getLogger(__name__)

__all__ = ['Rule', 'RuleSyntaxError', 'Filter']

RE_TOK = re.compile('\W')

MAP_RE = (('\|\|','(//|\.)'),
          ('\^', r'[/\\:+!@#\$^\^&\*\(\)\|]'),
          ('\*', r'.*'))


class RuleSyntaxError(Exception):
    pass


TYPE_OPTS = (('script', 'external scripts loaded via HTML script tag'),
             ('image', 'regular images, typically loaded via HTML img tag'),
             ('stylesheet', 'external CSS stylesheet files'),
             ('object', 'content handled by browser plugins, e.g. Flash or Java'),
             ('xmlhttprequest', 'requests started by the XMLHttpRequest object'),
             ('object-subrequest', 'requests started plugins like Flash'),
             ('subdocument', 'embedded pages, usually included via HTML frames'),
             ('document', 'the page itself (only exception rules can be applied to the page)'),
             ('elemhide', 'for exception rules only, similar to document but only disables element hiding rules on the page rather than all filter rules (Adblock Plus 1.2 and higher required)'),
             ('other', 'types of requests not covered in the list above'))
TYPE_OPT_IDS = [x[0] for x in TYPE_OPTS]


class Rule(object):
    def __init__(self, rule_str):
        self.rule_str = rule_str.strip()
        if '$' in rule_str:
            try:
                # A regex may contain a $ and that was breaking this
                rules_split = rule_str.split('$')
                self.optstring = rules_split.pop()
                self.pattern = '$'.join(rules_split)

            except ValueError:
                raise RuleSyntaxError('Invalid rule syntax')
        else:
            self.pattern = self.rule_str
            self.optstring = ''

        self.regex = self._to_regex()
        opts = self.optstring.split(',')
        self.excluded_elements = []
        self.matched_elements = []
        for o in opts:
            if o.startswith('~') and o[1:] in TYPE_OPT_IDS:
                self.excluded_elements.append(o)
            elif o in TYPE_OPT_IDS:
                self.matched_elements.append(o)
        if self.matched_elements == []:
            self.matched_elements = TYPE_OPT_IDS

    def get_tokens(self):
        return RE_TOK.split(self.pattern)

    def match(self, url, elementtype=None):
        if elementtype:
            if elementtype in self.excluded_elements or\
                    (elementtype not in self.matched_elements and\
                         'other' not in self.matched_elements):
                return False
        return self.regex.search(url)

    def _to_regex(self):
        re_str = re.escape(self.pattern)
        for m in MAP_RE:
            re_str = re_str.replace(*m)
        return re.compile(re_str)
    
    def __unicode__(self):
        return self.rule_str


class Filter(object):
    def __init__(self, f, **kwargs):
        self.index = {}
        self.echo = kwargs.get('echo', False)
        for rul in f.readlines():
            if rul.startswith('!'):  # Comment
                continue
            if '##' in rul:  # HTML rule
                continue
            try:
                rule = Rule(rul)

                for tok in rule.get_tokens():
                    if len(tok) > 2:
                        if tok not in self.index:
                            self.index[tok] = []
                        self.index[tok].append(rule)

            except RuleSyntaxError:
                logger.error('syntax error in %s' % rul)

    def match(self, url, elementtype=None):
        matchlist = []
        tokens = RE_TOK.split(url)
        for tok in tokens:
            if len(tok) > 2:
                if tok in self.index:
                    for rule in self.index[tok]:
                        if rule.match(url, elementtype=elementtype):
                            matchlist.append(rule)
                            if self.echo:
                                print(str(rule))
        return matchlist


if __name__ == '__main__':
    fh = open(sys.argv[1], 'r')
    f = Filter(fh, echo=True)
    print('start matching')
    f.match(sys.argv[2])
