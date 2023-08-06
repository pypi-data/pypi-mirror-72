
import re
import repromancy

def test_cast_on_emptyham(emptyham):
    repromancy.cast(emptyham)
    assert(repr(emptyham).startswith('<module \'emptyham\' from '))

def test_cast_on_spam(spam):
    repromancy.cast(spam)
    assert(repr(spam).startswith('<module \'_repromancy_spam\' from '))
    assert(repr(spam.ham).startswith('<module \'_repromancy_spam.ham\' from '))
    assert(repr(spam.EggType) == '<class \'_repromancy_spam.EggType\'>')
    assert(repr(spam.Egg) == '<class \'_repromancy_spam.Egg\'>')
    assert(re.match(
        r'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>',
        repr(spam.egg)
    ))
    assert(re.match(
        r'<function \'_repromancy_spam.count_eggs\' at 0x[\da-fA-F]+>',
        repr(spam.count_eggs)
    ))
    assert(repr(spam.ham.Public) == '<class \'_repromancy_spam.ham.Public\'>')
    assert(
        repr(spam.ham.Private) ==
        '<class \'_repromancy_spam._impl.ham.Private\'>'
    )
    
    assert(not re.match(
        r'<class \'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>\.YolkType\'>',
        repr(spam.egg.YolkType)
    ))
    assert(not re.match(
        r'<class \'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>\.Yolk\'>',
        repr(spam.egg.Yolk)
    ))
    assert(not re.match(
        r'<function \'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>\.crack\' '
        r'at 0x[\dA-F]+>',
        repr(spam.egg.crack)
    ))
    repromancy.cast(spam.egg)
    assert(re.match(
        r'<class \'<_repromancy_spam.Egg object at '
        f'0x[\da-fA-F]+>\.YolkType\'>',
        repr(spam.egg.YolkType)
    ))
    assert(re.match(
        r'<class \'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>\.Yolk\'>',
        repr(spam.egg.Yolk)
    ))
    assert(re.match(
        r'<function \'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>\.crack\' '
        r'at 0x[\da-fA-F]+>',
        repr(spam.egg.crack)
    ))
