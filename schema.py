from enum import Enum

class QuestStatus(Enum):
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Quest:
    def __init__(self, difficulty: int, title: str, description: str):
        self.difficulty = difficulty
        self.title = title
        self.description = description
    
    def __str__(self):
        return f"**{self.title}** (Difficulty: {self.difficulty})\n{self.description}"

class GeneratedQuest:
    def __init__(self, user: str, quest: Quest, status: QuestStatus = QuestStatus.IN_PROGRESS):
        self.user = user
        self.quest = quest
        self.status = status
    
    def __str__(self):
        return f"{self.user}'s Quest - Status: {self.status.value}\n{self.quest}"
    


class User:
    def __init__(self, username: str, active_quest: dict = None, score: int = 0):
        self.username = username
        self.active_quest = active_quest
        self.score = score
    
    def to_dict(self):
        return {
            "username": self.username,
            "active_quest": self.active_quest,
            "score": self.score
        }
    
    @staticmethod
    def from_dict(data):
        return User(data["username"], data.get("active_quest"), data.get("score", 0))

class TeamQuest:
    def __init__(self, quest: Quest, players: list[str], quest_id: str = None, status: QuestStatus = QuestStatus.IN_PROGRESS):
        self.quest_id = quest_id
        self.quest = quest
        self.players = players
        self.status = status
    
    def to_dict(self):
        return {
            "quest_id": self.quest_id,
            "quest": {
                "difficulty": self.quest.difficulty,
                "title": self.quest.title,
                "description": self.quest.description
            },
            "players": self.players,
            "status": self.status.value
        }
    
    @staticmethod
    def from_dict(data):
        quest = Quest(data["quest"]["difficulty"], data["quest"]["title"], data["quest"]["description"])
        status = QuestStatus(data.get("status", "in progress"))
        return TeamQuest(data["quest_id"], quest, data["players"], status)
    
    def __str__(self):
        players_str = ", ".join(self.players)
        return f"**{self.quest.title}** (Difficulty: {self.quest.difficulty})\nTeam: {players_str}\nStatus: {self.status.value}"
