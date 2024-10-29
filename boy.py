from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT

from state_machine import StateMachine, space_down, time_out, right_down, left_up, left_down, right_up, start_event


class Idle:
    @staticmethod
    def enter(boy, e):
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1
        boy.dir = 0
        boy.frame = 0
        #현재 시간을 저장
        boy.start_time = get_time()
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)



class Sleep:
    @staticmethod
    def enter(boy, e):

        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:   #오른쪽 바라보는 사태에서 눕기
            boy.image.clip_composite_draw(
                boy.frame *100, 300, 100, 100,
                3.141592/2, # 90도 회전
                '', # 좌우상하 반전 X
                boy.x - 25, boy.y - 25, 100, 100
            )
        elif boy.face_dir == -1 :
            boy.image.clip_composite_draw(
                boy.frame * 100, 200, 100, 100,
                -3.141592 / 2,  # 90도 회전
                '',  # 좌우상하 반전 X
                boy.x + 25, boy.y - 25, 100, 100
            )






class Run :

    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e): #오른쪽으로 달리기
            boy.dir,  boy.action = 1, 1

        elif left_down(e) or right_up(e): #왼쪽으로 달리기
            boy.dir, boy.action = -1, 0




    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir * 5
        boy.frame = (boy.frame + 1) % 8


    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action *100, 100, 100, boy.x, boy.y)






class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3

        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체의 state machine 생성
        self.state_machine.start(Idle) # 초기 상태가 Idle
        self.state_machine.set_transitions(
            {
                Idle : {right_down: Run, left_down: Run, left_up :Run, right_up: Run, time_out : Sleep },
                Sleep : {right_down:Run, left_down: Run, right_up:Run, left_up:Run, space_down : Idle},
                Run : {right_down:Idle, left_down:Idle, right_up:Idle, left_up:Idle},

                AutoRun : {}

            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        #event : 입력 이벤트 key, mouse
        #우리가 state machine 전달해줄껀 (  ,  ) - 튜플

        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()