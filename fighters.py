from __future__ import annotations

ATTACK = 0
DEFENSE = 1

class Move():
    def __init__(self, name: str, power: int, mana_cost: int, desc: str , type: int = ATTACK):
        self.name = name
        self.power = power
        self.mana_cost = mana_cost
        self.description = desc
        self.type = type # Type 0 means it's an attack, 1 means it's it's a defensive move.

class Fighter():
    def __init__(self, name: str, max_hp: int, max_mana: int, moves: list):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mana = max_mana
        self.mana = max_mana
        self.moves = moves

    def use_move(self, move: Move, opponent: Fighter):
        if self.mana >= move.mana_cost:
            if move.type == ATTACK:
                self.mana -= move.mana_cost
                opponent.take_damage(move.power)
                return f"{self.name} used {move.name}!"
            elif move.type == DEFENSE:
                self.mana -= move.mana_cost
                self.heal(move.power)
                return f"{self.name} healed themselves! (+{move.power} hp)" if self.hp < 200 else f"{self.name} healed themselves to full hp!"
        else:
            return False

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def is_alive(self):
        return self.hp > 0
