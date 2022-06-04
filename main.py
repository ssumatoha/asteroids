from classes import *


pygame.init()


pygame.display.set_caption('Asteroids')
win = pygame.display.set_mode((sw, sh))
clock = pygame.time.Clock()

gameover = False
lives = 3
rapidFire = False
rfStart = -1


def redrawGameWindow():  # ф-ция отрисовки
    win.blit(bg, (0, 0))
    font = pygame.font.SysFont('arial', 30)
    livesText = font.render('Lives: ' + str(lives), 1, (255, 255, 255))
    playAgainText = font.render('Press Tab to Play Again', 1, (255, 255, 255))

    player.draw(win)
    for i in asteroids:
        i.draw(win)
    for i in playerBullets:
        i.draw(win)

    if rapidFire:
        pygame.draw.rect(win, (0, 0, 0), [sw//2 - 51, 19, 102, 22])
        pygame.draw.rect(win, (255, 255, 255), [sw//2 - 50, 20, 100 - 100*(count - rfStart)/500, 20])

    if gameover:
        win.blit(playAgainText, (sw//2-playAgainText.get_width()//2, sh//2 - playAgainText.get_height()//2))
    win.blit(livesText, (25, 25))
    pygame.display.update()


playerBullets = []
asteroids = []
count = 0
run = True
screensaver = True
while run:  # цикл игры
    while screensaver:  # цикл-заставка
        font = pygame.font.SysFont('arial', 30)
        win.blit(bg, (0, 0))
        playAgainText = font.render('click the mouse button to start the game', 1, (255, 255, 255))
        win.blit(playAgainText, (sw//2-playAgainText.get_width()//2, sh//2 - playAgainText.get_height()//2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                screensaver = False
    clock.tick(60)
    count += 1
    if not gameover:  # заполнение поля астероидами
        if count % 50 == 0:
            asteroids.append(Asteroid(1))

        player.updateLocation()
        for b in playerBullets:  # удаление пули при выходе за экран
            b.move()
            if b.checkOffScreen():
                playerBullets.pop(playerBullets.index(b))

        for a in asteroids:  # проверка на попадание игрока в астероид
            a.x += a.xv
            a.y += a.yv

            if (a.x >= player.x - player.w//2 and a.x <= player.x + player.w//2) or (a.x + a.w <= player.x + player.w//2 and a.x + a.w >= player.x - player.w//2):
                if(a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or (a.y  +a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    break

            for b in playerBullets:  # проверка на попадание в астероид пули
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        asteroids.pop(asteroids.index(a))
                        playerBullets.pop(playerBullets.index(b))
                        break

        if lives <= 0:
            gameover = True

        if rfStart != -1:
            if count - rfStart > 500:
                rapidFire = False
                rfStart = -1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()
        if keys[pygame.K_UP]:
            player.moveForward()
        if keys[pygame.K_SPACE]:
            if rapidFire:
                playerBullets.append(Bullet())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    if not rapidFire:
                        playerBullets.append(Bullet())
            if event.key == pygame.K_m:
                isSoundOn = not isSoundOn
            if event.key == pygame.K_TAB:
                if gameover:
                    gameover = False
                    lives = 3
                    asteroids.clear()

    redrawGameWindow()

pygame.quit()
