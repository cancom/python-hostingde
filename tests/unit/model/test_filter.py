import pytest

from hostingde.model.filter import FilterCondition, FilterCompilationException, FilterChain, FilterChainConnective


class TestSimpleFilterCondition:

    def test_simple_equals_condition(self):
        filter = FilterCondition('key').eq('random').to_filter_object()

        assert filter.get('field', '') == 'key'
        assert filter.get('value', '') == 'random'
        assert filter.get('relation', '') == 'equal'

    def test_simple_not_equals_condition(self):
        filter = FilterCondition('key').ne('random').to_filter_object()

        assert filter.get('field', '') == 'key'
        assert filter.get('value', '') == 'random'
        assert filter.get('relation', '') == 'unequal'

    def test_simple_lesser_than_condition(self):
        filter = FilterCondition('key').lt('random').to_filter_object()

        assert filter.get('field', '') == 'key'
        assert filter.get('value', '') == 'random'
        assert filter.get('relation', '') == 'less'

    def test_simple_lesser_equals_condition(self):
        filter = FilterCondition('key').le('random').to_filter_object()

        assert filter.get('field', '') == 'key'
        assert filter.get('value', '') == 'random'
        assert filter.get('relation', '') == 'lessEqual'

    def test_simple_greater_than_condition(self):
        filter = FilterCondition('key').gt('random').to_filter_object()

        assert filter.get('field', '') == 'key'
        assert filter.get('value', '') == 'random'
        assert filter.get('relation', '') == 'greater'

    def test_simple_greater_equals_condition(self):
        filter = FilterCondition('key').ge('random').to_filter_object()

        assert filter.get('field', '') == 'key'
        assert filter.get('value', '') == 'random'
        assert filter.get('relation', '') == 'greaterEqual'

    def test_simple_startswith_condition(self):
        filter = FilterCondition('key').startswith('random').to_filter_object()

        assert filter.get('field', '') == 'key'
        assert filter.get('value', '') == 'random*'
        assert filter.get('relation', '') == 'equal'

    def test_condition_needs_value(self):
        filter = FilterCondition('key')

        with pytest.raises(FilterCompilationException):
            filter.to_filter_object()


class TestSimpleFilterChain:

    def test_filter_bitand_chain(self):
        f1 = FilterCondition('field').eq('value')
        f2 = FilterCondition('field2').ne('value')

        chain = f1 & f2

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter', [])) == 2

    def test_filter_bitor_chain(self):
        f1 = FilterCondition('field').eq('value')
        f2 = FilterCondition('field2').ne('value')

        chain = f1 | f2

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter', [])) == 2

    def test_empty_chain_should_throw(self):
        with pytest.raises(FilterCompilationException):
            FilterChain(FilterChainConnective.OR).to_filter_object()


class TestFilterIntoChainInsertion:

    def test_filter_ele_and_into_and(self):
        f1 = FilterCondition('field').eq('value')
        c1 = FilterCondition('field2').eq('radnom') & FilterCondition('field3').eq('something')

        chain = f1 & c1

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter', [])) == 3

    def test_filter_ele_or_into_or(self):
        f1 = FilterCondition('field').eq('value')
        c1 = FilterCondition('field2').eq('radnom') | FilterCondition('field3').eq('something')

        chain = f1 | c1

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter', [])) == 3

    def test_filter_ele_and_into_or(self):
        f1 = FilterCondition('field').eq('value')
        c1 = FilterCondition('field2').eq('radnom') | FilterCondition('field3').eq('something')

        chain = f1 & c1

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter', [])) == 2
        assert filter.get('subFilter', [])[1].get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter', [])[1].get('subFilter')) == 2

    def test_filter_ele_or_into_and(self):
        f1 = FilterCondition('field').eq('value')
        c1 = FilterCondition('field2').eq('radnom') & FilterCondition('field3').eq('something')

        chain = f1 | c1

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter', [])) == 2
        assert filter.get('subFilter', [])[1].get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter', [])[1].get('subFilter')) == 2

    def test_filter_ele_or_should_throw_for_none_element(self):
        with pytest.raises(FilterCompilationException):
            print(FilterCondition('field2').eq('radnom') | 'test')

    def test_filter_ele_or_should_throw_for_invalid_connctive(self):
        f1 = FilterCondition('field2').eq('radnom')
        fake = FilterChain('random')

        with pytest.raises(FilterCompilationException):
            print(f1 | fake)

    def test_filter_ele_and_should_throw_for_none_element(self):
        with pytest.raises(FilterCompilationException):
            print(FilterCondition('field2').eq('radnom') & 'test')

    def test_filter_ele_and_should_throw_for_invalid_connctive(self):
        f1 = FilterCondition('field2').eq('radnom')
        fake = FilterChain('random')

        with pytest.raises(FilterCompilationException):
            print(f1 & fake)


class TestFilterIntoChainAppend:

    def test_filter_ele_and_chain_and_append(self):
        f1 = FilterCondition('field').eq('value')
        c1 = FilterCondition('field2').eq('radnom') & FilterCondition('field3').eq('something')

        chain = c1 & f1

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter', [])) == 3

    def test_filter_ele_or_chain_or_append(self):
        f1 = FilterCondition('field').eq('value')
        c1 = FilterCondition('field2').eq('radnom') | FilterCondition('field3').eq('something')

        chain = c1 | f1

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter', [])) == 3

    def test_filter_ele_or_chain_and_append(self):
        f1 = FilterCondition('field').eq('value')
        c1 = FilterCondition('field2').eq('radnom') | FilterCondition('field3').eq('something')

        chain = c1 & f1

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter', [])) == 2
        assert filter.get('subFilter', [])[0].get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter', [])[0].get('subFilter')) == 2

    def test_filter_ele_and_chain_or_append(self):
        f1 = FilterCondition('field').eq('value')
        c1 = FilterCondition('field2').eq('radnom') & FilterCondition('field3').eq('something')

        chain = c1 | f1

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter', [])) == 2
        assert filter.get('subFilter', [])[0].get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter', [])[0].get('subFilter')) == 2

    def test_filter_ele_and_chain_append_invalid_should_throw(self):
        f1 = FilterCondition('field').eq('value')
        c1 = FilterCondition('field2').eq('radnom') & FilterCondition('field3').eq('something')
        c1.connective = 'random'

        with pytest.raises(FilterCompilationException):
            print(c1 & f1)

    def test_filter_ele_or_chain_append_invalid_should_throw(self):
        f1 = FilterCondition('field').eq('value')
        c1 = FilterCondition('field2').eq('radnom') & FilterCondition('field3').eq('something')
        c1.connective = 'random'

        with pytest.raises(FilterCompilationException):
            print(c1 | f1)


class TestFilterChainMerger:

    def test_chain_and_and_merge_and(self):
        c1 = FilterCondition('field2').eq('radnom') & FilterCondition('field3').eq('something')
        c2 = FilterCondition('file').eq('doc') & FilterCondition('type').eq('pdf') & FilterCondition('sig').eq('v4')

        chain = c1 & c2

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter', [])) == 5

    def test_chain_and_or_merge_and(self):
        c1 = FilterCondition('field2').eq('radnom') & FilterCondition('field3').eq('something')
        c2 = FilterCondition('file').eq('doc') | FilterCondition('type').eq('pdf') | FilterCondition('sig').eq('v4')

        chain = c1 & c2

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter', [])) == 3
        assert filter.get('subFilter')[2].get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter')[2].get('subFilter')) == 3

    def test_chain_or_and_merge_and(self):
        c1 = FilterCondition('field2').eq('radnom') | FilterCondition('field3').eq('something')
        c2 = FilterCondition('file').eq('doc') & FilterCondition('type').eq('pdf') & FilterCondition('sig').eq('v4')

        chain = c1 & c2

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter', [])) == 4
        assert filter.get('subFilter')[0].get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter')[0].get('subFilter')) == 2

    def test_chain_or_or_merge_and(self):
        c1 = FilterCondition('field2').eq('radnom') | FilterCondition('field3').eq('something')
        c2 = FilterCondition('file').eq('doc') | FilterCondition('type').eq('pdf') | FilterCondition('sig').eq('v4')

        chain = c1 & c2

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter', [])) == 2
        assert filter.get('subFilter')[0].get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter')[0].get('subFilter')) == 2
        assert filter.get('subFilter')[1].get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter')[1].get('subFilter')) == 3

    def test_chain_and_should_throw_if_invalid_connective(self):
        c1 = FilterCondition('field2').eq('radnom') | FilterCondition('field3').eq('something')
        c2 = FilterCondition('file').eq('doc') & FilterCondition('type').eq('pdf') & FilterCondition('sig').eq('v4')

        c1.connective = 'random'

        with pytest.raises(FilterCompilationException):
            print(c1 & c2)

    def test_chain_or_or_merge_or(self):
        c1 = FilterCondition('field2').eq('radnom') | FilterCondition('field3').eq('something')
        c2 = FilterCondition('file').eq('doc') | FilterCondition('type').eq('pdf') | FilterCondition('sig').eq('v4')

        chain = c1 | c2

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter', [])) == 5

    def test_chain_or_and_merge_or(self):
        c1 = FilterCondition('field2').eq('radnom') | FilterCondition('field3').eq('something')
        c2 = FilterCondition('file').eq('doc') & FilterCondition('type').eq('pdf') & FilterCondition('sig').eq('v4')

        chain = c1 | c2

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter', [])) == 3
        assert filter.get('subFilter')[2].get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter')[2].get('subFilter')) == 3

    def test_chain_and_or_merge_or(self):
        c1 = FilterCondition('field2').eq('radnom') & FilterCondition('field3').eq('something')
        c2 = FilterCondition('file').eq('doc') | FilterCondition('type').eq('pdf') | FilterCondition('sig').eq('v4')

        chain = c1 | c2

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter', [])) == 4
        assert filter.get('subFilter')[0].get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter')[0].get('subFilter')) == 2

    def test_chain_and_and_merge_or(self):
        c1 = FilterCondition('field2').eq('radnom') & FilterCondition('field3').eq('something')
        c2 = FilterCondition('file').eq('doc') & FilterCondition('type').eq('pdf') & FilterCondition('sig').eq('v4')

        chain = c1 | c2

        filter = chain.to_filter_object()

        assert filter is not None
        assert filter.get('subFilterConnective') == 'or'
        assert len(filter.get('subFilter', [])) == 2
        assert filter.get('subFilter')[0].get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter')[0].get('subFilter')) == 2
        assert filter.get('subFilter')[1].get('subFilterConnective') == 'and'
        assert len(filter.get('subFilter')[1].get('subFilter')) == 3

    def test_chain_or_should_throw_if_invalid_connective(self):
        c1 = FilterCondition('field2').eq('radnom') | FilterCondition('field3').eq('something')
        c2 = FilterCondition('file').eq('doc') & FilterCondition('type').eq('pdf') & FilterCondition('sig').eq('v4')

        c1.connective = 'random'

        with pytest.raises(FilterCompilationException):
            print(c1 | c2)
