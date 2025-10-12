from src.entities.player import Player

class PlayerDTO:
    @staticmethod
    def to_dict(player: Player):
        return {
            "name": player.name,
            "birthdate": player.birthdate,
            "gender": player.gender,
            "rating": {
                "classic": player.rating.classic,
                "rapid": player.rating.rapid,
                "blitz": player.rating.blitz
            }
        }
    
    @staticmethod
    def from_dict(data: dict) -> Player:
        from src.entities.rating import Rating  # Import here to avoid circular dependency
        rating_data = data.get("rating", {})
        rating = Rating(
            classic=rating_data.get("classic", 0),
            rapid=rating_data.get("rapid", 0),
            blitz=rating_data.get("blitz", 0)
        )
        return Player(
            name=data.get("name", ""),
            birthdate=data.get("birthdate", ""),
            gender=data.get("gender", ""),
            rating=rating
        )