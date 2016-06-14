# -*- coding:utf-8 -*-

from bro.models import Bro, friendship
from main.extensions import db
from sqlalchemy import asc, desc, func


class OrderBy(object):
    @staticmethod
    def get_bros():
        return db.session.query(Bro)

    @staticmethod
    def get_bros_friends_qty():
        friends_qty = func.count(friendship.c.bro_id).label('friends_qty')
        bros_friends = db.session.query(Bro) \
            .outerjoin(friendship, Bro.id == friendship.c.bro_id) \
            .group_by(Bro.id) \
            .add_columns(Bro.id, Bro.username, friends_qty)
        return bros_friends

    def execute(self):
        return self.get_bros()


class OrderByNameAsc(OrderBy):
    def execute(self):
        bros = super(OrderByNameAsc, self).get_bros()
        return bros.order_by(asc(Bro.username))


class OrderByNameDesc(OrderBy):
    def execute(self):
        bros = super(OrderByNameDesc, self).get_bros()
        return bros.order_by(desc(Bro.username))


class OrderByFriendsQtyAsc(OrderBy):
    def execute(self):
        bros_friends = super(OrderByFriendsQtyAsc, self).get_bros_friends_qty()
        return bros_friends.order_by(asc('friends_qty'))


class OrderByFriendsQtyDesc(OrderBy):
    def execute(self):
        bros_friends = super(OrderByFriendsQtyDesc, self).get_bros_friends_qty()
        return bros_friends.order_by(desc('friends_qty'))


class SortStrategy(object):
    def __init__(self, strategy=''):
        self.strategy = strategy

    def _get_strategy_class(self):
        strategy_class = OrderBy
        if self.strategy == 'name_asc':
            strategy_class = OrderByNameAsc
        elif self.strategy == 'name_desc':
            strategy_class = OrderByNameDesc
        elif self.strategy == 'friends_qty_asc':
            strategy_class = OrderByFriendsQtyAsc
        elif self.strategy == 'friends_qty_desc':
            strategy_class = OrderByFriendsQtyDesc
        return strategy_class

    def get_result(self, page=1, per_page=10):
        order_class = self._get_strategy_class()
        result = order_class().execute()
        total = result.count()
        per_page_bros = result.offset(per_page * (page - 1)).limit(per_page)
        return total, per_page_bros
