# import thư viện
import pygame
from pygame.locals import *

pygame.init()

background  = pygame.image.load("./asset/img/background.png")
ground = pygame.image.load("./asset/img/ground.png")

clock = pygame.time.Clock()

# game variables
fps = 60
ground_scroll = 0 #điểm bắt đầu của mặt đất
scroll_speed = 4 # mỗi lần mặt đất sẽ di chuyển 4 pixel
background_scroll = 0
bg_scroll_speed = 0.03
screen_width = 855
screen_height = 635
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")
game_start = False
game_over = False

# tao một class Bird bằng pygame.sprite
# các sprites là các thực thể có thể chuyển động trong game, có màu sắc, hành động,...
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # kế thừa các hàm có sẵn trong pygame.sprite.Sprite
        pygame.sprite.Sprite.__init__(self)
        # danh sách các hình ảnh của Bird, để animate Bird thì chỉ cần show từng index trong danh sách này thiệt nhanh, giống như flipbook hoặc như kiểu animation vẽ tay rồi cho chạy các bản vẽ
        self.images = []
        # mỗi index là mỗi hình ảnh của Bird
        self.index = 0
        # bộ đếm dùng cho tốc độ chuyển index
        self.counter = 0
        # thêm vào danh sách images
        for num in range(1, 4):
            img = pygame.image.load(f"./asset/img/bird{num}.png")
            self.images.append(img)
        # hình ảnh mặc định của Bird
        self.image = self.images[self.index]
        # hộp chứa đối tượng, dùng để xác định vị trí, kích thước, va chạm của đối tượng
        self.rect = self.image.get_rect()
        # set vị trí của đối tượng
        self.rect.center = [x,y]
        # ?
        self.flap_animation_flag = 0
        # vận tốc rơi
        self.velocity = 0
        # nhấn chuột
        self.clicked = False

    # overwrite hàm update
    def update(self):
        
        # trọng lực
        # giới hạn tốc độ rơi
        if self.velocity > 8:
            self.velocity = 8
        if game_start:
            self.velocity += 0.5
            if self.rect.bottom < 535:
                self.rect.y += int(self.velocity)

        # nhảy lên khi nhấn chuột trái
        if game_over == False :
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.velocity = -10
                self.clicked = True
            elif pygame.mouse.get_pressed()[0] == False and self.clicked == True:
                self.clicked = False

            self.counter += 1
            flap_cooldown = 5

            # sau 5 lần lặp thì sẽ cập nhật hình ảnh của flappy 1 lần
            if self.counter > flap_cooldown and self.rect.bottom < 535:
                self.counter = 0

                if self.flap_animation_flag == 0:
                    self.index += 1
                    if self.index >= len(self.images) - 1:
                        self.flap_animation_flag = 1

                else:
                    self.index -= 1
                    if self.index <= 0:
                        self.flap_animation_flag = 0

            # Cập nhật hình ảnh flappy
            self.image = self.images[self.index]

            # xoay flappy khi rơi hoặc khi bay
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)


# tạo mảng các sprite, mỗi phần tử là 1 dạng của flappy
bird_group = pygame.sprite.Group()

# tạo một đối tượng Bird trước
flappy = Bird(100, int(screen_height/2))

# thêm vào bird_group
bird_group.add(flappy)

run = True

while run:


    # fps của game
    clock.tick(fps)


    # vẽ background
    screen.blit(background, (background_scroll,0))

    # vẽ flappy
    bird_group.draw(screen)
    bird_group.update()

    # vẽ mặt đất
    screen.blit(ground, (ground_scroll, 535))

    # nếu flappy chạm cỏ
    if flappy.rect.bottom >= 535:
        game_over = True
        game_start = False

    if game_over == False:  #nếu flappy chưa chạm đất
        ground_scroll -= scroll_speed # di chuyển mặt đất về bên trái
        background_scroll -= bg_scroll_speed

    if(abs(ground_scroll) > 20):
        ground_scroll = 0
    if(abs(background_scroll) > 325):
        background_scroll = 0

    

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_start == False and game_over == False:
            game_start = True

    

    pygame.display.update()            

pygame.quit()