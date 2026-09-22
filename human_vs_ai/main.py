import random

#   ---SPELLZ---

class Spellz:
    def __init__(self, name, mana_drain, damage, defense, effect):
        self.name = name
        self.mana_drain = mana_drain
        self.damage = damage
        self.defense = defense
        self.effect = effect

    def cast(self, caster, target):
        if caster.mana < self.mana_drain:
            print(f"- {caster.name} doesn't have enough mana for {self.name}!")
            return False

        caster.mana -= self.mana_drain
        print(f"- {caster.name} uses {self.mana_drain} mana to cast {self.name}")

        if self.effect == "damage":
            inflicted = target.take_damage(self.damage)
            print(f"- {self.name} inflicts {inflicted} damage to {target.name}")

        elif self.effect == "defense":
            caster.defense += self.defense
            print(f"- {caster.name}'s defense increased by {self.defense}!")

        elif self.effect == "heal":
            caster.heal()  # or custom heal
            print(f"- {self.name} restores HP!")

        elif self.effect == "bind":
            target.apply_bind(3)
            print(f"- {target.name} is bound for 3 turns!")

        return True

    def __str__(self):
        return f"{self.name} ({self.mana_drain} mana, {self.damage} dmg)"

FIREBALL = Spellz("Fireball", 20, 20, 0, "damage")
ICEBOLT = Spellz("Icebolt", 15, 15, 0, "damage")
STONE_SKIN = Spellz("Stone Skin", 10, 0, 5, "defense")
RESURRECT = Spellz("Resurrect", 20, 0, 0, "heal")
BIND = Spellz("Bind", 70, 0, 0, "bind")

class Hero:
    """Holds shared logic for any hero"""
    def __init__(self, name, hp, max_hp, mana, max_mana, attack_pts, defense, bind_turns):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.mana = mana
        self.max_mana = max_mana
        self.attack_pts = attack_pts
        self.defense = defense
        self.bind_turns = 0
        self.spellbook = [FIREBALL, ICEBOLT, STONE_SKIN, RESURRECT, BIND]


    def is_alive(self):
        """Returns True if HP > 0"""
        return self.hp > 0

    def take_damage(self, raw_damage):
        taken = raw_damage - self.defense
        if taken < 1:
            taken = 1     # Minumun 1 damage
        self.hp -= taken
        if self.hp < 0:
            self.hp = 0
        return taken    # <- Return the actual damage

    def attack(self, target):
        raw_damage = random.randint(
            int(self.attack_pts * 0.7),
            int(self.attack_pts * 1.2)
        )
        inflicted_damage = target.take_damage(raw_damage)
        print(f"- {self.name} inflicted {inflicted_damage} total damage to {target.name}")

    def cast_spell(self, spell, target):
        """Casts a spell object at target."""
        if spell in self.spellbook:
            return spell.cast(self, target)
        print(f"- {self.name} doesn't know that spell!")
        return False

    def defend(self):
        self.defense += 3/100 * self.max_hp
        print(f"- {self.name} has increased their defenses!")

    def heal(self):
        healed = self.mana // 5 + 1
        self.hp += healed
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        self.mana -= healed
        print(f"- {self.name} heals {healed} HP!")

    def mana_regen(self):
        self.mana += 7
        print(f"- {self.name} replenishes their nexus!")

    def apply_bind(self, turns):
        """Applies bind for X turns"""
        self.bind_turns = turns

    def is_bound(self):
        """Returns True if currently bound"""
        return self.bind_turns > 0

    def tick_bind(self):
        """Reduces bind counter by 1 at turn start"""
        if self.bind_turns > 0:
            self.bind_turns -= 1
            if self.bind_turns == 1:
                print(f"{self.name} is bound for 1 more turn!")
            else:
                print(f"{self.name} is bound for another {self.bind_turns} turns!")

    def __str__(self):
        return f"{self.name} (HP:{self.hp}/{self.max_hp} MAN:{self.mana}/{self.max_mana})"



#   ---PLAYERS---

class Player(Hero):
    """Inherits from Hero"""
    """User-Controlled"""

    def __init__(self, name, hp, max_hp, mana, max_mana, attack_pts, defense, bind_turns):
        super().__init__(name, hp, max_hp, mana, max_mana, attack_pts, defense, bind_turns)
        self.potions = 3


class Enemy(Hero):
    """Inherits from Hero"""
    """AI-Controlled"""
    def __init__(self, name, hp, max_hp, mana, max_mana, attack_pts, defense, bind_turns):
        super().__init__(name, hp, max_hp, mana, max_mana, attack_pts, defense, bind_turns)

    def choose_action(self):
        return "attack" if random.random() < 0.8 else "heal"

#   ---BATTLE---

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 0

    def player_turn(self):
        print(f"\nTurn: {self.turn}")
        print(self.player)
        print(self.enemy)
        if self.turn > 1:
            self.player.mana_regen()


        choice = int(input("Choose an action:"
              "\nAttack [1]     "
              "Heal [2]    "
              "Spellbook [3]   "
              "Defend [4]"
              "Skip [5]"
                           "\n"))

        if choice == 1:
            self.player.attack(self.enemy)
        elif choice == 2:
            self.player.heal()
        elif choice == 4:
            self.player.defend()
        elif choice == 5:
            print("- Nothing happens, lel!")

        if choice == 3:
            print("\n=== Spellbook ===")
            for i, spell in enumerate(self.player.spellbook, start=1):
                print(f"[{i}] {spell}")

            pick = int(input("Choose a spell: "))

            if 1 <= pick <= len(self.player.spellbook):
                spell = self.player.spellbook[pick - 1]
                self.player.cast_spell(spell, self.enemy)


    def enemy_turn(self):
        if self.turn > 1:
            self.player.mana_regen()
        action = self.enemy.choose_action()
        if action == "attack":
            self.enemy.attack(self.player)
        if action == "heal":
            self.enemy.heal()

    def start(self):
        print(f"{self.player} VS {self.enemy}!!!")

        while self.player.is_alive() and self.enemy.is_alive():
            self.turn += 1

            self.player.tick_bind()
            self.enemy.tick_bind()

            if not self.player.is_bound():
                self.player_turn()
            else:
                print(f"- You are bound!")

            if not self.enemy.is_alive():
                print(f"{self.player.name} wins!")
                break

            if not self.enemy.is_bound():
                self.enemy_turn()
            else:
                print(f"{self.enemy.name} is bound! ")

            if self.turn > 1:
                self.enemy.mana_regen()


            if not self.player.is_alive():
                print(f"{self.enemy.name} wins!")
                break

player = Player("Malekith", 100, 100, 100, 100, 25, 5, 0)
enemy = Enemy("Galthran", 80, 80, 80, 80, 20, 3, 0)
battle = Battle(player, enemy)
battle.start()

