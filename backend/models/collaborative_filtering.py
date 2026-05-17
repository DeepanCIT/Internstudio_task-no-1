"""
Collaborative Filtering Recommendation Model
- User-User CF  : find users with similar taste, recommend what they liked
- Item-Item CF  : find items similar to what the user already rated / bought
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class CollaborativeFiltering:
    def __init__(self):
        self.user_item_matrix = None
        self.user_similarity  = None
        self.item_similarity  = None

    # ------------------------------------------------------------------ #
    #  Build                                                               #
    # ------------------------------------------------------------------ #
    def build_matrix(self, ratings_data: list[tuple]) -> pd.DataFrame | None:
        """
        ratings_data : list of (user_id, product_id, rating)
        """
        self.user_item_matrix = None
        self.user_similarity  = None
        self.item_similarity  = None

        if len(ratings_data) < 2:
            return None

        df = pd.DataFrame(ratings_data, columns=['user_id', 'product_id', 'rating'])
        self.user_item_matrix = df.pivot_table(
            index='user_id', columns='product_id',
            values='rating', fill_value=0
        )

        if len(self.user_item_matrix) > 1:
            self.user_similarity = cosine_similarity(self.user_item_matrix)
        if len(self.user_item_matrix.columns) > 1:
            self.item_similarity = cosine_similarity(self.user_item_matrix.T)

        return self.user_item_matrix

    # ------------------------------------------------------------------ #
    #  User-User CF                                                        #
    # ------------------------------------------------------------------ #
    def get_user_recommendations(self, user_id: int, n: int = 10) -> list[int]:
        if (self.user_item_matrix is None
            or self.user_similarity is None
            or user_id not in self.user_item_matrix.index):
            return []

        user_idx   = list(self.user_item_matrix.index).index(user_id)
        sim_scores = sorted(enumerate(self.user_similarity[user_idx]),
                            key=lambda x: x[1], reverse=True)

        # top-5 similar users (excluding self)
        similar_users = [self.user_item_matrix.index[i]
                         for i, _ in sim_scores[1:6]]

        already_rated = set(
            self.user_item_matrix.loc[user_id][
                self.user_item_matrix.loc[user_id] > 0
            ].index
        )

        candidates: dict[int, float] = {}
        for su in similar_users:
            for pid, rating in self.user_item_matrix.loc[su].items():
                if pid not in already_rated and rating > 0:
                    candidates[pid] = candidates.get(pid, 0) + rating

        sorted_c = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        return [int(pid) for pid, _ in sorted_c[:n]]

    # ------------------------------------------------------------------ #
    #  Item-Item CF                                                        #
    # ------------------------------------------------------------------ #
    def get_item_recommendations(self, product_id: int, n: int = 10) -> list[int]:
        if (self.user_item_matrix is None
            or self.item_similarity is None
            or product_id not in self.user_item_matrix.columns):
            return []

        item_idx   = list(self.user_item_matrix.columns).index(product_id)
        sim_scores = sorted(enumerate(self.item_similarity[item_idx]),
                            key=lambda x: x[1], reverse=True)

        return [int(self.user_item_matrix.columns[i])
                for i, _ in sim_scores[1:n + 1]]
