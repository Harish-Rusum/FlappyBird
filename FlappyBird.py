import pygame

import random

pygame.init()
pygame.mixer.init()

# Screen variables
screenWidth = 436
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
icon = pygame.image.load("assets/favicon.ico").convert()
pygame.display.set_icon(icon)
pygame.display.set_caption("Flappy Bird")

# Loading images
bgImg = pygame.image.load("assets/sprites/background-day.png").convert()
bgImg = pygame.transform.scale(
    bgImg, (1.6 * bgImg.get_width(), 1.6 * bgImg.get_height())
)
ground = pygame.image.load("assets/sprites/base.png").convert()
ground = pygame.transform.scale(
    ground, (1.3 * ground.get_width(), 1.3 * ground.get_height())
)
ground2 = pygame.image.load("assets/sprites/base.png").convert()
ground2 = pygame.transform.scale(
    ground2, (1.3 * ground2.get_width(), 1.3 * ground2.get_height())
)

# Loading sounds
die = pygame.mixer.Sound("assets/audio/hit.wav")
die.set_volume(0.5)
point = pygame.mixer.Sound("assets/audio/point.wav")
point.set_volume(0.1)
flap = pygame.mixer.Sound("assets/audio/wing.wav")
flap.set_volume(0.1)


# Bird class
class Bird:
    def __init__(self):
        self.b1 = pygame.image.load(
            "assets/sprites/yellowbird-upflap.png"
        ).convert_alpha()
        self.b2 = pygame.image.load(
            "assets/sprites/yellowbird-midflap.png"
        ).convert_alpha()
        self.b3 = pygame.image.load(
            "assets/sprites/yellowbird-downflap.png"
        ).convert_alpha()
        self.birdCycle = [
            pygame.transform.scale(
                self.b1, (1.1 * self.b1.get_width(), 1.1 * self.b1.get_height())
            ),
            pygame.transform.scale(
                self.b2, (1.1 * self.b2.get_width(), 1.1 * self.b2.get_height())
            ),
            pygame.transform.scale(
                self.b3, (1.1 * self.b3.get_width(), 1.1 * self.b3.get_height())
            ),
        ]
        self.img = self.birdCycle[0]
        self.x, self.y = (screenWidth // 2) - 170.0, (screenHeight // 2)
        self.vel_y = 0.0
        self.g = 0.3
        self.jumpStrength = -7
        self.aniFrame = 0
        self.rect = self.img.get_rect()
        self.angle = 0

    def gravity(self):
        self.vel_y += self.g
        self.y += self.vel_y

    def jump(self):
        self.vel_y = self.jumpStrength
        self.angle = 20

    def update(self, screen):
        self.img = self.birdCycle[self.aniFrame // 7 % 3]
        self.img = pygame.transform.rotate(self.img, self.angle)
        self.gravity()
        self.rect = self.img.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(self.img, self.rect.topleft)
        self.aniFrame += 1
        self.angle = max(self.angle - 1, -70)


# Pipe class
class Pipe:
    def __init__(self, x):
        self.imgBottom = pygame.image.load("assets/sprites/pipe-green.png").convert()
        self.imgTop = pygame.transform.rotate(self.imgBottom, 180)
        self.bottomY = random.randrange(200, 400)
        self.topY = self.bottomY - (self.imgTop.get_height() + 156)
        self.x = x
        self.moveSpeed = 2
        self.offScreen = False
        self.rectTop = self.imgTop.get_rect()
        self.rectBottom = self.imgBottom.get_rect()
        self.rectTop.x = self.x
        self.rectTop.y = self.topY
        self.rectBottom.x = self.x
        self.rectBottom.y = self.bottomY

    def move(self):
        self.x -= self.moveSpeed

    def update(self, surface, score):
        self.move()
        if self.x + self.imgTop.get_width() < 0:
            self.offScreen = True
            score += 1
            point.play()
        self.rectTop.x = self.x
        self.rectTop.y = self.topY
        self.rectBottom.x = self.x
        self.rectBottom.y = self.bottomY
        surface.blit(self.imgTop, (self.x, self.topY))
        surface.blit(self.imgBottom, (self.x, self.bottomY))
        return score


def menu():
    running = True
    menu = pygame.image.load("assets/sprites/message.png").convert_alpha()
    menu = pygame.transform.scale(
        menu, (1.5 * menu.get_width(), 1.5 * menu.get_height())
    )
    bgImg = pygame.image.load("assets/sprites/background-day.png").convert()
    bgImg = pygame.transform.scale(
        bgImg, (1.6 * bgImg.get_width(), 1.6 * bgImg.get_height())
    )
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        screen.blit(bgImg, (0, -200))
        screen.blit(menu, (70, 80))
        pygame.display.flip()


def main():
    # Game variables
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(screenWidth + 100), Pipe(screenWidth + 300), Pipe(screenWidth + 500)]
    running = True
    groundHeight = ground.get_height()
    groundY = screenHeight - groundHeight
    groundOneX = 0
    groundTwoX = groundOneX + ground.get_width()
    score = 0
    scoreDict = {
        1: pygame.image.load("assets/sprites/1.png").convert_alpha(),
        2: pygame.image.load("assets/sprites/2.png").convert_alpha(),
        3: pygame.image.load("assets/sprites/3.png").convert_alpha(),
        4: pygame.image.load("assets/sprites/4.png").convert_alpha(),
        5: pygame.image.load("assets/sprites/5.png").convert_alpha(),
        6: pygame.image.load("assets/sprites/6.png").convert_alpha(),
        7: pygame.image.load("assets/sprites/7.png").convert_alpha(),
        8: pygame.image.load("assets/sprites/8.png").convert_alpha(),
        9: pygame.image.load("assets/sprites/9.png").convert_alpha(),
        0: pygame.image.load("assets/sprites/0.png").convert_alpha(),
    }
    while running:
        # Game quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Handling bird jumping
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    bird.jump()
                    flap.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()
                flap.play()

        # Clear screen
        screen.fill((0, 0, 0))

        # Updating screen images
        screen.blit(bgImg, (0, -200))
        bird.update(screen)
        pipes_to_remove = []
        for pipe in pipes:
            if pipe.rectTop.colliderect(bird.rect) or pipe.rectBottom.colliderect(
                bird.rect
            ):
                die.play()
                return (score, scoreDict)
            score = pipe.update(screen, score)
            if pipe.offScreen:
                pipes_to_remove.append(pipe)

        # Remove pipes that are off screen
        for pipe in pipes_to_remove:
            pipes.remove(pipe)
            new_pipe = Pipe(screenWidth + 150)
            pipes.append(new_pipe)
        screen.blit(ground, (groundOneX, groundY))
        screen.blit(ground2, (groundTwoX, groundY))

        offset = 0
        width = 0
        for i in range(len(str(score))):
            width += scoreDict[int(str(score)[i])].get_width()
        startingX = (screenWidth // 2) - width // 2
        for i in range(len(str(score))):
            char = scoreDict[int(str(score)[i])]
            screen.blit(char, (startingX + offset, 500))
            offset += char.get_width()
        pygame.display.flip()

        # Updating infinite scrolling background
        groundOneX -= 2
        groundTwoX -= 2
        if groundOneX <= -ground.get_width():
            groundOneX = groundTwoX + ground.get_width()
        if groundTwoX <= -ground.get_width():
            groundTwoX = groundOneX + ground.get_width()

        if bird.y >= screenHeight - ground.get_height():
            die.play()
            return (score, scoreDict)

        # Clock timer
        clock.tick(60)
    die.play()
    return (score, scoreDict)


def gOver(score, scoreDict):
    running = True
    gameOver = pygame.image.load("assets/sprites/gameOver.png").convert_alpha()
    gameOver = pygame.transform.scale(
        gameOver, (1.5 * gameOver.get_width(), 1.5 * gameOver.get_height())
    )
    bgImg = pygame.image.load("assets/sprites/background-day.png").convert()
    bgImg = pygame.transform.scale(
        bgImg, (1.6 * bgImg.get_width(), 1.6 * bgImg.get_height())
    )
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    return "Redo"
        screen.blit(bgImg, (0, -200))
        screen.blit(gameOver, (70, 80))
        offset = 0
        width = 0
        for i in range(len(str(score))):
            width += pygame.transform.scale2x(scoreDict[int(str(score)[i])]).get_width()
        startingX = (screenWidth // 2) - width // 2
        for i in range(len(str(score))):
            char = pygame.transform.scale2x(scoreDict[int(str(score)[i])])
            screen.blit(char, (startingX + offset, screenHeight // 2))
            offset += char.get_width()
        pygame.display.flip()


def game():
    menu()
    tup = main()
    if gOver(tup[0], tup[1]) == "Redo":
        game()


game()
