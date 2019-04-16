"""Module to test the order model module"""
import pytest
from app.core.models.inventory import Stock, Item, IngredientGroup
from app.core.models.order import Order
from app.core.models import db


def test_create_order(app):
  """Test creating order and adding items to it"""
  with app.app_context():
    sburger = Stock(name="burger", amount=3)
    swrap = Stock(name="wrap", amount=0)
    db.session.add(sburger)
    db.session.add(swrap)
    imain = Item(name="main")
    iburger = Item(name="burger")
    iwrap = Item(name="wrap")
    gtype = IngredientGroup(
        name="type", min_item=1, max_item=1, min_option=1, max_option=1)
    db.session.add(imain)
    db.session.add(iburger)
    db.session.add(iwrap)
    db.session.add(gtype)
    sburger.items.append(iburger)
    swrap.items.append(iwrap)
    gtype.options.append(iburger)
    gtype.options.append(iwrap)
    imain.ingredientgroups.append(gtype)
    db.session.commit()

    order = Order()
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("0.0", [iburger.GetID()], [1])
    order.AddRootItem(imain.GetID(), 1)
    with pytest.raises(RuntimeError):
      order.AddIG("0.0", [iburger.GetID()], [1])
    with pytest.raises(ValueError):
      order.AddIG("1.0", [iburger.GetID()], [2])
    with pytest.raises(ValueError):
      order.AddIG("1.0", [], [])
    with pytest.raises(RuntimeError):
      order.AddIG("1.0", [iwrap.GetID()], [1])
    swrap.IncreaseAmount(1)
    order.AddIG("1.0", [iwrap.GetID()], [1])


def test_order_details_string(app):
  """ Test GetDetailsString in Order class
  """
  with app.app_context():
    sburger = Stock(name="burger", amount=1)
    swrap = Stock(name="wrap", amount=1)
    db.session.add(sburger)
    db.session.add(swrap)
    imain = Item(name="main", price=0)
    iburger = Item(name="burger", price=5)
    iwrap = Item(name="wrap", price=3.3)
    gtype = IngredientGroup(
        name="type", min_item=1, max_item=1, min_option=1, max_option=1)
    db.session.add(imain)
    db.session.add(iburger)
    db.session.add(iwrap)
    db.session.add(gtype)
    sburger.items.append(iburger)
    swrap.items.append(iwrap)
    gtype.options.append(iburger)
    gtype.options.append(iwrap)
    imain.ingredientgroups.append(gtype)
    db.session.commit()

    order = Order()
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("0.0", [iburger.GetID()], [1])
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("1.0", [iwrap.GetID()], [1])

    assert order.GetDetailsString() == """main\n  type:burger ......$5.00\nmain
  type:wrap ......$3.30\n\n\nTotal price: $8.30"""


def test_pay_order_1(app):
  """ Test pay for order
  """
  with app.app_context():
    sburger = Stock(name="burger", amount=3)
    swrap = Stock(name="wrap", amount=3)
    db.session.add(sburger)
    db.session.add(swrap)
    imain = Item(name="main", price=0)
    iburger = Item(name="burger", price=5)
    iwrap = Item(name="wrap", price=3.3, stock_unit=2)
    gtype = IngredientGroup(
        name="type", min_item=1, max_item=1, min_option=1, max_option=1)
    db.session.add(imain)
    db.session.add(iburger)
    db.session.add(iwrap)
    db.session.add(gtype)
    sburger.items.append(iburger)
    swrap.items.append(iwrap)
    gtype.options.append(iburger)
    gtype.options.append(iwrap)
    imain.ingredientgroups.append(gtype)
    db.session.commit()

    order = Order()
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("0.0", [iburger.GetID()], [1])
    assert order.GetPrice() == 5
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("1.0", [iwrap.GetID()], [1])
    assert order.GetPrice() == 8.3
    db.session.add(order)
    db.session.commit()

    order.Pay()
    db.session.commit()

    assert order.GetStatus() == 1  # paid
    assert order.GetPrice() == 8.3
    assert sburger.GetAmount() == 2
    assert swrap.GetAmount() == 1

def test_pay_order_2(app):
  """ Test pay order with complicated types of food
  """
  with app.app_context():
    main = Item(name="Main", root=True)
    db.session.add(main)

    main_type_group = IngredientGroup(
        name="Main Type",
        max_item=1,
        min_item=1,
        max_option=1,
        min_option=1)

    main.ingredientgroups.append(main_type_group)
    db.session.add(main_type_group)

    burger = Item(name="Burger", root=False, price=10)
    db.session.add(burger)

    main_type_group.options.append(burger)
    bun_group = IngredientGroup(
        name="Bun", max_item=3, min_item=2, max_option=1, min_option=1)
    db.session.add(bun_group)
    burger.ingredientgroups.append(bun_group)

    muffin_bun = Item(
        name="Muffin Bun", root=False, identical=True, price=1)
    sesame_bun = Item(
        name="Sesame Bun", root=False, identical=True, price=2)
    standard_bun = Item(name="Standard Bun", root=False, identical=True, price=1)

    db.session.add(muffin_bun)
    db.session.add(sesame_bun)
    db.session.add(standard_bun)

    bun_group.options.append(muffin_bun)
    bun_group.options.append(sesame_bun)
    bun_group.options.append(standard_bun)

    wrap = Item(name="Wrap", root=False, price=5)
    db.session.add(wrap)
    main_type_group.options.append(wrap)

    patty_group = IngredientGroup(
        name="Patties", max_item=3, min_item=1, max_option=3, min_option=1)
    db.session.add(patty_group)
    main.ingredientgroups.append(patty_group)
    chicken_patty = Item(
        name="Chicken Patty", root=False, identical=True, price=4)
    beef_patty = Item(
        name="Beef Patty", root=False, identical=True, price=5)
    vegetarian_patty = Item(
        name="Vegetarian Patty", root=False, identical=True, price=3)
    tuna_patty = Item(
        name="Tuna Patty", root=False, identical=True, price=3)

    db.session.add(chicken_patty)
    db.session.add(beef_patty)
    db.session.add(vegetarian_patty)
    db.session.add(tuna_patty)

    patty_group.options.append(chicken_patty)
    patty_group.options.append(beef_patty)
    patty_group.options.append(vegetarian_patty)
    patty_group.options.append(tuna_patty)

    ingredients = IngredientGroup(
        name="Other Ingredients", max_item=5, max_option=5)
    db.session.add(ingredients)
    main.ingredientgroups.append(ingredients)
    tomato = Item(name="Tomato", root=False, identical=True, price=1)
    tomato_sauce = Item(
        name="Tomato Sauce", root=False, identical=True, price=0.5)
    bbq_sauce = Item(
        name="BBQ Sauce", root=False, identical=True, price=0.5)
    mint_sauce = Item(
        name="mint Sauce", root=False, identical=True, price=0.5)
    chocolate_sauce = Item(
        name="chocolate_sauce", root=False, identical=True, price=0.5)
    cheddar_cheese = Item(
        name="Cheddar Cheese", root=False, identical=True, price=0.5)
    db.session.add(tomato)
    db.session.add(tomato_sauce)
    db.session.add(bbq_sauce)
    db.session.add(mint_sauce)
    db.session.add(chocolate_sauce)
    db.session.add(cheddar_cheese)

    ingredients.options.append(tomato)
    ingredients.options.append(tomato_sauce)
    ingredients.options.append(bbq_sauce)
    ingredients.options.append(mint_sauce)
    ingredients.options.append(chocolate_sauce)
    ingredients.options.append(cheddar_cheese)
    nuggets = Item(name="Nuggets", root=True, price=2)
    db.session.add(nuggets)
    nuggets_amount = IngredientGroup(
        name="Nuggets Amount",
        max_item=1,
        min_item=1,
        max_option=1,
        min_option=1)

    nuggets.ingredientgroups.append(nuggets_amount)
    nuggets_3_pack = Item(
        name="3-pack Nuggets", root=False, identical=True, price=6)
    nuggets_6_pack = Item(
        name="6-pack Nuggets", root=False, identical=True, price=12)
    nuggets_12_pack = Item(
        name="12-pack Nuggets", root=False, identical=True, price=18)
    db.session.add(nuggets_3_pack)
    db.session.add(nuggets_6_pack)
    db.session.add(nuggets_12_pack)
    nuggets_amount.options.append(nuggets_3_pack)
    nuggets_amount.options.append(nuggets_6_pack)
    nuggets_amount.options.append(nuggets_12_pack)

    fries = Item(name="Fries", root=True, price=2)
    db.session.add(fries)

    fries_size = IngredientGroup(
        name="fries Size",
        max_item=1,
        min_item=1,
        max_option=1,
        min_option=1)
    db.session.add(fries_size)

    fries.ingredientgroups.append(fries_size)
    small_size = Item(
        name="Small Fries", root=False, identical=True, price=0)
    medium_size = Item(
        name="Medium Fries", root=False, identical=True, price=1)
    large_size = Item(
        name="Large Fries", root=False, identical=True, price=2)
    db.session.add(small_size)
    db.session.add(medium_size)
    db.session.add(large_size)

    fries_size.options.append(small_size)
    fries_size.options.append(medium_size)
    fries_size.options.append(large_size)

    sauce = IngredientGroup(name="Sauce", max_item=3, max_option=3)
    db.session.add(sauce)
    nuggets.ingredientgroups.append(sauce)
    fries.ingredientgroups.append(sauce)
    chilli_sauce = Item(
        name="Chilli Sauce", root=False, identical=True, price=1)
    db.session.add(chilli_sauce)

    sauce.options.append(tomato_sauce)
    sauce.options.append(bbq_sauce)
    sauce.options.append(chilli_sauce)
    sauce.options.append(mint_sauce)

    coke = Item(name="Coke", root=True, price=0)
    db.session.add(coke)
    coke_size = IngredientGroup(
        name="Coke Size",
        max_item=1,
        min_item=1,
        max_option=1,
        min_option=1)
    db.session.add(coke_size)
    coke.ingredientgroups.append(coke_size)
    small_coke = Item(
        name="Small Coke", root=False, identical=True, price=0)
    medium_coke = Item(
        name="Medium Coke", root=False, identical=True, price=1)
    large_coke = Item(
        name="Large Coke", root=False, identical=True, price=2)
    db.session.add(small_coke)
    db.session.add(medium_coke)
    db.session.add(large_coke)
    coke_size.options.append(small_coke)
    coke_size.options.append(medium_coke)
    coke_size.options.append(large_coke)
    db.session.commit()

    order = Order()

    # Add first main.
    order.AddRootItem(main.GetID(), 1)
    order.AddIG("0.0", [burger.GetID()], [1])
    assert order.GetPrice() == 10

    # Can't complete the order without choosing at least one bun.
    with pytest.raises(RuntimeError):
        order.Pay()

    # Customer can't order less than 1 bun or more than 3 buns.
    with pytest.raises(ValueError):
        order.AddIG("0.0.0.0", [muffin_bun.GetID()], [1])

    with pytest.raises(ValueError):
        order.AddIG("0.0.0.0", [muffin_bun.GetID()], [4])

    order.AddIG("0.0.0.0", [muffin_bun.GetID()], [2])
    assert order.GetPrice() == 12

    # Can't complete the order without choosing at least one patty.
    with pytest.raises(RuntimeError):
        order.Pay()

    # Can't choose more than three types of patties.
    with pytest.raises(ValueError):
        order.AddIG("0.1", [chicken_patty.GetID(), beef_patty.GetID(), vegetarian_patty.GetID(), tuna_patty.GetID()], [1,1,1,1])

    # Can't choose more than three patties.
    with pytest.raises(ValueError):
        order.AddIG("0.1", [chicken_patty.GetID(), beef_patty.GetID(), vegetarian_patty.GetID()], [1,1,2])

    # Customer can't choose zero patties or more than 4 patties.
    with pytest.raises(ValueError):
        order.AddIG("0.1", [chicken_patty.GetID()], [0])

    with pytest.raises(ValueError):
        order.AddIG("0.1", [chicken_patty.GetID()], [4])

    order.AddIG("0.1", [chicken_patty.GetID()], [3])

    assert order.GetPrice() == 24

    # Patty has been fulfilled so RuntimeError is raised.
    with pytest.raises(RuntimeError):
        order.AddIG("0.1", [beef_patty.GetID()], [3])

    # Can't choose more than five types of ingredients.
    with pytest.raises(ValueError):
        order.AddIG("0.2", [tomato.GetID(), tomato_sauce.GetID(), bbq_sauce.GetID(), mint_sauce.GetID(), chocolate_sauce.GetID(), cheddar_cheese.GetID()], [1, 1, 1, 1, 1, 1])

    # Can't choose more than five ingredients with more than one ingredient.
    with pytest.raises(ValueError):
        order.AddIG("0.2", [tomato.GetID(), tomato_sauce.GetID(), bbq_sauce.GetID(), mint_sauce.GetID(), cheddar_cheese.GetID()], [1, 1, 2, 1, 1])

    # Can't choose more than five ingredients with one ingredient.
    with pytest.raises(ValueError):
        order.AddIG("0.2", [tomato.GetID()], [6])

    order.AddIG("0.2", [tomato.GetID(), tomato_sauce.GetID(), bbq_sauce.GetID(), mint_sauce.GetID(), cheddar_cheese.GetID()], [1, 1, 1, 1, 1])
    assert order.GetPrice() == 27

    # Add second main.
    order.AddRootItem(main.GetID(), 1)
    order.AddIG("1.0", [wrap.GetID()], [1])
    assert order.GetPrice() == 32

    order.AddIG("1.1", [chicken_patty.GetID()], [3])
    assert order.GetPrice() == 44

    order.AddIG("1.2", [tomato.GetID()], [2])
    assert order.GetPrice() == 46

    order.AddRootItem(nuggets.GetID(), 1)

    # Can't choose more than one nuggets pack.
    with pytest.raises(ValueError):
        order.AddIG("2.0", [nuggets_3_pack.GetID()], [2])

    # Can't choose more than one type of nuggets pack.
    with pytest.raises(ValueError):
        order.AddIG("2.0", [nuggets_3_pack.GetID(), nuggets_3_pack.GetID()], [1, 1])

    order.AddIG("2.0", [nuggets_3_pack.GetID()], [1])

    # Can't pay before configure any sauces for nuggets.
    with pytest.raises(RuntimeError):
        order.Pay()

    # Can't choose more than three sauces.
    with pytest.raises(ValueError):
        order.AddIG("2.1", [tomato_sauce.GetID()], [4])

    # Can't choose more than three types of sauces.
    with pytest.raises(ValueError):
        order.AddIG("2.1", [tomato_sauce.GetID(), bbq_sauce.GetID(), chilli_sauce.GetID(), mint_sauce.GetID()], [1, 1, 1, 1])
 
    order.AddIG("2.1", [tomato_sauce.GetID()], [0])
    assert order.GetPrice() == 54

    order.AddRootItem(fries.GetID(), 1)

    # Can't pay without choosing a pack of fries.
    with pytest.raises(RuntimeError):
        order.Pay()

    # Can't choose more than one pack of fries.
    with pytest.raises(ValueError):
        order.AddIG("3.0", [small_size.GetID()], [2])

    # Can't choose more than one type of fries.
    with pytest.raises(ValueError):
        order.AddIG("3.0", [small_size.GetID(), medium_size.GetID()], [1, 1])

    order.AddIG("3.0", [small_size.GetID()], [1])
    assert order.GetPrice() == 56

    # Can't pay without choosing any sauces.
    with pytest.raises(RuntimeError):
        order.Pay()

    # Can't choose more than three sauces.
    with pytest.raises(ValueError):
        order.AddIG("3.1", [tomato_sauce.GetID()], [4])

    # Can't choose more than three types of sauces.
    with pytest.raises(ValueError):
        order.AddIG("3.1", [tomato_sauce.GetID(), bbq_sauce.GetID(), chilli_sauce.GetID(), mint_sauce.GetID()], [1, 1, 1, 1])
 
    order.AddIG("3.1", [tomato_sauce.GetID()], [0])

    order.AddRootItem(coke.GetID(), 1)

    # Can't pay without choosing a coke.
    with pytest.raises(RuntimeError):
        order.Pay()

    # Can't choose more than one coke.
    with pytest.raises(ValueError):
        order.AddIG("4.0", [small_coke.GetID()], [2])

    # Can't choose more than one type of coke.
    with pytest.raises(ValueError):
        order.AddIG("4.0", [small_coke.GetID(), medium_coke.GetID()], [1, 1])

    order.AddIG("4.0", [medium_coke.GetID()], [1])
    assert order.GetPrice() == 57
    
    db.session.add(order)
    db.session.commit()

    order.Pay()
    db.session.commit()

    assert order.GetStatus() == 1  # paid
    assert order.GetPrice() == 57
