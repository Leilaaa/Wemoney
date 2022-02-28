import pandas as pd
import numpy as np
from interest import Interest
from posts import Posts
import pytest 

interest_df = pd.read_csv("data/interest.csv")
posts_df = pd.read_csv("data/posts.csv")
users_df = pd.read_csv("data/users.csv")

def test_find_similarity():
    mat_dict = Interest(interest_df).find_similarity()
    assert mat_dict['5a1e85f2-a569-464d-a60d-edd981af3e59']['0ba4476e-a542-470c-a41d-2a8c6a45ddc1'] == 0.22360679774997896

def test_reorder_ranks():
    p = Posts(posts_df)
    new_ranks = p._reorder_ranks([1, 2, 3, 5, 7, 7, 10, 10, 11])
    assert new_ranks == [1, 2, 3, 4, 5, 5, 6, 6, 7]


def test_sort_posts_for_user():
    sim_dict = Interest(interest_df).find_similarity()
    p = Posts(posts_df, sim_dict)
    
    target_user = '0ba4476e-a542-470c-a41d-2a8c6a45ddc1'
    recency_true = p.sort_posts_for_user(target_user, by_recency=True, by_reply_numbers=False)
    assert recency_true.loc[0, "post_id"] == '91b7ce82-0ea4-4940-8e69-19ee239a1930'
    assert recency_true.loc[1, "post_id"] == 'acf17268-fa2e-4bcb-8286-37164fb75112'
    assert recency_true.loc[2, "post_id"] == '5f5765aa-4b9f-41fa-b790-186ba831fdf4'

    reply_number_true = p.sort_posts_for_user(target_user, by_recency=False, by_reply_numbers=True)
    assert reply_number_true.loc[0, "post_id"] == '91b7ce82-0ea4-4940-8e69-19ee239a1930'
    assert reply_number_true.loc[1, "post_id"] == 'acf17268-fa2e-4bcb-8286-37164fb75112'
    assert reply_number_true.loc[2, "post_id"] == 'f5389c56-831f-4a85-907f-515836d26e40'
    assert reply_number_true.loc[3, "post_id"] == '5f5765aa-4b9f-41fa-b790-186ba831fdf4'


if __name__ == "__main__":
    test_find_similarity()
    test_reorder_ranks()
    test_sort_posts_for_user()