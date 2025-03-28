from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

import pandas as pd
import numpy as np

import json

class MakeRecommendationsAPIView(APIView):
    def post(self, request):
        # Get the data from the request
        data = request.data

        # Convert the data to a DataFrame
        df = pd.DataFrame(data)

        # Check if the DataFrame is empty
        if df.empty:
            return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the DataFrame has the required columns
        required_columns = ['user_id', 'item_id', 'rating']
        for col in required_columns:
            if col not in df.columns:
                return Response({"error": f"Missing column: {col}"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a pivot table
        pivot_table = df.pivot(index='user_id', columns='item_id', values='rating').fillna(0)

        # Convert the pivot table to a numpy array
        matrix = pivot_table.values

        # Calculate the cosine similarity matrix
        from sklearn.metrics.pairwise import cosine_similarity
        similarity_matrix = cosine_similarity(matrix)

        # Create a DataFrame for the similarity matrix
        similarity_df = pd.DataFrame(similarity_matrix, index=pivot_table.index, columns=pivot_table.index)

        # Get recommendations for each user
        recommendations = {}
        for user in similarity_df.index:
            similar_users = similarity_df[user].sort_values(ascending=False)[1:6].index.tolist()
            recommended_items = set()
            for similar_user in similar_users:
                recommended_items.update(pivot_table.loc[similar_user][pivot_table.loc[similar_user] > 0].index.tolist())
            recommendations[user] = list(recommended_items)

        return Response(recommendations, status=status.HTTP_200_OK)
