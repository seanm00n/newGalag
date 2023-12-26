import pygame

pygame.init()
display = pygame.display.set_mode((800,600))
myfont = pygame.font.SysFont('Comic Sans MS', 30)
score = 0

player = pygame.image.load("plane.gif")
playerX, playerY, playerDx, playerDy = 400, 550, 0, 0

alien = pygame.image.load("plane.gif")
alienX, alienY, alienDx, alienDy = 0, 10, 0.1, 0.1

missile = pygame.image.load("plane.gif")
missileX, missileY, missileDx, missileDy = 0, 1000, 0, 0.1
missileState = "hidden"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  playerDx = -0.1
            if event.key == pygame.K_RIGHT:  playerDx = 0.1
            if event.key == pygame.K_SPACE:
                if missileState == "hidden":
                    missileState = "fire"
                    missileX, missileY = playerX, playerY
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerDx = 0

    rect1 = pygame.Rect(alien.get_rect(topleft=(alienX, alienY)))
    rect2 = pygame.Rect(missile.get_rect(topleft=(missileX, missileY)))
    if rect1.colliderect(rect2) and missileState != "hidden":
        score += 1
        alienX, alienY, alienDx, alienDy = 0, 10, 0.1, 0.1

    playerX += playerDx

    alienX += alienDx
    if alienX <= 0 or alienX > 750:
        alienDx *= -1
        alienY += 30

    if missileY <= 0:
        missileY = 1000
        missilestate = "hidden"

    if missileState == "fire":
        missileY -= missileDy
        
    display.fill((0,0,0))
    display.blit(player, (playerX, playerY))
    display.blit(missile, (missileX, missileY))
    display.blit(alien, (alienX, alienY))
    text = myfont.render(f"score={score}",False, (255,255,255))
    display.blit(text,(10,550))
    pygame.display.update()
            
pygame.quit()
