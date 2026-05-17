"""
Hybrid Recommendation Model
Combines Collaborative Filtering (CF) + Content-Based Filtering (CB)
using a weighted reciprocal-rank fusion strategy.
"""

from .collaborative_filtering import CollaborativeFiltering
from .content_based import ContentBasedFiltering


class HybridRecommender:
    def __init__(
        self,
        cf_model:  CollaborativeFiltering,
        cb_model:  ContentBasedFiltering,
        cf_weight: float = 0.5,
        cb_weight: float = 0.5
    ):
        self.cf_model  = cf_model
        self.cb_model  = cb_model
        self.cf_weight = cf_weight
        self.cb_weight = cb_weight

    # ------------------------------------------------------------------ #
    #  Main entry point                                                    #
    # ------------------------------------------------------------------ #
    def get_recommendations(
        self,
        user_id:              int,
        browsed_product_ids:  list[int],
        purchased_product_ids: list[int] | None = None,
        n:                    int = 10
    ) -> list[int]:
        pool = (browsed_product_ids or []) + (purchased_product_ids or [])

        cf_recs = self.cf_model.get_user_recommendations(user_id, n=n * 2)
        cb_recs = self.cb_model.get_user_profile_recommendations(pool, n=n * 2)

        scores: dict[int, float] = {}

        for rank, pid in enumerate(cf_recs):
            scores[pid] = scores.get(pid, 0) + self.cf_weight * (1.0 / (rank + 1))

        for rank, pid in enumerate(cb_recs):
            scores[pid] = scores.get(pid, 0) + self.cb_weight * (1.0 / (rank + 1))

        sorted_pids = [pid for pid, _ in
                       sorted(scores.items(), key=lambda x: x[1], reverse=True)]

        # Fallback: fill with CB-only results when CF has nothing
        if len(sorted_pids) < n:
            for pid in cb_recs:
                if pid not in sorted_pids:
                    sorted_pids.append(pid)
                if len(sorted_pids) >= n:
                    break

        # Final fallback: CF item-based similarity from most-recent browse
        if len(sorted_pids) < n and browsed_product_ids:
            item_based = self.cf_model.get_item_recommendations(
                browsed_product_ids[-1], n=n
            )
            for pid in item_based:
                if pid not in sorted_pids:
                    sorted_pids.append(pid)
                if len(sorted_pids) >= n:
                    break

        return [int(p) for p in sorted_pids[:n]]

    # ------------------------------------------------------------------ #
    #  "Similar products" widget (product-detail page)                    #
    # ------------------------------------------------------------------ #
    def get_similar_products(self, product_id: int, n: int = 8) -> list[int]:
        cb_sims = self.cb_model.get_similar_products(product_id, n=n * 2)
        cf_sims = self.cf_model.get_item_recommendations(product_id, n=n * 2)

        scores: dict[int, float] = {}
        for rank, pid in enumerate(cb_sims):
            scores[pid] = scores.get(pid, 0) + 0.6 * (1.0 / (rank + 1))
        for rank, pid in enumerate(cf_sims):
            scores[pid] = scores.get(pid, 0) + 0.4 * (1.0 / (rank + 1))

        return [int(pid) for pid, _ in
                sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]]
