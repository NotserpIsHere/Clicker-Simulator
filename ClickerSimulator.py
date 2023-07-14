import pygame
import random
pygame.init()

# Set screen size
screen = pygame.display.set_mode((400, 300))

# Set initial score and income
score = 0
income = 0

# Set font for displaying score
font = pygame.font.Font(None, 36)

# Set colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set upgrade costs and effects
upgrade_costs = [10, 50, 100]
upgrade_effects = [1, 5, 10]

# Set achievement thresholds and rewards
achievement_thresholds = [10, 100, 1000]
achievement_rewards = [1, 10, 100]
achievements_unlocked = [False] * len(achievement_thresholds)

# Set particle properties
particles = []
particle_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
particle_lifetime = 60

# Set level properties
levels = [10, 100, 1000]
current_level = 0

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Increase score on mouse click
            score += 1 + income
            # Add particles
            for i in range(10):
                x,y=event.pos
                dx=random.randint(-5,
                                   5)
                dy=random.randint(-5,-1)
                color=random.choice(particle_colors)
                particles.append([x,y,dx,
                                  dy,color,
                                  particle_lifetime])
            # Check if mouse is over a button
            x,y=event.pos
            if y>250:
                # Check which button was clicked
                button=x//130
                if button<len(upgrade_costs) and score>=upgrade_costs[button]:
                    # Buy upgrade
                    score-=upgrade_costs[button]
                    income+=upgrade_effects[button]

    # Update particles
    for particle in particles:
        particle[0]+=particle[2]
        particle[1]+=particle[3]
        particle[5]-=1

    # Remove dead particles
    particles=[p for p in particles if p[5]>0]

    # Check for unlocked achievements
    for i in range(len(achievement_thresholds)):
        if not achievements_unlocked[i] and score>=achievement_thresholds[i]:
            # Unlock achievement
            achievements_unlocked[i]=True
            income+=achievement_rewards[i]

    # Check for level up
    if current_level<len(levels) and score>=levels[current_level]:
        current_level+=1

    # Clear screen
    screen.fill(white)

    # Render score and income
    text=font.render(f"Score: {score}",True,
                     black)
    screen.blit(text,(20,20))
    text=font.render(f"Income: {income}/click",True,
                     black)
    screen.blit(text,(20,50))

    # Render buttons
    for i in range(len(upgrade_costs)):
        x=i*130+10
        y=250
        if score>=upgrade_costs[i]:
            color=(0,200,0)
        else:
            color=(200,0,0)
        pygame.draw.rect(screen,color,(x,y,
                                       120,
                                       40))
        text=font.render(f"+{upgrade_effects[i]}",True,
                         white)
        screen.blit(text,(x+10,y+5))
        text=font.render(f"{upgrade_costs[i]} pts",True,
                         white)
        screen.blit(text,(x+10,y+25))

    # Render achievements
    y=100
    for i in range(len(achievement_thresholds)):
        if achievements_unlocked[i]:
            color=(0,200,0)
        else:
            color=(200,200,200)
        pygame.draw.rect(screen,color,(10,y+i*50,
                                       380,
                                       40))
        text=font.render(f"Achievement: {achievement_thresholds[i]} pts",True,
                         white)
        screen.blit(text,(20,y+i*50+5))
        text=font.render(f"+{achievement_rewards[i]}/click",True,
                         white)
        screen.blit(text,(20,y+i*50+25))

    # Render level
    text=font.render(f"Level: {current_level}",True,
                     black)
    screen.blit(text,(20,80))

    # Render particles
    for particle in particles:
        x,y=int(particle[0]),int(particle[1])
        color=particle[4]
        pygame.draw.circle(screen,color,(x,y),
                           3)

    # Update display
    pygame.display.flip()
