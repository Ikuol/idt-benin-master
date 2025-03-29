from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import random


class MakeRecommendationsAPIView(APIView):

    # Ajout de la méthode GET pour renvoyer des recommandations simulées
    def get(self, request):
        # Simuler des recommandations pour un utilisateur donné (peut être modifié pour un vrai système)
        user_cluster = random.randint(1, 5)

        top_products = [
            {"product": "Video Streaming", "confidence": 0.85,
                "description": "Enjoy unlimited access to video content platforms without interruptions"},
            {"product": "Music Streaming", "confidence": 0.78,
                "description": "Stream your favorite music without any data worries"},
            {"product": "Gaming Premium", "confidence": 0.72,
                "description": "Get exclusive access to premium gaming content and features"},
            {"product": "Music Unlimited", "confidence": 0.68,
                "description": "Unlimited access to all your favorite music and podcasts"},
            {"product": "Video Unlimited", "confidence": 0.65,
                "description": "Unlimited access to all your favorite movies and series without data limits"},
        ]

        preferred_channels = ["myMTN", "USSD", "Ayoba"]

        upsell_opportunities = [
            {"product": "Extra Data Bundle", "reason": "High data usage detected"},
            {"product": "Device Upgrade", "reason": "Old device model detected"}
        ]

        response_data = {
            "status": "success",
            "cluster": user_cluster,
            "recommendations": {
                "top_products": top_products,
                "preferred_channels": preferred_channels,
                "upsell_opportunities": upsell_opportunities
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        # Récupération des données envoyées par le frontend
        data = request.data

        if not data:
            return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

        df = pd.DataFrame(data)

        # Vérification des colonnes nécessaires
        required_columns = ['user_id', 'item_id', 'rating']
        for col in required_columns:
            if col not in df.columns:
                return Response({"error": f"Missing column: {col}"}, status=status.HTTP_400_BAD_REQUEST)

        # Création de la matrice utilisateur-élément
        pivot_table = df.pivot(
            index='user_id', columns='item_id', values='rating').fillna(0)

        # Calcul de la similarité cosinus
        similarity_matrix = cosine_similarity(pivot_table.values)
        similarity_df = pd.DataFrame(
            similarity_matrix, index=pivot_table.index, columns=pivot_table.index)

        # Sélection d'un utilisateur pour l'exemple
        user_id = pivot_table.index[0]

        # Trouver les utilisateurs similaires
        similar_users = similarity_df[user_id].sort_values(ascending=False)[
            1:6].index.tolist()

        # Générer des recommandations de produits
        recommended_items = set()
        for similar_user in similar_users:
            recommended_items.update(
                pivot_table.loc[similar_user][pivot_table.loc[similar_user] > 0].index.tolist())

        user_cluster = random.randint(1, 5)

        top_products = [
            {"product": str(item), "confidence": round(
                random.uniform(0.6, 0.9), 2)}
            for item in recommended_items
        ][:3]

        preferred_channels = random.sample(
            ["myMTN", "USSD", "Ayoba", "SMS", "Email"], 3)

        upsell_opportunities = [
            {"product": "Extra Data Bundle", "reason": "High data usage detected"},
            {"product": "Device Upgrade", "reason": "Old device model detected"}
        ]

        response_data = {
            "status": "success",
            "cluster": user_cluster,
            "recommendations": {
                "top_products": top_products,
                "preferred_channels": preferred_channels,
                "upsell_opportunities": upsell_opportunities
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)
