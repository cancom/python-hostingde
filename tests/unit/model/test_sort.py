from hostingde.model.sort import SortConfiguration, SortOrder


def test_sort_constructor():
    sort = SortConfiguration(field="test", order=SortOrder.ASC)

    assert sort.field == "test"
    assert sort.order == SortOrder.ASC


def test_sort_dump():
    # TODO: Enum by_value fix
    sort = SortConfiguration(field="test", order=SortOrder.ASC)

    assert sort.to_json() == dict(field="test", order="ASC")
