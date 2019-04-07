"""core SalesSystem module"""

# pylint: disable=unused-import

from app.core.models import db
from app.core.models.user import User
from app.core.models.order import Order
from app.core.models.inventory import Item, IngredientGroup, Stock


class SalesSystem:
  """core SalesSystem class"""

  def __init__(self, app):
    self.app = app
    db.init_app(self.app)

  def InitializeDb(self, skeleton=False):
    """Create db schema and populate it with default inventory data"""
    with self.app.app_context():
      db.create_all()

      if not skeleton:
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

        burger = Item(name="Burger", root=False, price=9.99)
        db.session.add(burger)
        main_type_group.options.append(burger)

        bun_group = IngredientGroup(
            name="Bun", max_item=3, min_item=2, max_option=1, min_option=1)
        db.session.add(bun_group)
        burger.ingredientgroups.append(bun_group)

        muffin_bun = Item(
            name="Muffin Bun", root=False, identical=True, price=0.99)
        sesame_bun = Item(
            name="Sesame Bun", root=False, identical=True, price=0.99)
        standard_bun = Item(name="Standard Bun", root=False, identical=True)
        db.session.add(muffin_bun)
        db.session.add(sesame_bun)
        db.session.add(standard_bun)
        bun_group.options.append(muffin_bun)
        bun_group.options.append(sesame_bun)
        bun_group.options.append(standard_bun)

        wrap = Item(name="Wrap", root=False)
        db.session.add(wrap)
        main_type_group.options.append(wrap)

        patty_group = IngredientGroup(
            name="Patties", max_item=3, min_item=1, max_option=3, min_option=1)
        db.session.add(patty_group)
        main.ingredientgroups.append(patty_group)

        chicken_patty = Item(
            name="Chicken Patty", root=False, identical=True, price=0.99)
        beef_patty = Item(
            name="Beef Patty", root=False, identical=True, price=1.99)
        vegetarian_patty = Item(
            name="Vegetarian Patty", root=False, identical=True, price=0.99)
        db.session.add(chicken_patty)
        db.session.add(beef_patty)
        db.session.add(vegetarian_patty)
        patty_group.options.append(chicken_patty)
        patty_group.options.append(beef_patty)
        patty_group.options.append(vegetarian_patty)

        ingredients = IngredientGroup(
            name="Other Ingredients", max_item=5, max_option=5)
        db.session.add(ingredients)
        main.ingredientgroups.append(ingredients)

        tomato = Item(name="Tomato", root=False, identical=True, price=0.99)
        tomato_sauce = Item(
            name="Tomato Sauce", root=False, identical=True, price=0.99)
        bbq_sauce = Item(
            name="BBQ Sauce", root=False, identical=True, price=0.99)
        cheddar_cheese = Item(
            name="Cheddar Cheese", root=False, identical=True, price=0.99)
        db.session.add(tomato)
        db.session.add(tomato_sauce)
        db.session.add(bbq_sauce)
        db.session.add(cheddar_cheese)
        ingredients.options.append(tomato)
        ingredients.options.append(tomato_sauce)
        ingredients.options.append(bbq_sauce)
        ingredients.options.append(cheddar_cheese)

        nuggets = Item(name="Nuggets", root=True, price=1.99)
        db.session.add(nuggets)

        nuggets_amount = IngredientGroup(
            name="Nuggets Amount",
            max_item=1,
            min_item=1,
            max_option=1,
            min_option=1)
        db.session.add(nuggets)
        nuggets.ingredientgroups.append(nuggets_amount)

        nuggets_3_pack = Item(
            name="3-pack Nuggets", root=False, identical=True, price=0)
        nuggets_6_pack = Item(
            name="6-pack Nuggets", root=False, identical=True, price=1)
        nuggets_12_pack = Item(
            name="12-pack Nuggets", root=False, identical=True, price=2)
        db.session.add(nuggets_3_pack)
        db.session.add(nuggets_6_pack)
        db.session.add(nuggets_12_pack)
        nuggets_amount.options.append(nuggets_3_pack)
        nuggets_amount.options.append(nuggets_6_pack)
        nuggets_amount.options.append(nuggets_12_pack)

        fries = Item(name="Fries", root=True, price=1.99)
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

        tomato_sauce = Item(
            name="Tomato Sauce",
            root=False,
            identical=True,
            price=0,
            max_item=1)
        bbq_sauce = Item(name="BBQ Sauce", root=False, identical=True, price=1)
        chilli_sauce = Item(
            name="Chilli Sauce", root=False, identical=True, price=1)
        db.session.add(tomato_sauce)
        db.session.add(bbq_sauce)
        db.session.add(chilli_sauce)
        sauce.options.append(tomato_sauce)
        sauce.options.append(bbq_sauce)
        sauce.options.append(chilli_sauce)

        coke = Item(name="Coke", root=True, price=1.99)
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
