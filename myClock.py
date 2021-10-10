import time
class Clock:
    
    def __init__(self, name:str='Clock',  seconds=0) -> None:
        self.name = name
        self.seconds = seconds

    # (self) -> Clock
    def time(self):
        return Clock(self.name, time.time() )

    #(self, other: Clock) 
    def compare_time(self, other) -> str:
        seconds = self.seconds - other.seconds
        return f'{self.name}: {seconds} seconds'

    def time_this(func:callable, args:list=[]):
        clock = Clock().time()
        # type quit to see the time
        func(*args)
        print(Clock('RunTime').time().compare_time(clock))

    def __repr__(self) -> str:
        return f'{self.name}: {self.seconds} seconds'