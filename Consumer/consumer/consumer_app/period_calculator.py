from .entities import Action,Period
from typing import List,Tuple

def last(arr: List):
    """
        Returns the last element in an array. 
        In case the array is empty- returns None.
    """
    if len(arr) == 0:
        return None
    else:
        return arr[len(arr) - 1]

class PeriodCalculator:
    """
        Calculates the periods from the actions. 
        
        Its base assumptions are:
        1. Every action before the first "start" should be ignored.
        2. "start" as the last action should be ignored.
        3. "cancel_start" after a "stop" should be ignored (when wasn't a "start" between).
        4. "cancel_stop" after a "start" should be ignored (when wasn't a "stop" between).
        5. In case of sequence of "start" or "stop" - 
           we should take the action with the latest activation date.
        6. There isn't a guide for dealing with "start" and "stop" with the same activation date.
    """

    def calculate(self, actions: List[Action])-> List[Period]:
        """
            This method calculates the periods according the actions. 
            It assumes that the actions are ordered according "activation_date".
        """

        periods = []
        starts, stops = self.__create_positions(actions)

        # If there aren't positions - there aren't periods
        if len(starts) != 0:
            # The positions are ordered that for every "start" has a "stop" partner at the same index.
            # They "builds" the period (-:
            for index in range(0, len(starts)):
                start_action = actions[starts[index]]
                stop_action = actions[stops[index]]

                periods.append(Period(start_action.date, stop_action.date))

        return periods

    def calculate2(self, actions: List[Action]) -> List[Period]:
        cleaned_actions: List[Action] = []

        for action in actions:
            if action.is_start():
                # Wern't actions or the last action was stop - append the action
                if len(cleaned_actions) == 0 or last(cleaned_actions).is_stop():
                    cleaned_actions.append(action)
                # The last action was start - remove it and take this action (latest choice)
                else:
                    cleaned_actions.pop()
                    cleaned_actions.append(action)
            elif action.is_stop():
                # The first action must be "start"
                if len(cleaned_actions) == 0:
                    pass
                # The last action is start - append the action
                elif last(cleaned_actions).is_start():
                    cleaned_actions.append(action)
                # The last action is stop - remove it and take this action (latest choice)
                else:
                    cleaned_actions.pop()
                    cleaned_actions.append(action)
            elif action.is_cancel_start():
                # The last action is start - remove it. If last is stop- do nothing.
                if len(cleaned_actions) != 0 and last(cleaned_actions).is_start():
                    cleaned_actions.pop()
            elif action.is_cancel_stop():
                # The last action is stop - remove it. If last is start- do nothing.
                if len(cleaned_actions) != 0 and last(cleaned_actions).is_stop():
                    cleaned_actions.pop()

        # In the case the last action is start - we should remove it because the last 
        # must be stop
        if len(cleaned_actions) != 0 and last(cleaned_actions).is_start():
            cleaned_actions.pop()

        # "cleaned_actions" consists from pairs of "start" and "stop". 
        # Therefore, we are going to iterate over it create the periods from the pairs
        periods = []
        index = 0
        while index < len(cleaned_actions):
            start_action = cleaned_actions[index]
            stop_action = cleaned_actions[index + 1]

            periods.append(Period(start_action.date, stop_action.date))
            index += 2

        return periods



    def __create_positions(self, actions: List[Action])-> Tuple:
        """
            This method gets all actions and creates the positions of "starts" and "stops" according 
            the assumptions above.
            It returns a pair of positions - ("starts", "stops")
        """
        starts, stops = [], []

        # Iterate over the actions and create the "start" and "stop" positions according them
        for index in range(0, len(actions)):
            self.__create_positions_according_action(starts, stops, actions, index)
            
        # "start" is not allowed to be the last action.
        if last(starts) != None and (last(stops) == None or last(stops) < last(starts)):
            starts.pop()

        return starts, stops

    def __create_positions_according_action(self, starts, stops, actions, action_index):
        action = actions[action_index]

        if action.is_stop():
            # "stop" in the begining - ignore
            if last(starts) == None:
                return

            # last action was "start" - append position
            elif last(stops) == None or last(stops) < last(starts):
                stops.append(action_index)

            # last action was "stop" - 
            # remove its position and append the current (we take the later)
            else:
                stops.pop()
                stops.append(action_index)
        elif action.is_start():
            # This is the first action - append position
            if last(starts) == None:
                starts.append(action_index)
            
            # The previous was "stop"
            elif last(stops) != None and last(stops) > last(starts):
                starts.append(action_index)
            
            # The previous was "start" - 
            # remove its position and append the current (we take the later)
            else:
                starts.pop()
                starts.append(action_index)

        # Action is "cancel_stop" and the last action was "stop" - remove it
        elif action.is_cancel_stop() and last(stops) != None and last(stops) > last(starts):
            stops.pop()

        # Action is "cancel_start" and the last action was "start" - remove it
        elif action.is_cancel_start() and last(starts) != None \
                and (last(stops) == None or last(starts) > last(stops)):
            starts.pop()

