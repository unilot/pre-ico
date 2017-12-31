"""
Usage
-----
    >>> import markdown
    >>> src = '''This guy owns [big_amount:($)[7 000 000]] in cash and [big_amount:[25 000](ETH)] on crypto accounts.'''
    >>> html = markdown.markdown(src, ['big_amount'])
    >>> print(html)
    <p>This guy owns <span class="big-amount">$7 000 000</span> in cash and <span class="big-amount">25 000 ETH</span> on crypto accounts.</p>
"""

import markdown


BIG_AMOUNT_RE = r'\[big_amount:(|\((?P<prefix_symbol>[^\d]{1,3})\))\[(?P<amount>[\d ]+)\](|\((?P<suffix_symbol>[^\d]{1,10})\))\]'


class BigAmountPattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        prefix_symbol = m.group('prefix_symbol')
        amount = m.group('amount')
        suffix_symbol = m.group('suffix_symbol')

        el = markdown.util.etree.Element('span', {'class': 'big-amount'})

        if prefix_symbol:
            el.text = '{prefix}{amount}'.format(prefix=prefix_symbol, amount=amount)
        elif suffix_symbol:
            el.text = '{amount} {suffix}'.format(suffix=suffix_symbol, amount=amount)
        else:
            el.text = amount

        return el


class BigAmountExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['big_amount'] = BigAmountPattern(BIG_AMOUNT_RE, md)

def makeExtension(configs={}):
    return BigAmountExtension(configs=dict(configs))
