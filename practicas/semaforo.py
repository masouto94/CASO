from abc import ABC, abstractmethod



class Process(ABC):
    x = 0
    def __init__(self, type:str, name:str):
        self.type = type
        self.name = name
        self.status = "pending"
    @staticmethod
    @abstractmethod
    def dijkstra_p():
        pass

    @staticmethod
    @abstractmethod
    def dijkstra_v():
        pass
    
    def getCurrentStatus(self):
        return self.__class__.x

    def execute(self):
        print(f"Ejecutando {self.type}->{self.name}")
        self.status = "executed"
    
    def wait(self):
        print(f"El proceso {self.type}->{self.name} está encolado")

class Process_A(Process):
    x = 1
    def __init__(self, name):
        super().__init__("A", name)
    
    def routeNext(self):
        return Process_B
    
    @staticmethod
    def processType():
        return "A"    
    
    @staticmethod
    def dijkstra_p():
        Process_A.x -= 1

    @staticmethod
    def dijkstra_v():
        Process_A.x += 1

class Process_B(Process):
    x = 0
    def __init__(self, name):
        super().__init__("B", name)

    def routeNext(self):
        return Process_A
    
    @staticmethod
    def processType():
        return "B"
    @staticmethod
    def dijkstra_p():
        Process_B.x -= 1

    @staticmethod
    def dijkstra_v():
        Process_B.x += 1

class Queue(ABC):

    def __init__(self):
        self.queue = []
        self.waiting = []

    def addProcess(self, process: Process):
        self.queue.append(process)

    def runProcess(self, process, signal=False):
        if signal:
            process.execute()
            process.routeNext().dijkstra_v()
            return 
        process.dijkstra_p()
        if process.getCurrentStatus() < 0:
            process.wait()
            self.waiting.append(process)
        else:
            process.execute()
            process.routeNext().dijkstra_v()
    def popProcess(self, process):
        return self.queue.pop(self.queue.index(process))
    
    def requeueProcess(self, processType: str):
        processIndex=list(map(lambda process: process.type, self.queue)).index(processType)
        return self.waiting.pop(processIndex)
    
    
    def runQueue(self):
        while any(filter(lambda process: process.status == "pending", self.queue)):
          
            for process in filter(lambda process: process.status == "pending", self.queue):
                # process.dijkstra_p()
                # if process.getCurrentStatus() < 0:
                #     process.wait()
                #     self.waiting.append(process)
                # else:
                #     process.execute()
                #     process.routeNext().dijkstra_v()
                self.runProcess(process)
                if process.routeNext().x <= 0 and process.getCurrentStatus() <= 0:
                    self.runProcess(self.requeueProcess(process.routeNext().processType()), True)
                    
                

    

class ProcessQueue(Queue):
    def __init__(self):
        super().__init__()


processQueue = ProcessQueue()
a_processes = [Process_A(f"Proceso_A n°{i}") for i in range(3)]
b_processes = [Process_B(f"Proceso_B n°{i}") for i in range(3)]

readyQueue = []
readyQueue.extend(a_processes)
readyQueue.extend(b_processes)

for i in readyQueue:
    processQueue.addProcess(i)

processQueue.runQueue()