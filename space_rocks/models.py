from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import get_random_velocity, load_sound, load_sprite, wrap_position

UP = Vector2(0, -1)

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)       #中心点
        self.sprite = sprite                      #图像
        self.radius = sprite.get_width() / 2      #表示物体位置周围碰撞区的值，宽度一半
        self.velocity = Vector2(velocity)          #移动速度

    def draw(self, surface):            #blit（） 需要在左上角
        blit_position = self.position - Vector2(self.radius) # 将图像绘制到表面上的位置，减去半径，使图像的中心点与物体位置对齐
        surface.blit(self.sprite, blit_position) # 将图像绘制到表面上的位置

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface) # 移动物体，位置加上速度

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position) # 计算两个物体之间的距离
        return distance < self.radius + other_obj.radius # 如果距离小于两个物体的半径之和，则认为两个物体碰撞

class Spaceship(GameObject):
    MANEUVERABILITY = 3     # 机动性，每帧旋转角度
    ACCELERATION = 0.25
    BULLET_SPEED = 3

    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback  #callback
        self.laser_sound = load_sound("laser")
        # 复制原始UP向量，因为后面会被修改
        self.direction = Vector2(UP)
        
        super().__init__(position, load_sprite("spaceship"), Vector2(0))


    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP) # 计算飞船的旋转角度
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size()) # 获取旋转后图像的大小
        blit_position = self.position - rotated_surface_size * 0.5 # 计算绘制位置，使图像的中心点与飞船位置对齐
        surface.blit(rotated_surface, blit_position) # 将旋转后的图像绘制到表面上的位置
    
    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION # 加速，速度加上方向乘以加速度
    
    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity    #飞船很快的话，可以制作高速子弹
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()


class Asteroid(GameObject):
    def __init__(self, position,create_asteroid_callback, size=3):
        self.creat_asteroid_callback = create_asteroid_callback
        self.size = size
        
        size_to_scale = {
            3: 1,
            2: 0.5,
            1: 0.25,
        }
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)

        super().__init__(
        position, sprite, get_random_velocity(1, 3)
        )
    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.creat_asteroid_callback, self.size - 1
                )
                self.creat_asteroid_callback(asteroid)

class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)
        
    def move(self, surface):
        self.position = self.position + self.velocity