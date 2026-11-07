import pygame
from models import Asteroid, Spaceship
from utils import get_random_position, load_sprite, print_text


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self, on_result=None):
        self.on_result = on_result
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()        #以固定帧率运行
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append) 

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()

            elif (              #子弹生成
            self.spaceship
            and event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            ):

                self.spaceship.shoot()


        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            elif is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()

    def _process_game_logic(self):
        #  所有对象 move
        for game_object in self._get_game_objects():
            game_object.move(self.screen)   
         
        #  撞击就摧毁，针对每个小行星进行检查
        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self._finish_game("loss", "You lost!")
                    break
                
        # 子弹出界就删除
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        # 子弹摧毁小行星，两者消失，或者小行星1变2
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        if not self.asteroids and self.spaceship:
            self._finish_game("win", "You won!")

    def _finish_game(self, result, message):
        # 胜负画面会继续刷新，但一局只通知一次。
        if self.message:
            return
        self.message = message
        if self.on_result:
            self.on_result(result)


    def _draw(self):
        self.screen.blit(self.background, (0,0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        
        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(60)    #每秒60帧    
        # print("Collides:", self.spaceship.collides_with(self.asteroid)) #测试碰撞识别

    def _get_game_objects(self):
        # 返回所有游戏对象
        game_objects = [*self.asteroids, *self.bullets]        
        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects
