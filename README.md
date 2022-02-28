# Wemoney: User Sorted Newsfeed engine

In this problem, we are trying to create a ranking system to sort the posts for the users based on their interests.
We have applied the similarity approach to scoring the news feed based on user interest similarity. Then, ordering the scores based on other criteria of the business problem such as recency and the number of replies.
The first step is calculating the similarity between each user based on what they are interested in. 

We have used the cosine similarity for this purpose. If two users have the same set of interests, e.g. Reducing spending, Buying a property, Track bills and EFTS, then the score calculated for these users will be 1.0. On the other hand, if two users do not share any similar interests, their similarity score will be zero. The similarity score is a fundamental step for the future development of the recommendation algorithm and there is room for imporovement here.

Finally, as the recent posts are more relevant and number of replies to a post makes it important, we have options to include them in our sorting system.

### Algorithm
The core of the algorithm are two classes, Posts and Interests. Class Interest calculates the similarity matrix (really a dictionary here) through the find_similarity method. Since we have a separate module here, makes it easy to modify the calculation of the similarity matrix in the future if needed.

Class Posts has two methods, a helper method (._reorder_ranks()) to rerank the posts if there are gaps and jumps due to the filtering. The second method is the .sort_posts_for_user() method. This method takes a user as a target and sorts all the posts by other users based on the similarity of their interests. We have 3 more arguments for this method:

- by_recency: the posts with the same similarity score will be sorted by the column time in descending order. It means, if we have, e.g. 5 posts by users whose interests are similar to the target user, the most recent posts will be placed on the top of the list. If the two posts are posted simultaneously (which should be a rare case), they will be sorted by the number of replies they have.

- by_reply_numbers: The posts with the same similarity score will be sorted by the column reply_numbers (which is calculated in a preprocessing step) in descending order. It means if we have, e.g 5 posts by users whose interests are similar to the target user, the posts with the highest number of replies are first to show. In case some of those posts have the same number of replies, they will be sorted by their recency.

### Future Ideas
It would be a good idea to score the comments based on their similarity with the target user's interest, so that any posts that do not contain anything that matches what the target user is interested in, can be filtered out.

The posts of users with similar interests come first, but also if those users are involved in any thread (replying to other posts) all of those posts will get priority for the target user. Let's assume a user who has the same similarity to our target user replying to a post. It makes sense that maybe those replies get priority as well. 

### Question:
I was unsure how to apply the current time as an argument to the algorithm that is going to be implemented. Since we sort on the recency and current time can be the time we run the algorithm. 



