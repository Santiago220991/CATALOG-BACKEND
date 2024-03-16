def test_list_all(product_repository, session, fake_database_product_list):

    [productA, productB] = fake_database_product_list
    session.add(productA)
    session.add(productB)
    session.commit()

    products = product_repository.list_all()
    assert len(products) == 2
    assert productA.name == products[0].name
    assert productB.name == products[1].name


def test_filter(product_repository, session, fake_database_product_list):
    [productA, productB] = fake_database_product_list
    session.add(productA)
    session.add(productB)
    session.commit()

    products = product_repository.filter("New")
    if len(products) > 0:
        for product in products:
            assert product.status == "New"
    else:
        assert products == []
