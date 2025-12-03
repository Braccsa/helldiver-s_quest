import json
import random
from typing import Optional, Tuple
from schema import Quest, User
from utils import get_or_create_user, save_user, award_points_to_players


def load_user_list() -> dict:
    """Load user quests from JSON file."""
    with open("activity/user_list.json", "r") as f:
        return json.load(f)


def save_user_list(users: list) -> None:
    """Save user quests to JSON file."""
    with open("activity/user_list.json", "w") as f:
        json.dump({"users": [u.to_dict() for u in users]}, f, indent=2)


def get_user(username: str) -> Optional[User]:
    """Get User object by username, returns None if not found."""
    data = load_user_list()
    for user_data in data["users"]:
        if user_data["username"] == username:
            return User.from_dict(user_data)
    return None


def get_or_create_user(username: str) -> User:
    """Get existing user or create a new one."""
    user = get_user(username)
    if user:
        return user
    return User(username)


def save_user(user: User) -> None:
    """Save or update a single user in the JSON file."""
    data = load_user_list()
    user_entry = next((u for u in data["users"] if u["username"] == user.username), None)
    
    if user_entry:
        user_entry.update(user.to_dict())
    else:
        data["users"].append(user.to_dict())
    
    save_user_list([User.from_dict(u) for u in data["users"]])


def generate_quest(username: str, difficulty: int) -> Tuple[Optional[Quest], str]:
    """Generate a quest for the given user at the specified difficulty."""
    user = get_or_create_user(username)
    
    if user.active_quest:
        response_text = f"""
════════════════════════════════════════
          QUEST ALREADY ACTIVE
════════════════════════════════════════

**helldiver:** {username}

You already have an active quest:
**{user.active_quest['title']}**

Complete or abandon it before requesting a new one!
"""
        return None, response_text
    
    with open("questLists/quest_list.json", "r") as f:
        data = json.load(f)

    matching_quests = [q for q in data["quests"] if q["difficulty"] == difficulty]

    if not matching_quests:
        return None, "No quests available for that difficulty."

    quest_data = random.choice(matching_quests)
    quest = Quest(quest_data["difficulty"], quest_data["title"], quest_data["description"])
    
    user.active_quest = {"title": quest.title, "difficulty": quest.difficulty, "description": quest.description}
    save_user(user)
    
    response_text = f"""
════════════════════════════════════════
             NEW QUEST ASSIGNED
════════════════════════════════════════

**helldiver:** {username}
**Mission:** {quest.title}
**Difficulty:** {'⭐' * quest.difficulty}

**Briefing:**
{quest.description}

Good luck, helldiver!
════════════════════════════════════════

"""
    
    return quest, response_text


def complete_user_quest(username: str) -> str:
    """Clear active quest for a user and award points based on difficulty."""
    user = get_or_create_user(username)
    
    if not user.active_quest:
        return f"No active quest to complete for {username}."
    
    difficulty = user.active_quest["difficulty"]
    points_earned = difficulty * 100
    user.active_quest = None
    save_user(user)
    
    reward_text = award_points_to_players([username], points_earned)
    return f"Quest completed for {username}.\n{reward_text}"


def abandon_user_quest(username: str) -> str:
    """Abandon active quest for a user without awarding points."""
    user = get_or_create_user(username)
    
    if not user.active_quest:
        return f"No active quest to abandon for {username}."
    
    quest_title = user.active_quest["title"]
    user.active_quest = None
    save_user(user)
    
    return f"Quest '{quest_title}' abandoned, {username}. Better luck next time, helldiver!"


def generate_team_quest_message(username: str) -> str:
    """Generate a custom team quest message for a user. TODO: Implement full logic."""
    return f"🎯 **TEAM QUEST ALERT**\n\nSoldier {username}, you have been selected for a team mission!\n\nStand by for further orders, soldier!"