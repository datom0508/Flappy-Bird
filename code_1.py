# import thư viện
import pygame
from pygame.locals import *
import random

pygame.init()

background  = pygame.image.load("./asset/img/background.png")
ground = pygame.image.load("./asset/img/ground.png")
restart_btn_img = pygame.image.load("./asset/img/restart.png")

clock = pygame.time.Clock()

#font chữ
font = pygame.font.SysFont('Bauhaus 93', 60)
# màu chữ
white = (255, 255, 255)

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
pipe_gap = 150 #khoảng cách giữa 2 ống
pipe_frequency = 1500 #tần suất xuất hiện 1 ống (ms)
last_pipe = pygame.time.get_ticks() - pipe_frequency #thời gian ống cuối cùng được tạo
pass_pipe = False #flappy đã bay qua ống hay chưa
score = 0

# hàm vẽ chữ
def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x, y))


# reset các biến khi reset game
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    flappy.velocity = 0
    score = 0
    return score

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
        if game_over == False:
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
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./asset/img/pipe.png")
        self.images = []
        self.rect = self.image.get_rect()
        # position = 1 thì là ống trên, -1 là ống dưới
        if position == 1:
            # xoay ngược hình của cái ống lại
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        else:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed  # cho ống di chuyển
        # nếu ống ra khỏi màn hình thì xóa nó luôn
        if self.rect.right < 0:
            self.kill()


class Button:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    def draw(self):

        btn_clicked = False

        # lấy vị trí con chuột
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):   #kiểm tra nếu con chuột đang hover trên cái nút
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0]:   #kiểm tra nếu chuột trái được nhấn
                btn_clicked = True
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return btn_clicked


# tạo mảng các sprite, mỗi phần tử là 1 dạng của flappy
bird_group = pygame.sprite.Group()

# tạo mảng Pipe
pipe_group = pygame.sprite.Group()

# tạo một đối tượng Bird trước
flappy = Bird(100, int(screen_height/2))

# thêm vào bird_group
bird_group.add(flappy)

# tạo nút restart
restart_btn = Button(restart_btn_img, screen_width // 2 - 50, screen_height // 2 - 100)

run = True

while run:


    # fps của game
    clock.tick(fps)


    # vẽ background
    screen.blit(background, (background_scroll,0))

    # vẽ ống
    pipe_group.draw(screen)

    # vẽ flappy
    bird_group.draw(screen)
    bird_group.update()

    # vẽ mặt đất
    screen.blit(ground, (ground_scroll, 535))

    # tính điểm
    if len(pipe_group) > 0:    #nếu có ít nhất 1 ống đã xuất hiện
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    # nếu flappy đụng ống
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0: #2 cái false là khi 2 group chạm nhau thì sẽ không có cái nào bị xóa, true là sẽ xóa đi
        game_over = True

    # nếu flappy chạm cỏ
    if flappy.rect.bottom >= 535:
        game_over = True
        game_start = False

    if game_over == False and game_start == True:  #nếu flappy chưa chạm đất

        # tạo ống
        pipe_height = random.randint(-100, 100) #lấy số nguyễn ngẫu nhiên, tạo sự ngẫu nhiên cho các ống
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            # tạo một ống trên 
            top_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, 1)
            # tạo một ống dưới 
            bot_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, -1)
            #thêm vào pipe_group
            pipe_group.add(top_pipe)
            pipe_group.add(bot_pipe)
            last_pipe = time_now

        pipe_group.update()

        ground_scroll -= scroll_speed # di chuyển mặt đất về bên trái
        background_scroll -= bg_scroll_speed

    if(abs(ground_scroll) > 20):
        ground_scroll = 0
    if(abs(background_scroll) > 325):
        background_scroll = 0

    
    # nếu game over
    if game_over == True:
        if restart_btn.draw():
            game_over = False
            score = reset_game()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_start == False and game_over == False:
            game_start = True

    

    pygame.display.update()            

pygame.quit()