# coding: utf-8

from __future__ import unicode_literals

import sys

from pytest import mark, raises

from gb2260 import Division, get


@mark.parametrize('code,stack_name,is_province,is_prefecture,is_county', [
    ('110101', u'北京市/市辖区/东城区', False, False, True),
    ('110100', u'北京市/市辖区', False, True, False),
    ('110000', u'北京市', True, False, False),
])
def test_division(code, stack_name, is_province, is_prefecture, is_county):
    division = get(code)
    assert division.code == code
    assert division.is_province == is_province
    assert division.is_prefecture == is_prefecture
    assert division.is_county == is_county
    assert '/'.join(x.name for x in division.stack()) == stack_name


@mark.skipif(sys.version_info[0] != 2, reason='requires python 2.x')
@mark.parametrize('code,year,repr_result,unicode_result', [
    ('110101', None,
     "gb2260.get(u'110101')", u'<GB2260 110101 北京市/市辖区/东城区>'),
    ('110100', None,
     "gb2260.get(u'110100')", u'<GB2260 110100 北京市/市辖区>'),
    ('110000', None,
     "gb2260.get(u'110000')", u'<GB2260 110000 北京市>'),
    ('110000', 2006,
     "gb2260.get(u'110000', 2006)", u'<GB2260-2006 110000 北京市>'),
])
def test_representation_python2(code, year, repr_result, unicode_result):
    division = get(code, year)
    assert repr(division) == repr_result
    assert str(division) == unicode_result.encode('utf-8')
    assert unicode(division) == unicode_result
    assert isinstance(repr(division), str)
    assert isinstance(str(division), str)
    assert isinstance(unicode(division), unicode)


@mark.skipif(sys.version_info[0] != 3, reason='requires python 3.x')
@mark.parametrize('code,year,repr_result,unicode_result', [
    ('110101', None,
     u"gb2260.get('110101')", u'<GB2260 110101 北京市/市辖区/东城区>'),
    ('110100', None,
     u"gb2260.get('110100')", u'<GB2260 110100 北京市/市辖区>'),
    ('110000', None,
     u"gb2260.get('110000')", u'<GB2260 110000 北京市>'),
    ('110000', 2006,
     u"gb2260.get('110000', 2006)", u'<GB2260-2006 110000 北京市>'),
])
def test_representation_python3(code, year, repr_result, unicode_result):
    division = get(code, year)
    assert repr(division) == repr_result
    assert str(division) == unicode_result
    assert isinstance(repr(division), str)
    assert isinstance(str(division), str)


def test_comparable():
    assert get(110101) == Division(110101, u'东城区')
    assert get(110101) != Division(110000, u'北京市')
    assert get(110101, year=2006) != Division(110101, u'东城区')


def test_hashable():
    division_set = set([
        Division(110101, u'东城区'),
        Division(110000, u'北京市'),
        Division(110101, u'东城区'),
        Division(110101, u'东城区', 2006),
    ])
    assert division_set == set([
        Division(110101, u'东城区'),
        Division(110000, u'北京市'),
        Division(110101, u'东城区', 2006),
    ])


def test_history_data():
    get(522401, year=2010) == Division(522401, u'毕节市', 2010)

    with raises(ValueError) as error:
        get(522401)
    assert error.value.args[0] == '522401 is not valid division code'

    with raises(ValueError) as error:
        get(110101, 2000)
    assert error.value.args[0].startswith('year must be in')


@mark.parametrize('code,name,year', [
    (522401, u'毕节市', 2010),
    (419000, u'省直辖县级行政区划', None),
])
def test_searching(code, name, year):
    division = Division.search(code)
    assert division.name == name
    assert division.year == year
