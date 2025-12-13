"""This module contains the Game class, which is used to manage the game environment."""
import random
from collections import Counter
from player import Player
from role import Role


class Game:
    """Class to manage the game environment."""
    def __init__(self, players: list[Player], roles: list[Role]):
        self._running: bool = True
        self._day: int = 0

        random.shuffle(roles)
        for player, role in zip(players, roles):
            player.role = role

        self._survivors: dict[int, Player] = {p.id: p for p in players}
        self._dead_players: dict[int, Player] = {}
        self._pending_death: Player | None = None
        self._poisoned_player: Player | None = None

        self._wolfs: dict[int,Player] = {r.id: r.role == Role.WOLF for r in self._survivors.values()}
        self._wolfs_number: int = sum(self._wolfs.values())
        self._clergy_number: int = sum(r.role in {Role.PROPHET, Role.WITCH, Role.HUNTER} for r in self._survivors.values())
        self._villagers_number: int = len(self._survivors) - self._wolfs_number - self._clergy_number

        self._votes: dict[int, int] = {}
        self._kill_votes: dict[int, int] = {}
        self._votes_list: list[int] = []
        self._message_log: list[str] = []

    def receive_message(self, msg: str) -> None:
        """Receive a message and add it to the message log."""
        self._message_log.append(msg)

    def send_message(self, msg: str) -> None:
        """Broadcast a message to all players."""
        print(f"Game broadcast: {msg}")

    def wolf_kill(self) -> None:
        """Handle the logic for wolves to kill a player."""
        for player in self._wolfs.values():
            self._kill_votes[player.id] = player.kill_vote()
        counts = Counter(self._kill_votes.values())
        most_frequent_list = counts.most_common(1)
        if most_frequent_list.len() > 1:
            for player in self._wolfs.values():
                
        pass

    def witch_time(self) -> None:
        """Handle the witch's actions, including saving and poisoning players."""
        for p in self._survivors.values():
            if p.role == Role.WITCH:
                witch = p
                break
        if witch is None:
            return
        if witch.save_player(self._pending_death):
            self._pending_death = None
        else:
            self._poisoned_player = self._survivors[witch.poison_player()]
        return 

    def prophet_check(self) -> None:
        """Handle the prophet's action to check a player's role."""
        for p in self._survivors.values():
            if p.role == Role.PROPHET:
                prophet = p
                break
        if prophet is None:
            return 
        target_id = prophet.check_role(self._survivors.values())
        target = self._survivors[target_id]
        # Inform the prophet of the target's role
        return
    def died_player(self, player: Player) -> None:
        """Handle the logic for a player dying."""
        self._dead_players[player.id] = player
        del self._survivors[player.id]
        if player.role == Role.WOLF:
            self._wolfs_number -= 1
            self._wolfs.pop(player.id)
        elif player.role in {Role.PROPHET, Role.WITCH, Role.HUNTER}:
            self._clergy_number -= 1
        else:
            self._villagers_number -= 1
        return
    
    def day_change(self) -> None:
        """Advance the game to the next day."""
        if self._pending_death is not None:
            #self._pending_death.killed()
            '''if self._pending_death.role == Role.HUNTER:
                self.hunter_kill()'''
            self.died_player(self._pending_death)
            self._pending_death = None
        if self._poisoned_player is not None:
            #self._poisoned_player.poisoned()
            self.died_player(self._poisoned_player)
            self._poisoned_player = None
        
        self._day += 1
        self._votes.clear()
        self._kill_votes.clear()

    def vote(self) -> None:
        """Handle the voting process."""
        pass

    def vote_kill(self) -> None:
        """Handle the logic for killing a player based on votes."""
        pass

    def hunter_kill(self) -> None:
        """Handle the hunter's action to kill a player."""
        pass

    def end_game(self) -> None:
        """Determine the game's outcome and end the game."""
        pass
