import random

from pygame import Vector2, sprite, Surface

from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.game_settings import WINDOW_HEIGHT, WINDOW_WIDTH
from thefloatingdutchman.manager import Manager


class EnemyManager(Manager):
    def __init__(self):
        super().__init__()
        self._enemies = None

    def spawn(self, level: int):
        self._enemies = sprite.Group()
        self._add_enemies(level)


    def _add_enemies(self, level: int):

        for i in range(random.randint(2, 4) + level):

            # picking position a fair distance away from player
            rand_pos_x: int = random.randint(40, WINDOW_WIDTH/2 - 200) if bool(
                random.randint(0, 1)) else random.randint(WINDOW_WIDTH/2 + 200, WINDOW_WIDTH - 40)

            rand_pos_y: int = random.randint(40, WINDOW_HEIGHT/2 - 100) if bool(
                random.randint(0, 1)) else random.randint(WINDOW_HEIGHT/2 + 100, WINDOW_HEIGHT - 40)

            self._enemies.add(
                EnemySprite(
                    EnemyData(
                        random.randint(30, 50) + (level*5),
                        1500, # random.randint(5, 15) + random.randint(0, level*2), 
                        Vector2(rand_pos_x, rand_pos_y),
                        5
                    )
                )
            )

    def get_enemy_count(self) -> int:
        return len(self._enemies.sprites())

    def update(self, player: PlayerSprite, screen: Surface):
        # enemies need reference to other enemies and the player
        self._enemies.update(player, self._enemies, screen)
        hit = sprite.groupcollide(self._enemies, player.bullets, False, True, sprite.collide_mask)
        for enemy in hit:
            enemy.take_damage(player._damage)

    def draw(self, screen: Surface):
        self._enemies.draw(screen)
        for enemy in self._enemies:
            enemy.bullets.draw(screen)
