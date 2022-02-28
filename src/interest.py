from sklearn import preprocessing
import numpy as np
import pandas as pd
from numpy import dot
from numpy.linalg import norm



class Interest:
    def __init__(self, df):
        self.interest_df = df.copy()

    def find_similarity(self):
        '''
            This will find the similarity between users based on their interests.
            output:
                A dictionary that maps user to the similarity values of other users.
        '''
        le = preprocessing.LabelEncoder()
        self.interest_df["label"] = le.fit_transform(np.ravel(self.interest_df["interest"]))
        user_interest = pd.pivot_table(self.interest_df, columns="interest", index="uid", aggfunc='count', fill_value=0)

        data = user_interest.values
        users = user_interest.index

        m, k = data.shape

        mat = np.zeros((m, m))

        for i in range(m):
            for j in range(m):
                if i != j:
                    mat[i][j] = dot(data[i], data[j])/(norm(data[i])*norm(data[j]))
                else:
                    mat[i][j] = 0.
        
        similarity_matrix = pd.DataFrame(mat, columns=users, index=users)
        similarity_dict = similarity_matrix.to_dict('dict')

        return similarity_dict