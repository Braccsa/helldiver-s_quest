import json
import random
import uuid
from typing import Optional, Tuple, List
from schema import Quest, TeamQuest
from utils import award_points_to_players


def load_team_quests() -> dict:
    """Load team quests from JSON file."""
    with open("questLists/team_quest_list.json", "r") as f:
        return json.load(f)


def save_team_quest(team_quest: TeamQuest) -> None:
    """Save a team quest to the active team quests file."""
    with open("activity/active_team_quest.json", "r") as f:
        data = json.load(f)
    
    data["team_quests"].append(team_quest.to_dict())
    
    with open("activity/active_team_quest.json", "w") as f:
        json.dump(data, f, indent=2)


def load_active_team_quests() -> dict:
    """Load active team quests from JSON file."""
    with open("activity/active_team_quest.json", "r") as f:
        return json.load(f)


def save_active_team_quests(data: dict) -> None:
    """Save active team quests to JSON file."""
    with open("activity/active_team_quest.json", "w") as f:
        json.dump(data, f, indent=2)


def generate_team_quest(players: List[str], difficulty: int) -> Tuple[Optional[TeamQuest], str]:
    """Generate a team quest for the given players at the specified difficulty."""
    if difficulty < 1 or difficulty > 3:
        return None, "Difficulty must be between 1 and 3."
    
    data = load_team_quests()
    matching_quests = [q for q in data["team_quests"] if q["difficulty"] == difficulty]
    
    if not matching_quests:
        return None, f"No team quests available for difficulty {difficulty}."
    
    quest_data = random.choice(matching_quests)
    quest = Quest(quest_data["difficulty"], quest_data["title"], quest_data["description"])
    
    quest_id = str(uuid.uuid4())[:8]
    team_quest = TeamQuest(quest, players, quest_id)
    save_team_quest(team_quest)
    
    players_str = ", ".join(players)
    response_text = f"""
════════════════════════════════════════
         TEAM QUEST ASSIGNED
════════════════════════════════════════

**Mission:** {quest.title}
**Team:** {players_str}
**Difficulty:** {'⭐' * quest.difficulty}
**Quest ID:** {quest_id}

**Briefing:**
{quest.description}

Good luck, Helldivers!
════════════════════════════════════════
"""
    
    return team_quest, response_text


def generate_team_quest_message(username: str) -> str:
    """Generate a custom team quest message for a user. TODO: Implement full logic."""
    return f"🎯 **TEAM QUEST ALERT**\n\nSoldier {username}, you have been selected for a team mission!\n\nStand by for further orders, soldier!"


def complete_team_quest(quest_id: str) -> str:
    """Complete a team quest by ID and award points to all players."""
    team_quests_data = load_active_team_quests()
    
    quest_entry = next((q for q in team_quests_data["team_quests"] if q["quest_id"] == quest_id), None)
    
    if not quest_entry:
        return f"❌ Team quest with ID {quest_id} not found."
    
    difficulty = quest_entry["quest"]["difficulty"]
    points_per_player = difficulty * 100
    players = quest_entry["players"]
    
    reward_text = f"✅ Team quest completed! Quest ID: {quest_id}\n\n"
    reward_text += award_points_to_players(players, points_per_player)
    
    team_quests_data["team_quests"] = [q for q in team_quests_data["team_quests"] if q["quest_id"] != quest_id]
    save_active_team_quests(team_quests_data)
    
    return reward_text


def get_active_team_quests() -> str:
    """Display all active team quests."""
    team_quests_data = load_active_team_quests()
    quests = team_quests_data["team_quests"]
    
    if not quests:
        return "No active team quests at the moment."
    
    display_text = """
════════════════════════════════════════
         ACTIVE TEAM QUESTS
════════════════════════════════════════

"""
    
    for quest in quests:
        players_str = ", ".join(quest["players"])
        display_text += f"""**Quest ID:** {quest["quest_id"]}
**Mission:** {quest["quest"]["title"]}
**Team:** {players_str}
**Difficulty:** {'⭐' * quest["quest"]["difficulty"]}
**Status:** {quest["status"]}

"""
    
    display_text += "════════════════════════════════════════"
    return display_text

