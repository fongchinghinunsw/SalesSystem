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

        burger = Item(name="Burger", root=False)
        db.session.add(burger)
        main_type_group.options.append(burger)

        bun_group = IngredientGroup(
            name="Bun", max_item=3, min_item=2, max_option=1, min_option=1)
        db.session.add(bun_group)
        burger.ingredientgroups.append(bun_group)

        muffin_bun = Item(name="Muffin Bun", root=False)
        sesame_bun = Item(name="Sesame Bun", root=False)
        standard_bun = Item(name="Standard Bun", root=False)
        db.session.add(muffin_bun)
        db.session.add(sesame_bun)
        db.session.add(standard_bun)
        bun_group.options.append(muffin_bun)
        bun_group.options.append(sesame_bun)
        bun_group.options.append(standard_bun)

        wrap = Item(name="Wrap", root=False)
        db.session.add(wrap)
        main_type_group.options.append(wrap)

        db.session.commit()
