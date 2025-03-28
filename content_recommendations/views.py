from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import random

class MakeRecommendationsAPIView(APIView):
    def post(self, request):
        # Récupération des données
        data = request.data

        # Vérification des données
        if not data:
            return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

        df = pd.DataFrame(data)

        # Vérification des colonnes requises
        required_columns = ['user_id', 'item_id', 'rating']
        for col in required_columns:
            if col not in df.columns:
                return Response({"error": f"Missing column: {col}"}, status=status.HTTP_400_BAD_REQUEST)

        # Création de la matrice utilisateur-élément
        pivot_table = df.pivot(index='user_id', columns='item_id', values='rating').fillna(0)

        # Calcul de la similarité cosinus entre utilisateurs
        similarity_matrix = cosine_similarity(pivot_table.values)
        similarity_df = pd.DataFrame(similarity_matrix, index=pivot_table.index, columns=pivot_table.index)

        # Sélection d'un utilisateur (premier utilisateur du dataset pour l'exemple)
        user_id = pivot_table.index[0]

        # Trouver des utilisateurs similaires
        similar_users = similarity_df[user_id].sort_values(ascending=False)[1:6].index.tolist()

        # Obtenir les recommandations de produits
        recommended_items = set()
        for similar_user in similar_users:
            recommended_items.update(pivot_table.loc[similar_user][pivot_table.loc[similar_user] > 0].index.tolist())

        # Simuler un cluster utilisateur (exemple : une valeur entre 1 et 5)
        user_cluster = random.randint(1, 5)

        # Filtrer les recommandations et attribuer un score de confiance aléatoire
        top_products = [
            {"product": str(item), "confidence": round(random.uniform(0.6, 0.9), 2)}
            for item in recommended_items
        ][:3]  # On sélectionne 3 produits max

        # Simuler les canaux préférés
        preferred_channels = random.sample(["myMTN", "USSD", "Ayoba", "SMS", "Email"], 3)

        # Simuler des opportunités d'upsell
        upsell_opportunities = [
            {"product": "Extra Data Bundle", "reason": "High data usage detected"},
            {"product": "Device Upgrade", "reason": "Old device model detected"}
        ]

        # Construire la réponse finale
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
