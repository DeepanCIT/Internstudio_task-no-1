"""
Content-Based Filtering Recommendation Model
Uses TF-IDF on product metadata (name, description, category, tags, brand)
to find products similar to what a user has interacted with.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedFiltering:
    def __init__(self):
        self.tfidf_matrix = None
        self.product_ids  = []
        self.vectorizer   = TfidfVectorizer(
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2)
        )

    # ------------------------------------------------------------------ #
    #  Build product profiles                                             #
    # ------------------------------------------------------------------ #
    def build_profile(self, products_data: list[dict]) -> None:
        if not products_data:
            return

        df = pd.DataFrame(products_data)
        self.product_ids = df['id'].tolist()

        def _normalize_tags(value) -> str:
            if isinstance(value, list):
                return " ".join([str(tag).strip() for tag in value if tag])
            if value is None:
                return ""
            return str(value)

        df['tags'] = df['tags'].apply(_normalize_tags)

        # Concatenate all text features into a single "document"
        df['content'] = (
            df['name'].fillna('')        + ' ' +
            df['description'].fillna('') + ' ' +
            df['category'].fillna('')    + ' ' +
            df['subcategory'].fillna('') + ' ' +
            df['tags'].fillna('')        + ' ' +
            df['brand'].fillna('')
        ).str.lower()

        self.tfidf_matrix = self.vectorizer.fit_transform(df['content'])

    # ------------------------------------------------------------------ #
    #  Similar products (item → items)                                    #
    # ------------------------------------------------------------------ #
    def get_similar_products(self, product_id: int, n: int = 10) -> list[int]:
        if self.tfidf_matrix is None or product_id not in self.product_ids:
            return []

        idx        = self.product_ids.index(product_id)
        cosine_sim = cosine_similarity(
            self.tfidf_matrix[idx], self.tfidf_matrix
        ).flatten()

        sim_scores = sorted(enumerate(cosine_sim),
                            key=lambda x: x[1], reverse=True)
        sim_scores = [s for s in sim_scores if s[0] != idx]
        return [int(self.product_ids[i]) for i, _ in sim_scores[:n]]

    # ------------------------------------------------------------------ #
    #  Personalised recs from browsing / purchase history                 #
    # ------------------------------------------------------------------ #
    def get_user_profile_recommendations(
        self,
        interacted_product_ids: list[int],
        n: int = 10
    ) -> list[int]:
        if self.tfidf_matrix is None or not interacted_product_ids:
            return []

        valid = [pid for pid in interacted_product_ids if pid in self.product_ids]
        if not valid:
            return []

        indices      = [self.product_ids.index(pid) for pid in valid]
        user_profile = np.mean(self.tfidf_matrix[indices].toarray(), axis=0)

        cosine_sim = cosine_similarity(
            user_profile.reshape(1, -1), self.tfidf_matrix
        ).flatten()

        sim_scores = sorted(enumerate(cosine_sim),
                            key=lambda x: x[1], reverse=True)
        # exclude already-interacted products
        interacted_set = set(interacted_product_ids)
        sim_scores = [s for s in sim_scores
                      if self.product_ids[s[0]] not in interacted_set]

        return [int(self.product_ids[i]) for i, _ in sim_scores[:n]]
