import pygame
import math


class MathFun:
    def __init__(self, InStr, NumParams = 2):
        self.Str = InStr
        self.Exc = compile(InStr, "<string>", "eval")
        self.NumParams = NumParams
    def Eval(self, *Args):
        try:
            if self.NumParams == 2:
                x, y = Args[0], Args[1]
                return eval(self.Exc)
            elif self.NumParams == 1:
                x = Args[0]
                return eval(self.Exc)
        except:
            return None
class Integral:
    def __init__(self, Func):
        self.Func = Func
    def EvalLeft(self, x0, x1, step):
        Rtn = 0
        x = x0
        while x < x1:
            Rtn += eval(self.Func.Exc) * step
            x += step
        return Rtn
    def EvalRight(self, x0, x1, step):
        Rtn = 0
        x = x0
        while x < x1:
            x += step
            Rtn += eval(self.Func.Exc) * step
        return Rtn
    def EvalTrap(self, x0, x1, step):
        Rtn = 0
        x = x0
        Prev = eval(self.Func.Exc) / .5
        x += step
        while x < x1:
            Mid = eval(self.Func.Exc) / .5
            Rtn += (Prev + Mid) * step
            Prev = Mid
            x += step
        return Rtn
def ln(x):
    return math.log1p(x-1)
def logbase(b, x):
    return math.log(x, b)
def GetLenX(Len, Slope):
    return (float(Len ** 2) / ((Slope ** 2) + 1)) ** .5
pi = math.pi
sin = math.sin
cos = math.cos
tan = math.tan
arcsin = math.asin
arccos = math.acos
arctan = math.atan
log = math.log10
e = math.e
LnColor = (255, 255, 255)
Scale = .08
ScaleInt = .01
LnW = 1
def DrawLn(x, y, Slope, Surf, Len, Col):
    AbsX = GetLenX(Len / 2, Slope)
    AbsY = (Len / 2) ** 2 - AbsX ** 2
    AbsX1 = x - AbsX
    AbsX2 = x + AbsX
    AbsY1 = y + AbsY
    AbsY2 = y - AbsY
    AbsX1 += Base[0]
    AbsX2 += Base[0]
    AbsY1 += Base[1]
    AbsY2 += Base[1]
    pygame.draw.line(Surf, Col, (AbsX1, AbsY1), (AbsX2, AbsY2), LnW)
ColGrid = [(0, 0, 255), (255, 0, 255), (255, 255, 255), (0, 255, 255), (255, 0, 0)]
def DrawGrid(Surf, Func, Width, Height, Spacing):
    for y in xrange(-Height / 2, Height / 2, Spacing):
        for x in xrange(-Width / 2, Width / 2, Spacing):
            Slope = Func.Eval(float(Scale * x) / Spacing + FunOff[0], -(float(Scale * y) / Spacing + FunOff[1]))
            if Slope != None:
                Quadrant = 0
                x1 = float(Scale * x) / Spacing + FunOff[0]
                y1 = float(Scale * y) / Spacing + FunOff[1]
                if x1 < 0 and y1 <= 0:
                    Quadrant = 1
                elif x1 > 0 and y1 > 0:
                    Quadrant = 3
                elif x1 <= 0 and y1 > 0:
                    Quadrant = 2
                DrawLn(x, y, Slope, Surf, Spacing, ColGrid[Quadrant])
pygame.display.init()
pygame.font.init()
MonW = pygame.display.Info().current_w
MonH = pygame.display.Info().current_h
OrigW = 1280
OrigH = 700
Surface = pygame.display.set_mode((OrigW, OrigH))
FunOff = (0, 0)
CurrFun = None
DragOn = False
Spacer = 8
CurrW, CurrH = Surface.get_size()
Base = (CurrW/2, CurrH/2)
IsFullscr = False

while True:
    Evt = pygame.event.wait()
    if Evt.type == pygame.QUIT:
        break
    elif Evt.type == pygame.MOUSEBUTTONDOWN:
        if Evt.button == 5:
            Scale += ScaleInt
        elif Evt.button == 4 and Scale >= ScaleInt:
            Scale -= ScaleInt
        elif Evt.button == 1:
            DragOn = True
        if CurrFun != None:
            Surface.fill((0,0,0))
            DrawGrid(Surface, CurrFun, CurrW, CurrH, Spacer)
            pygame.display.update()
    elif Evt.type == pygame.MOUSEBUTTONUP:
        if Evt.button == 1:
            DragOn = False
    elif Evt.type == pygame.MOUSEMOTION:
        if DragOn and CurrFun != None:
            FunOff = (FunOff[0] - (Evt.rel[0] * Scale) / Spacer), (FunOff[1] - (Evt.rel[1] * Scale) / Spacer)
            Surface.fill((0,0,0))
            DrawGrid(Surface, CurrFun, CurrW, CurrH, Spacer)
            pygame.display.update()
    elif Evt.type == pygame.KEYDOWN:
        if Evt.key == pygame.K_RETURN:
            CurrFun = MathFun(raw_input("give me function of x and y: "))
            Surface.fill((0,0,0))
            DrawGrid(Surface, CurrFun, CurrW, CurrH, Spacer)
            pygame.display.update()
        elif Evt.key == pygame.K_c:
            if CurrFun != None:
                FunOff = (0, 0)
                Surface.fill((0,0,0))
                DrawGrid(Surface, CurrFun, CurrW, CurrH, Spacer)
                pygame.display.update()
        elif Evt.key == pygame.K_F11:
            IsFullscr = not IsFullscr
            if IsFullscr: Surface = pygame.display.set_mode((MonW, MonH), pygame.FULLSCREEN)
            else: Surface = pygame.display.set_mode((OrigW, OrigH))
            CurrW, CurrH = Surface.get_size()
            Base = (CurrW / 2, CurrH / 2)
            if CurrFun != None:
                Surface.fill((0,0,0))
                DrawGrid(Surface, CurrFun, CurrW, CurrH, Spacer)
                pygame.display.update()
pygame.quit()
