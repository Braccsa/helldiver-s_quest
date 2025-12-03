import json
from typing import List, Tuple, Dict, Any, Optional
import discord
from schema import User


def load_user_list() -> Dict[str, Any]:
    """Load user list from JSON file."""
    with open("activity/user_list.json", "r") as f:
        return json.load(f)


def save_user_list(users: List[User]) -> None:
    """Save user list to JSON file."""
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


async def send_dm_to_users(users: List[discord.User], message: str) -> tuple[int, int]:
    """
    Send a DM to multiple users.
    
    Args:
        users: List of discord.User objects to send DMs to
        message: Message content to send
    
    Returns:
        Tuple of (successful_count, failed_count)
    """
    successful = 0
    failed = 0
    
    for user in users:
        try:
            await user.send(message)
            successful += 1
        except discord.Forbidden:
            failed += 1
    
    return successful, failed


def award_points_to_players(players: List[str], points_per_player: int) -> str:
    """
    Award points to multiple players and update their scores.
    
    Args:
        players: List of player usernames
        points_per_player: Points to award each player
    
    Returns:
        Formatted reward message
    """
    reward_text = ""
    
    for player_name in players:
        user = get_or_create_user(player_name)
        user.score += points_per_player
        save_user(user)
        reward_text += f"🎉 {player_name}: +{points_per_player} points (Total: {user.score})\n"
    
    return reward_text
