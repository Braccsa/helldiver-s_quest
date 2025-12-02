from typing import List
from quest_generator import load_user_quests
from schema import User


def get_user_stats(username: str) -> str:
    """Display score statistics for a specific user."""
    data = load_user_quests()
    user_data = next((u for u in data["users"] if u["username"] == username), None)
    
    if not user_data:
        return f"No stats found for {username}."
    
    user = User.from_dict(user_data)
    
    stats_text = f"""
════════════════════════════════════════
             SOLDIER STATS
════════════════════════════════════════

**Soldier:** {user.username}
**Total Score:** {user.score}

Keep fighting, soldier!
"""
    return stats_text


def get_leaderboard() -> str:
    """Display a leaderboard of users ranked by score."""
    data = load_user_quests()
    users = [User.from_dict(u) for u in data["users"]]
    
    if not users:
        return "No users found on the leaderboard yet."
    
    sorted_users = sorted(users, key=lambda u: u.score, reverse=True)
    
    leaderboard_text = """
════════════════════════════════════════
            GLOBAL LEADERBOARD
════════════════════════════════════════

"""
    
    for rank, user in enumerate(sorted_users, 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        leaderboard_text += f"{medal} {user.username}: {user.score} points\n"
    
    leaderboard_text += "\n════════════════════════════════════════"
    
    return leaderboard_text
