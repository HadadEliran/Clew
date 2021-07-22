from datetime import date, datetime

class Action:
    def __init__(self, action_type, action_activation_date:date):
        self.type = str.upper(action_type)
        self.date: datetime = action_activation_date

    #   Factory Methods #
    
    @classmethod
    def start(cls, activation_date:str):
        return Action("START", datetime.strptime(activation_date, '%d-%m-%Y').date())

    @classmethod
    def stop(cls, activation_date:str):
        return Action("STOP", datetime.strptime(activation_date, '%d-%m-%Y').date())

    @classmethod
    def cancel_start(cls, activation_date:str):
        return Action("CANCEL_START", datetime.strptime(activation_date, '%d-%m-%Y').date())

    @classmethod
    def cancel_stop(cls, activation_date:str):
        return Action("CANCEL_STOP", datetime.strptime(activation_date, '%d-%m-%Y').date())

    def is_start(self):
        return self.type == "START"
    
    def is_stop(self):
        return self.type == "STOP"
    
    def is_cancel_start(self):
        return self.type == "CANCEL_START"

    def is_cancel_stop(self):
        return self.type == "CANCEL_STOP"

class Period:
    def __init__(self, start, end):
        if type(start) == str:
            start = datetime.strptime(start, '%d-%m-%Y').date()

        if type(end) == str:
            end = datetime.strptime(end, '%d-%m-%Y').date()
        
        self.start = start
        self.end = end

    def __eq__(self, o: object) -> bool:
        if type(o) is not Period:
            return False

        other: Period = o
        return self.start == other.start and self.end == other.end

    def __str__(self)-> str:
        return f"{self.start} : {self.end}"

    def as_dict(self):
        return {"start":self.start.strftime('%d-%m-%Y'), 
                "end":self.end.strftime('%d-%m-%Y')}
                
    def __repr__(self) -> str:
        return str(self)