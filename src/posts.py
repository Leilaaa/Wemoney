
import pandas as pd

class Posts:
    def __init__(self, postDF, sim_dict=None):
        self.postDF = postDF
        self.sim_dict = sim_dict
    
        self.postDF["post_time"] = pd.to_datetime(self.postDF["post_time"])

        number_of_replies = self.postDF.loc[(self.postDF["parent_id"]!='0'), "parent_id"].value_counts()
        number_of_replies.name = "reply_numbers"

        self.postDF = pd.merge(self.postDF, number_of_replies, left_on="post_id", right_index=True, how='outer').fillna(0)
        self.postDF["reply_numbers"] = self.postDF["reply_numbers"].astype(int)

    def _reorder_ranks(self, rank_col):
        ''' This function tries to rearrange the ranks. 
            The posts belong to the same thread will rank the same.
            
            args: 
            rank_col: The column of ranks that needs to be rearranged

            output:
            new_ranks: The rearranged ranks
            
        '''
        previous_rank = rank_col[0] 
        new_ranks = [previous_rank]

        for rank in rank_col[1:]:
            if rank - previous_rank == 0:
                new_ranks.append(new_ranks[-1]) 
                previous_rank = rank
            elif rank - previous_rank > 0:
                new_ranks.append(new_ranks[-1]+1)
                previous_rank = rank
        return new_ranks
    
    def sort_posts_for_user(self, target_user, by_recency=False, by_reply_numbers=False):
        '''
            This function will sort all the posts based on the
            similarity of the interests of the users who post them with the target user.
            args:
                target_user: the target user we want to arrange the posts for
                by_recency: if it's True, will arrange the recent post
                            on the top for those who have similar interest
                            with the target user.(default=True)
                by_thread: if it's True, all the posts in the same thread will rank together.
                           example: If a user with similar interest to the target user has responded
                           to another post, all the thread will be ranked as high.
            
            output:
                a dataframe similar to posts dataframe which is ranked for the target user.

                
        '''
        cols_to_display = ["uid", "post_time", "text", 
                           "hashtags", "post_id", "parent_id",
                           "reply_numbers", "score", "rank"]

        df = pd.merge(self.postDF, pd.Series(self.sim_dict[target_user], name="score"), left_on="uid", right_index=True)
        
        df.sort_values(['score'], ascending=False, inplace=True)
            
        df["rank"] = list(range(1, df.shape[0]+1))

        if by_recency:
            df = df.sort_values('rank', ascending=True) \
                    .groupby(['score'], sort=False) \
                    .apply(lambda x: x.sort_values(['post_time', 'reply_numbers'], ascending=False)) \
                    .reset_index(drop=True)
            
        elif by_reply_numbers:
            df = df.sort_values('score', ascending=False) \
                    .groupby(['score'], sort=False) \
                    .apply(lambda x: x.sort_values(['reply_numbers', 'post_time'], ascending=False)) \
                    .reset_index(drop=True)
            df["rank"] = list(range(1, df.shape[0]+1))

        df = df[cols_to_display]
        return df
