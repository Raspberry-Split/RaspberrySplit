#Imports:
import pygame
import os
import sys
import time

#Get the current framebuffer via sysargs:
a = sys.argv[1]

#If it's on the TV, use 2x (dpi=2) assets. If it's on the PiTFT, use 1x assets.
if a == "0":
    dpi = 2
else:
    dpi = 1

#Code to set the Pi's 3.5mm volume, and load the Pi's current volume via sysargs:
vol = int(sys.argv[2])
def set_vol():
    global vol
    if vol > 0 and vol < 40:
        vol = 58
    if vol < 57:
        vol = 0
    os.system("sudo amixer cset numid=1 " + str(vol) + "%")
    os.environ['SWITCH_VOL'] = str(vol)
set_vol()

#Enviroment variables:
os.environ["SDL_FBDEV"] = "/dev/fb" + a
os.environ['SDL_VIDEODRIVER'] = 'fbcon'
os.environ['SWITCH_GAME'] = '/home/pi/RaspberrySplit/Apps/gpsp/gba_bios.bin'
os.environ['SWITCH_ED'] = '0'

#If it's on the TV:
if a == "0":
    os.system("vcgencmd display_power 1")
    os.environ['SWITCH_FB'] = '1'
    os.system("sudo amixer cset numid=3 2")
    #Turn the TV on, and change the audio device to the Pi's HDMI output.
    #Set SWITCH_FB so the next time the menu launches, it switches to the other framebuffer.
#If it's on the TFT:
else:
    os.system("vcgencmd display_power 0")
    os.environ['SWITCH_FB'] = '0'
    os.system("sudo amixer cset numid=3 1")
    #Turn the TV off, and change the audio device to the Pi's 3.5mm headphone jack.

#Create a font
pygame.font.init()
myfont = pygame.font.SysFont("a", 32*dpi)

#Create a text surface
textsurface = myfont.render('', False, (61, 197, 190))

#Some code for displaying game boxes.
class gamebox:
    def __init__(self, id, img, name, file):
        global maxed
        self.file = file
        self.id = id
        self.img = img
        self.rect = pygame.Rect((23+(155+23)*self.id-2)*dpi, 100*dpi, 157*dpi, 161*dpi)
        self.name = name
        maxed = id
    def draw(self):
        global selectedName
        global txx
        screen.blit(box, ((23+(155+23)*self.id+scroll)*dpi, 102*dpi))
        screen.blit(self.img, ((23+(155+23)*self.id+4+scroll)*dpi, 106*dpi))
        if self.id == selected:
            screen.blit(blue, ((23+(155+23)*self.id-2+scroll)*dpi, 100*dpi))
            selectedName = self.name

txx = 0

maxed = -1

scroll = 0

images = []
boxes = []


#Load different images depending on the DPI of the screen
if dpi == 1:
    gray = pygame.image.load("/home/pi/RaspberrySplit/Theme/NonRetina/BG.png")
    handheld = pygame.image.load("/home/pi/RaspberrySplit/Theme/NonRetina/Handheld.png")
    STTV = pygame.image.load("/home/pi/RaspberrySplit/Theme/NonRetina/STTV.png")

    box = pygame.image.load("/home/pi/RaspberrySplit/Theme/NonRetina/Box.png")
    blue = pygame.image.load("/home/pi/RaspberrySplit/Theme/NonRetina/Blue.png")

    s1 = pygame.image.load("/home/pi/RaspberrySplit/Theme/NonRetina/Shutdown1.png")
    s2 = pygame.image.load("/home/pi/RaspberrySplit/Theme/NonRetina/Shutdown2.png")
    s3 = pygame.image.load("/home/pi/RaspberrySplit/Theme/NonRetina/Shutdown3.png")

    cont2 = pygame.image.load("/home/pi/RaspberrySplit/Theme/NonRetina/Cont2.png")
else:
    gray = pygame.image.load("/home/pi/RaspberrySplit/Theme/Retina/BG.png")
    handheld = pygame.image.load("/home/pi/RaspberrySplit/Theme/Retina/Handheld.png")
    STTV = pygame.image.load("/home/pi/RaspberrySplit/Theme/Retina/STTV.png")

    box = pygame.image.load("/home/pi/RaspberrySplit/Theme/Retina/Box.png")
    blue = pygame.image.load("/home/pi/RaspberrySplit/Theme/Retina/Blue.png")

    s1 = pygame.image.load("/home/pi/RaspberrySplit/Theme/Retina/Shutdown1.jpg")
    s2 = pygame.image.load("/home/pi/RaspberrySplit/Theme/Retina/Shutdown2.jpg")
    s3 = pygame.image.load("/home/pi/RaspberrySplit/Theme/Retina/Shutdown3.jpg")

    cont2 = pygame.image.load("/home/pi/RaspberrySplit/Theme/Retina/Cont2.png")

#Blank image for last box, that you're not supposed to access:
gd = pygame.image.load("/home/pi/RaspberrySplit/Theme/Blank.png")
pleasewait = pygame.image.load("/home/pi/RaspberrySplit/Theme/NonRetina/Loading.png")

joy = True

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((480*dpi, 320*dpi), pygame.FULLSCREEN, 16)
done = False
clock = pygame.time.Clock()
selected = 0
selectedName = "ERRR"

rootdir = '/boot/Games/GameFiles'

#Discover games on SD card
for subdir, dirs, files in os.walk(rootdir):
    i = 0
    for file in files:
        file_name = os.path.splitext(file)[0]
        print("file " + file)
        print("filename " + file_name)
        if (file != file_name and file[0] != "."):
            if (i == 0):
                selectedName = file_name
            images.append(pygame.image.load("/boot/Games/BoxArt/" + file_name + "@" + str(dpi) + "x.png"))
            boxes.append(gamebox(i, images[i], file_name, "/boot/Games/GameFiles/" + file_name + ".32bit"))
            i += 1

boxes.append(gamebox(maxed + 1, gd, "NO GAMES", "/home/pi/RaspberrySplit/Apps/gpsp/gba_bios.bin"))
boxes.append(gamebox(maxed + 1, gd, "", "/home/pi/RaspberrySplit/Apps/gpsp/gba_bios.bin"))
boxes.append(gamebox(maxed + 1, gd, "", "/home/pi/RaspberrySplit/Apps/gpsp/gba_bios.bin"))

#Load and play the menu music:
file = '/home/pi/RaspberrySplit/Sound/MenuMusic.mp3'
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=4, buffer=512)
pygame.mixer.music.load(file)
pygame.mixer.music.play()

#Load SEs:
sl = pygame.mixer.Sound("/home/pi/RaspberrySplit/Sound/Select.wav")
att = pygame.mixer.Sound("/home/pi/RaspberrySplit/Sound/Warn.wav")
swi = pygame.mixer.Sound("/home/pi/RaspberrySplit/Sound/Switch.wav"),
att2 = pygame.mixer.Sound("/home/pi/RaspberrySplit/Sound/Attention.wav")
back = pygame.mixer.Sound("/home/pi/RaspberrySplit/Sound/Select2.wav")
sle = pygame.mixer.Sound("/home/pi/RaspberrySplit/Sound/Click.wav")
power = pygame.mixer.Sound("/home/pi/RaspberrySplit/Sound/PowerOff.wav")

#Set the volume of menu SEs to slightly lower:
va = 0.5
sl.set_volume(va)
att.set_volume(va)
att2.set_volume(va)
back.set_volume(va)
sle.set_volume(va)
power.set_volume(va)

#Unused:
currentmode = 0

modes = [handheld, handheld]
textmodes = [STTV, STTV]

#Draw menu:
def draw():
    screen.blit(gray, (0, 0))
    screen.blit(modes[currentmode], (23*dpi, 280*dpi))
    screen.blit(textmodes[currentmode], (145*dpi, 290*dpi))

    pygame.display.flip()

#Update menu:
oldselect = -1

sselect = 1

def draw2():
    global txx
    global oldselect
    global selected
    global boxes
    screen.blit(gray, (0, 0))
    #screen.blit(gray, (23, 280))
    if not oldselect == selected:
        for box in boxes:
            box.draw()
    textsurface = myfont.render(selectedName, False, (61,197,190))
    screen.blit(textsurface,((20+txx)*dpi,68*dpi))

    tgr = textsurface.get_rect()
    if not pygame.Rect(19*dpi, 68*dpi, (tgr.width/dpi+txx)*dpi, 23*dpi).colliderect(pygame.Rect(20*dpi,68*dpi,169*dpi,23*dpi)):
        txx = 169

    if oldselect == selected:
        pygame.display.update([pygame.Rect(20*dpi,68*dpi,169*dpi,23*dpi)])
    else:
        pygame.display.update([boxes[0].rect,boxes[1].rect,boxes[2].rect,pygame.Rect(20*dpi,68*dpi,169*dpi,23*dpi), pygame.Rect(0,91*dpi,480*dpi,157*dpi)])
        oldselect = selected

#Draw shutdown screen:
def draw3():
    global sselect
    if sselect == 1:
        screen.blit(s1, (0, 0))
    if sselect == 0:
        screen.blit(s2, (0, 0))
    pygame.display.flip()

#Update shutdown screen:
def draw4():
    global sselect
    if sselect == 1:
        screen.blit(s1, (0, 0))
    if sselect == 0:
        screen.blit(s2, (0, 0))
    pygame.display.update([pygame.Rect(81*dpi,205*dpi,312*dpi,90*dpi)])

#Draw final shutdown screen:
def draw5():
    screen.blit(s3, (0, 0))
    pygame.display.flip()

#Draw controller reconnection screen:
def draw6():
    screen.blit(cont2, (0, 0))
    pygame.display.flip()

a = True
tick = 0
tbt = 0
frame = 0
draw()

if (os.popen('cat /home/pi/connected').read() == "0\n"):
    screen.blit(pleasewait, (0, 0))
    pygame.display.update([pygame.Rect(149*dpi,148*dpi,182*dpi,21*dpi)])
    while True:
        clock.tick(120)
        frame += 1
        if (frame == 60):
            frame = 0
            if (os.popen('cat /home/pi/connected').read() == "1\n"):
                break

pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
print ("There is ", joystick_count, "joystick/s")
if joystick_count == 0:
    print ("Error, I did not find any joysticks")
    joy = False
else:
    j = pygame.joystick.Joystick(0)
    j.init()

#Play start-up sound:
att2.play()

def get():
    out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    it = 0 #iterator
    pygame.event.pump()

    #Read input from the two joysticks
    for i in range(0, j.get_numaxes()):
        out[it] = j.get_axis(i)
        it+=1
    #Read input from buttons
    for i in range(0, j.get_numbuttons()):
        out[it] = j.get_button(i)
        it+=1
    return out

#while True:
#    print(get())

lastevent1 = 0
lastevent2 = 0
shutdown = False;
apress1 = False;
apress2 = False;
otherfb = False;
apress3 = False;
apress4 = False;

sargv = sys.argv[1]

gameselected = False;

joy = False

dr = False
dl = False
du = False
dd = False

fa = False
fb = False
fx = False
fy = False

shl = False
shr = False

start = False
select = False

lastevent3 = 0

def volumeroutine():
    global apress3
    global apress4
    global vol
    if fx and not apress3:
        apress3 = True
        vol += 1
        set_vol()
        sle.play()
    if fy and not apress4:
        apress4 = True
        vol -= 1
        set_vol()
        sle.play()
    if not fx:
        apress3 = False
    if not fy:
        apress4 = False

pygame.event.set_grab(False)

def getInput():
    global dr
    global dl
    global du
    global dd
    global fa
    global fb
    global fx
    global fy
    global shl
    global shr
    global start
    global select
    global lastevent1
    global lastevent2
    pygame.event.pump()
    #+ Control Pad
    if j.get_button(8) and not du:
        du = True
    if j.get_button(9) and not dd:
        dd = True
    if j.get_button(10) and not dl:
        dl = True
    if j.get_button(11) and not dr:
        dr = True

    #Face buttons
    if j.get_button(0) and not fa:
        fa = True
    if j.get_button(1)and not fb:
        fb = True
    if j.get_button(2) and not fx:
        fx = True
    if j.get_button(3) and not fy:
        fy = True

    #Shoulder buttons
    if j.get_button(4) and not shl:
        shl = True
    if j.get_button(5) and not shr:
        shr = True

    #Start/Select buttons
    if j.get_button(6) and not start:
        start = True
    if j.get_button(7) and not select:
        select = True

    #+ Control Pad
    if not j.get_button(8) and du:
        lastevent2 = 0
        du = False
    if not j.get_button(9) and dd:
        lastevent2 = 0
        dd = False
    if not j.get_button(10) and dl:
        lastevent1 = 0
        dl = False
    if not j.get_button(11) and dr:
        lastevent1 = 0
        dr = False

    #Face buttons
    if not j.get_button(0) and fa:
        fa = False
    if not j.get_button(1) and fb:
        fb = False
    if not j.get_button(2) and fx:
        fx = False
    if not j.get_button(3) and fy:
        fy = False

    #Shoulder buttons
    if not j.get_button(4) and shl:
        shl = False
    if not j.get_button(5) and shr:
        shr = False

    #Start/Select buttons
    if not j.get_button(6) and start:
        start = False
    if not j.get_button(7) and select:
        select = False

while not done:
        if not shutdown:
            if not gameselected:
                if tbt < 60:
                    tbt += 1
                if tbt == 60:
                    tick += 1
                    if tick == 1:
                        txx -= 1
                        tick = 0
                        a = True

        getInput()

        if dr and lastevent1 != -1:
            lastevent1 = -1
            if selected < maxed-3 and not shutdown:
                selected += 1
                os.environ['SWITCH_GAME'] = boxes[selected].file
                a = True
                txx = 0
                tbt = 0
                sl.play()
                if selected > 1:
                    scroll -= 178

        if dl and lastevent1 != 1:
            lastevent1 = 1
            if selected > 0 and not shutdown:
                selected -= 1
                os.environ['SWITCH_GAME'] = boxes[selected].file
                a = True
                txx = 0
                tbt = 0
                sl.play()
                if selected > 1:
                    scroll += 178
                if selected == 1:
                    scroll = 0

        if du and lastevent2 != 1:
            lastevent2 = 1
            if shutdown:
                sl.play()
                sselect = 0
                a = True

        if dd and lastevent2 != -1:
            lastevent2 = -1
            if shutdown:
                sl.play()
                sselect = 1
                a = True

        if shl and shr and start and select:
            if not shutdown:
                draw3()
                att.play()
                shutdown = True;
                pygame.mixer.music.pause()

        if fa and not apress1:
            apress1 = True
            if shutdown and sselect == 0:
                draw5()
                sle.play()
                power.play()
                time.sleep(2)
                break

            #____SWITCH AND PLAY____
            elif not shutdown and not gameselected:
                #Play Menu Click Sound
                pygame.mixer.music.pause()
                sle.play()
                gameselected = True

                #Refresh Framebuffer
                draw()

                #Show Emulator on FB0 (Is this needed?)
                os.environ["SDL_FBDEV"] = "/dev/fb0"
                os.environ['SDL_VIDEODRIVER'] = 'fbcon'

                #Start game in certain way depending on SARGV FB
                if sargv == "0":
                    os.system("/home/pi/RaspberrySplit/Scripts/StartGameTV.sh")
                else:
                    os.system("/home/pi/RaspberrySplit/Scripts/StartGame.sh")

                #DISABLE Suspend Timer
                timed = False
                timer = 0

                while True:
                    #Keep Getting Key/Pad Events
                    getInput()

                    #IF X or Y is Pressed:
                    if fx and fy and not timed and not apress2:
                        apress2 = True
                        #Play "Switch" Sound
                        sle.play()
                        if sargv == "0":
                            time.sleep(1.5)
                        else:
                            time.sleep(0.5)

                        #Switch FB, SARGV, and run Script
                        if sargv == "0":
                            sargv = "1"
                            os.system("vcgencmd display_power 0 &")
                            os.system("/home/pi/RaspberrySplit/Scripts/CopyFrames.sh")
                            os.system("sudo amixer cset numid=3 1")
                            otherfb = not otherfb
                        else:
                            sargv = "0"
                            os.system("vcgencmd display_power 1 &")
                            os.system("/home/pi/RaspberrySplit/Scripts/DontCopyFrames.sh")
                            os.system("( sleep 1 ; cat /home/pi/RaspberrySplit/Overlay/SwitchFromTV.raw >/dev/fb1 ) &")
                            os.system("sudo amixer cset numid=3 2")
                            otherfb = not otherfb
                    if not ( fx and fy ):
                        apress2 = False

                    volumeroutine()
                    if (frame == 60):
                        frame = 0
                        if (not timed and os.popen('cat /home/pi/connected').read() == "0\n"):
                            att.play()
                            os.system("/home/pi/RaspberrySplit/Apps/pngview -n /home/pi/RaspberrySplit/Theme/Retina/Cont1.png &")
                            os.system("/home/pi/RaspberrySplit/Scripts/PauseGame.sh")
                            while True:
                                clock.tick(120)
                                frame += 1
                                if (frame == 60):
                                    frame = 0
                                    if (os.popen('cat /home/pi/connected').read() == "1\n"):
                                        att2.play()
                                        while True:
                                            getInput()
                                            if fx:
                                                apress3 = True
                                                break
                                            if fy:
                                                apress4 = True
                                                break
                                            clock.tick(120)
                                        sle.play()
                                        os.system("/home/pi/RaspberrySplit/Scripts/ResumeGame.sh")
                                        break

                    #IF START and SELECT are Pressed:
                    if start and select and not timed:
                        #Play Warning Sound
                        att.play()

                        #PAUSE Game and Show Suspend Menu
                        os.system("/home/pi/RaspberrySplit/Apps/pngview -n /home/pi/RaspberrySplit/Overlay/Cancel.png &")
                        os.system("/home/pi/RaspberrySplit/Scripts/PauseGame.sh")

                        #Start Suspend Timer
                        timed = True
                        timer = 0

                    #IF the Suspend Timer is ON:
                    if timed:
                        #Increment the Timer by 1 every frame
                        timer += 1

                        #If any Face Button is pressed
                        if fa or fb or fx or fy:
                            #Turn the Suspend Timer OFF
                            timed = False
                            #RESUME Game and Hide Suspend Menu
                            os.system("/home/pi/RaspberrySplit/Scripts/ResumeGame.sh")
                    #Quit if the Timer is Greater Than 2.5 Seconds
                    if timer > 300:
                        break
                    #Wait 60 Frames
                    clock.tick(120)
                    frame += 1

                #Play Menu Boot Sound
                att2.play()

                #End the Game
                #if sargv == "0":
                os.system("/home/pi/RaspberrySplit/Scripts/ResumeGame.sh")
                os.system("/home/pi/RaspberrySplit/Scripts/QuitGame.sh")

                #RESTART the Program if the FB was Switched
                if otherfb:
                    time.sleep(0.5)
                    os.system("/home/pi/RaspberrySplit/Scripts/QuitGame.sh &")
                    break

                #Refresh the Menu
                gameselected = False
                #if sargv == "0":
                time.sleep(0.1)
                draw()
                oldselect = 999

                #RESTART the Menu Music
                #pygame.mixer.music.rewind()
                pygame.mixer.music.unpause()

            if shutdown and sselect == 1:
                draw()
                oldselect = 999
                draw2()
                back.play()
                shutdown = False
                pygame.mixer.music.unpause()

        if not fa:
            apress1 = False

        if fx and fy:
            break

        volumeroutine()

        if a and not gameselected:
            if shutdown:
                draw4()
            else:
                draw2()
            a = False

        if (frame == 60):
            frame = 0
            if (os.popen('cat /home/pi/connected').read() == "0\n"):
                pygame.mixer.music.pause()
                att.play()
                draw6()
                while True:
                    clock.tick(120)
                    frame += 1
                    if (frame == 60):
                        frame = 0
                        if (os.popen('cat /home/pi/connected').read() == "1\n"):
                            att2.play()
                            while True:
                                getInput()
                                if fx:
                                    apress3 = True
                                    break
                                if fy:
                                    apress4 = True
                                    break
                                clock.tick(120)
                            pygame.mixer.music.unpause()
                            sle.play()
                            draw()
                            oldselect = 999
                            draw2()
                            break

        clock.tick(120)
        frame += 1
if not shutdown:
    os.system("/home/pi/RaspberrySplit/Scripts/Switch.sh &")
    time.sleep(0.1)
else:
    os.system("/home/pi/RaspberrySplit/Shutdown/Shutdown.sh &")

sys.exit(0)
