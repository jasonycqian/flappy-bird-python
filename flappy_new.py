'''
Flappy Bird
Original by Jason Qian, June 11th 2024
Edited by Jason Qian, September 30th 2026
(Instructions built in the game)
Please enjoy the game!
'''
import os
import sys
import time
import random
import pygame
from graphics import *


# =============================================================================
# SETTINGS (all the "magic numbers" from the old code, now with names)
# =============================================================================

WIN_WIDTH = 420
WIN_HEIGHT = 760
CENTER_X = WIN_WIDTH / 2

RED = color_rgb(245, 54, 7)
GOLD = color_rgb(240, 175, 53)
FONT = "times roman"

BIRD_IMAGE = "theflappy.gif"
FPS = 60                    # frames per second

# Bird physics (same feel as the original game)
SPEED_SCALE = 100           # the bird moves y_speed / SPEED_SCALE pixels per frame
GRAVITY_START = 100         # how strong gravity is right after a flap
GRAVITY_GROWTH = 1.05       # gravity gets 5% stronger every frame
FLAP_SPEED = -1300          # upward speed given by a flap

# Bird tilt and death spin
ANGLE_STEP = 10             # one picture per 10 degrees (must divide 360; smaller = smoother)
TILT_UP_LIMIT = -30         # most nose-up tilt, right after a flap
TILT_DOWN_LIMIT = 60        # most nose-down tilt, when diving
TILT_PER_SPEED = 4          # degrees of tilt per pixel/frame of falling speed
SPIN_SPEED = 20             # degrees per frame he spins when he dies (negative = other way)
BIRD_FRAMES_FOLDER = "bird_frames"   # where the rotated pictures are saved

# Bird hitbox (distance from the bird's center to each edge)
BIRD_START_X = 50
BIRD_START_Y = 380
BIRD_RIGHT_EDGE = 31
BIRD_LEFT_EDGE = 28
BIRD_HALF_HEIGHT = 22
GROUND_LIMIT_Y = 607        # bird dies below this

# Pillars
PILLAR_COUNT = 3
PILLAR_SPACING = 200        # horizontal distance between pillars
PILLAR_SPAWN_X = 458        # where new pillars appear (just off the right side)
PILLAR_OFFSCREEN_X = -67    # when a pillar reaches this, it's recycled
PILLAR_SPEED = 5            # pixels per frame
PILLAR_HALF_WIDTH = 39
PILLAR_IMAGE_OFFSET = 440   # distance from gap center to each pillar image's center
GAP_CENTER_Y = 338
GAP_HALF_HEIGHT = 74
FIRST_GAP_RANGE = 200       # first pillars: gap moves up/down a bit
RESPAWN_GAP_RANGE = 300     # later pillars: gap can be lower (same as original)


# =============================================================================
# SETUP: sounds, music, window
# =============================================================================

pygame.mixer.init()
click_sound = pygame.mixer.Sound("point.wav")
fall_sound = pygame.mixer.Sound("falling.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
flap_sound = pygame.mixer.Sound("flap.wav")

win = GraphWin("Flappy Bird", WIN_WIDTH, WIN_HEIGHT, autoflush=False)


def make_bird_frames():
    """Use pygame to rotate the bird to every angle and save each one as a PNG,
    then load them all for graphics.py. Returns a dictionary: angle -> Image."""
    os.makedirs(BIRD_FRAMES_FOLDER, exist_ok=True)

    original = pygame.image.load(BIRD_IMAGE)
    # Copy onto a see-through surface so the corners stay transparent when rotated
    bird_surface = pygame.Surface(original.get_size(), pygame.SRCALPHA, 32)
    bird_surface.blit(original, (0, 0))

    frames = {}
    for angle in range(0, 360, ANGLE_STEP):
        rotated = pygame.transform.rotate(bird_surface, -angle)  # minus: pygame turns counterclockwise
        filename = os.path.join(BIRD_FRAMES_FOLDER, f"bird_{angle}.png")
        pygame.image.save(rotated, filename)
        frames[angle] = Image(Point(0, 0), filename)
    return frames


bird_frames = make_bird_frames()


# =============================================================================
# DRAWING HELPERS
# =============================================================================

def make_text(center, message, size, color="black", bold=False):
    """Create, style, and draw a piece of text. Returns it."""
    label = Text(center, message)
    label.setSize(size)
    label.setFace(FONT)
    label.setTextColor(color)
    if bold:
        label.setStyle("bold")
    label.draw(win)
    return label


def make_image(center, filename):
    """Create and draw an image. Returns it."""
    picture = Image(center, filename)
    picture.draw(win)
    return picture


def make_button(corner1, corner2, label_text, outline_width=0, text_color="black"):
    """Draw a red button with text centered on it. Returns (box, label)."""
    box = Rectangle(corner1, corner2)
    box.setWidth(outline_width)
    box.setFill(RED)
    box.draw(win)
    label = make_text(box.getCenter(), label_text, 36, text_color)
    return box, label


def make_panel():
    """Draw the big red panel used behind About, Instructions and Game Over."""
    panel = Rectangle(Point(50, 100), Point(370, 660))
    panel.setFill(RED)
    panel.setOutline("black")
    panel.draw(win)
    return panel


def undraw_all(items):
    """Undraw every object in a list."""
    for item in items:
        item.undraw()


def bring_to_front(item):
    """Redraw an object so it appears on top of everything else."""
    item.undraw()
    item.draw(win)


# =============================================================================
# CLICK HELPERS
# =============================================================================

def is_inside(point, rectangle):
    """True if the point is inside the rectangle."""
    corner1 = rectangle.getP1()
    corner2 = rectangle.getP2()
    left = min(corner1.getX(), corner2.getX())
    right = max(corner1.getX(), corner2.getX())
    top = min(corner1.getY(), corner2.getY())
    bottom = max(corner1.getY(), corner2.getY())
    return left < point.getX() < right and top < point.getY() < bottom


def wait_for_click_on(buttons):
    """Wait until the player clicks one of the given rectangles. Returns that rectangle."""
    while True:
        click = win.getMouse()
        click_sound.play()
        for button in buttons:
            if is_inside(click, button):
                return button


def quit_game():
    pygame.mixer.music.stop()
    win.close()
    sys.exit()


# =============================================================================
# PHYSICS HELPER
# =============================================================================

def apply_gravity(y_speed, gravity):
    """One frame of gravity: gravity gets stronger, and the bird falls faster.
    Returns the new (y_speed, gravity)."""
    gravity = gravity * GRAVITY_GROWTH
    y_speed = y_speed + gravity
    return y_speed, gravity


# =============================================================================
# BIRD ROTATION
# =============================================================================

def tilt_for_speed(y_speed):
    """Nose up when rising, nose down when falling (like the real game)."""
    angle = (y_speed / SPEED_SCALE) * TILT_PER_SPEED
    return max(TILT_UP_LIMIT, min(TILT_DOWN_LIMIT, angle))


def show_bird_angle(bird, angle):
    """Swap the bird for the picture closest to this angle, in the same spot.
    Returns the bird picture now on screen (save it back into your bird variable)."""
    angle = round(angle / ANGLE_STEP) * ANGLE_STEP % 360    # snap to a picture we made
    frame = bird_frames[angle]
    if frame is bird:           # already showing this angle, nothing to do
        return bird

    center = bird.getAnchor()
    bird.undraw()
    frame_center = frame.getAnchor()
    frame.move(center.getX() - frame_center.getX(), center.getY() - frame_center.getY())
    frame.draw(win)
    return frame


# =============================================================================
# MENU SCREENS
# =============================================================================

def show_about_screen():
    """Show the About page until the player clicks BACK."""
    screen_items = [
        make_panel(),
        make_text(Point(CENTER_X, 200), "ABOUT", 36, GOLD),
        make_text(Point(CENTER_X, 300), "Created by Jason Qian", 25, GOLD),
        make_text(Point(CENTER_X, 340), "June 11th, 2024", 25, GOLD),
        make_text(Point(CENTER_X, 375), "Inspired by the real Flappy Bird", 20, GOLD),
        make_image(Point(CENTER_X, 475), BIRD_IMAGE),
    ]
    back_box, back_label = make_button(Point(75, 550), Point(345, 625), "BACK",
                                       outline_width=4, text_color=GOLD)
    screen_items.append(back_box)
    screen_items.append(back_label)

    wait_for_click_on([back_box])
    undraw_all(screen_items)


def show_main_menu(title):
    """Show START / ABOUT. Returns once the player clicks START."""
    while True:
        start_box, start_label = make_button(Point(50, 300), Point(370, 400), "START")
        about_box, about_label = make_button(Point(50, 450), Point(370, 550), "ABOUT")

        choice = wait_for_click_on([start_box, about_box])
        undraw_all([start_box, start_label, about_box, about_label])

        if choice == start_box:
            return

        # ABOUT was clicked: hide the title, show About, then loop back to the menu
        title.undraw()
        show_about_screen()
        title.draw(win)


def play_title_animation():
    """Flappy flies across the screen, flapping randomly, until any key is pressed."""
    prompt = make_text(Point(CENTER_X, 650), "Press any key to continue", 36, RED)

    bird = make_image(Point(-50, 380), BIRD_IMAGE)
    y_speed = 300
    gravity = GRAVITY_START
    frames_since_flap = 0
    frames_flown = 0

    while win.checkKey() == "":
        bird.move(5, y_speed / SPEED_SCALE)
        frames_flown += 1
        frames_since_flap += 1

        if frames_since_flap > random.randint(5, 30):
            y_speed = -1000
            gravity = GRAVITY_START
            frames_since_flap = 0

        y_speed, gravity = apply_gravity(y_speed, gravity)
        update(FPS)

        # Bird has flown off the right side: pause, then start again from the left
        if frames_flown > 105:
            bird.undraw()
            time.sleep(random.randint(1, 200) / 100)
            bird = make_image(Point(-50, 380), BIRD_IMAGE)
            y_speed = 300
            gravity = GRAVITY_START
            frames_since_flap = 0
            frames_flown = 0

    undraw_all([prompt, bird])


def play_jump_demo(frames_after_flap, pause_at_end=0, keep_in_front=None):
    """Instruction animation: Flappy drifts right, flaps once, then resets.
    Repeats until any key is pressed.
    keep_in_front: an image that should be drawn on top of the bird (e.g. the pillar)."""
    frames_before_flap = 11

    while True:
        bird = make_image(Point(125, 350), BIRD_IMAGE)
        if keep_in_front is not None:
            bring_to_front(keep_in_front)
        y_speed = 300
        gravity = GRAVITY_START

        for frame in range(frames_before_flap + frames_after_flap):
            if win.checkKey() != "":
                bird.undraw()
                return
            bird.move(5, y_speed / SPEED_SCALE)
            if frame == frames_before_flap - 1:
                y_speed = -1600
                gravity = GRAVITY_START
            y_speed, gravity = apply_gravity(y_speed, gravity)
            update(FPS)

        time.sleep(pause_at_end)
        bird.undraw()
        time.sleep(0.1)


def show_instructions():
    """Two instruction pages, each with a small animation."""
    panel = make_panel()
    heading = make_text(Point(CENTER_X, 200), "INSTRUCTIONS", 36, GOLD)
    next_hint = make_text(Point(CENTER_X, 600), "Press again to continue", 30, GOLD)

    # Page 1: how to jump
    tip = make_text(Point(CENTER_X, 300), "Tap space to make Flappy jump", 22, GOLD)
    tap_picture = make_image(Point(260, 500), "tap.gif")
    play_jump_demo(frames_after_flap=19)
    undraw_all([tip, tap_picture])

    # Page 2: avoid pillars (bird flies into the pillar and pauses)
    tip = make_text(Point(CENTER_X, 300), "Avoid the incoming pillars", 25, GOLD)
    example_pillar = make_image(Point(300, 450), "egpillar.gif")
    play_jump_demo(frames_after_flap=14, pause_at_end=1, keep_in_front=example_pillar)
    undraw_all([tip, example_pillar, panel, heading, next_hint])


# =============================================================================
# PILLARS
# Each pillar is a dictionary holding its two images, its gap position,
# and whether the player already got a point for it.
# =============================================================================

def make_pillar(x, gap_range):
    """Create a top + bottom pillar pair at x with a random gap height."""
    gap_y = GAP_CENTER_Y + (random.randint(1, gap_range) - 100)
    return {
        "bottom": make_image(Point(x, gap_y + PILLAR_IMAGE_OFFSET), "pillarb.png"),
        "top": make_image(Point(x, gap_y - PILLAR_IMAGE_OFFSET), "pillart.png"),
        "gap_y": gap_y,
        "scored": False,
    }


def pillar_x(pillar):
    return pillar["top"].getAnchor().getX()

def rightmost_pillar_x(pillars):
    """The x position of the pillar furthest to the right."""
    rightmost = pillar_x(pillars[0])
    for pillar in pillars:
        if pillar_x(pillar) > rightmost:
            rightmost = pillar_x(pillar)
    return rightmost

def move_pillar(pillar):
    pillar["top"].move(-PILLAR_SPEED, 0)
    pillar["bottom"].move(-PILLAR_SPEED, 0)


def undraw_pillar(pillar):
    undraw_all([pillar["top"], pillar["bottom"]])


def bird_hits_pillar(bird, pillar):
    """True if the bird overlaps the pillar and is outside the gap."""
    bird_x = bird.getAnchor().getX()
    bird_y = bird.getAnchor().getY()
    x = pillar_x(pillar)
    gap_y = pillar["gap_y"]

    lined_up = (bird_x + BIRD_RIGHT_EDGE > x - PILLAR_HALF_WIDTH and
                bird_x - BIRD_LEFT_EDGE < x + PILLAR_HALF_WIDTH)
    outside_gap = (bird_y + BIRD_HALF_HEIGHT > gap_y + GAP_HALF_HEIGHT or
                   bird_y - BIRD_HALF_HEIGHT < gap_y - GAP_HALF_HEIGHT)
    return lined_up and outside_gap


# =============================================================================
# GAME
# =============================================================================

def play_death_fall(bird, angle):
    """Freeze for a moment after the hit, then Flappy spins off the bottom of the screen.
    Returns the bird picture that's on screen at the end."""
    hit_sound.play()
    time.sleep(0.5)

    fall_sound.play()
    bring_to_front(bird)        # so he falls in front of the ground and pillars
    y_speed = -800
    gravity = GRAVITY_START
    while bird.getAnchor().getY() < WIN_HEIGHT + 50:    # 50 = a bit past the bottom edge
        bird.move(-1, y_speed / SPEED_SCALE)
        y_speed, gravity = apply_gravity(y_speed, gravity)
        angle += SPIN_SPEED
        bird = show_bird_angle(bird, angle)
        update(FPS)

    time.sleep(1)               # short pause before the Game Over screen
    return bird


def play_round(ground):
    """Play one round of Flappy Bird. Returns the final score."""
    bird = make_image(Point(BIRD_START_X, BIRD_START_Y), BIRD_IMAGE)

    pillars = []
    for i in range(PILLAR_COUNT):
        pillars.append(make_pillar(PILLAR_SPAWN_X + i * PILLAR_SPACING, FIRST_GAP_RANGE))
    bring_to_front(ground)

    prompt = make_text(Point(CENTER_X, 200), "Tap space to get started!", 36, RED)
    win.getKey()
    prompt.undraw()

    score = 0
    score_label = make_text(Point(CENTER_X, 150), str(score), 36, bold=True)
    y_speed = 0
    gravity = GRAVITY_START
    bird_angle = 0
    alive = True

    while alive:
        # Flap
        if win.checkKey() == "space":
            y_speed = FLAP_SPEED
            gravity = GRAVITY_START
            flap_sound.play()

        # Bird physics
        bird.move(0, y_speed / SPEED_SCALE)
        y_speed, gravity = apply_gravity(y_speed, gravity)
        bird_angle = tilt_for_speed(y_speed)
        bird = show_bird_angle(bird, bird_angle)
        if bird.getAnchor().getY() > GROUND_LIMIT_Y:
            alive = False

        # Pillars: move all of them first...
        for pillar in pillars:
            move_pillar(pillar)

        # ...then recycle, collide, score
        for i in range(len(pillars)):
            if pillar_x(pillars[i]) <= PILLAR_OFFSCREEN_X:
                undraw_pillar(pillars[i])
                new_x = rightmost_pillar_x(pillars) + PILLAR_SPACING
                pillars[i] = make_pillar(new_x, RESPAWN_GAP_RANGE)
                bring_to_front(ground)


            if bird_hits_pillar(bird, pillars[i]):
                alive = False

            if not pillars[i]["scored"] and pillar_x(pillars[i]) < BIRD_START_X:
                pillars[i]["scored"] = True
                score += 1
                click_sound.play()
                score_label.setText(str(score))

        bring_to_front(score_label)
        update(FPS)

    # Flappy died: play the falling animation
    bird = play_death_fall(bird, bird_angle)

    # Round over: clear the playing field
    bird.undraw()
    score_label.undraw()
    for pillar in pillars:
        undraw_pillar(pillar)
    return score


def show_game_over(score):
    """Show the Game Over screen. Returns if PLAY AGAIN is clicked; quits on EXIT."""
    screen_items = [
        make_panel(),
        make_text(Point(260, 360), str(score), 36, GOLD),
        make_image(Point(CENTER_X, 250), "gameover.png"),
        make_text(Point(160, 360), "Score:", 30, GOLD),
    ]
    again_box, again_label = make_button(Point(75, 450), Point(345, 525), "PLAY AGAIN",
                                         outline_width=4, text_color=GOLD)
    exit_box, exit_label = make_button(Point(75, 550), Point(345, 625), "EXIT GAME",
                                       outline_width=4, text_color=GOLD)
    screen_items += [again_box, again_label, exit_box, exit_label]

    choice = wait_for_click_on([again_box, exit_box])
    if choice == exit_box:
        quit_game()
    undraw_all(screen_items)


# =============================================================================
# MAIN: the whole game, in order
# =============================================================================

def main():
    pygame.mixer.music.load("bgmusic.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    make_image(Point(CENTER_X, WIN_HEIGHT / 2), "bg.gif")
    title = make_image(Point(CENTER_X, 150), "flappytext.gif")

    show_main_menu(title)
    play_title_animation()
    title.undraw()
    show_instructions()

    ground = make_image(Point(CENTER_X, 700), "ground.png")
    while True:
        score = play_round(ground)
        show_game_over(score)


if __name__ == "__main__":
    main()
