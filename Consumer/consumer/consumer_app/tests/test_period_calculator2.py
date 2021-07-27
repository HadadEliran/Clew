from consumer_app.entities import Action, Period
from unittest import TestCase
from consumer_app.period_calculator import PeriodCalculator

class Calculate2Tests(TestCase):
    @staticmethod
    def test_ThereAreNotActions_ReturnsNonePeriods():
        actions = []
        periods = PeriodCalculator().calculate2(actions)
        assert periods == []

    @staticmethod
    def test_StartIsNotExist_ReturnsNonePeriods():
        actions = []

        actions.append(Action.stop("22-2-2010"))
        actions.append(Action.cancel_stop("23-2-2010"))
        actions.append(Action.cancel_start("24-2-2010"))
    
        periods = PeriodCalculator().calculate2(actions)
        assert periods == []

    @staticmethod
    def test_StartIsExistButNotInTheBegin_IgnoreBefore():
        actions = []

        actions.append(Action.stop("22-2-2010"))
        actions.append(Action.cancel_stop("23-2-2010"))
        actions.append(Action.cancel_start("24-2-2010"))
        actions.append(Action.start("25-2-2010"))
        actions.append(Action.stop("26-2-2010"))

        periods = PeriodCalculator().calculate2(actions)
        assert periods == [Period("25-2-2010", "26-2-2010")]

    @staticmethod
    def test_StartIsTheEnd_IgnoreIt():
        actions = []

        actions.append(Action.start("25-2-2010"))
        actions.append(Action.stop("26-2-2010"))
        actions.append(Action.start("27-2-2010"))

        periods = PeriodCalculator().calculate2(actions)
        assert periods == [Period("25-2-2010", "26-2-2010")]

    @staticmethod
    def test_SequenceOfStart_TakeTheLast():
        actions = []

        actions.append(Action.start("25-2-2010"))
        actions.append(Action.start("26-2-2010"))
        actions.append(Action.start("27-2-2010"))
        actions.append(Action.stop("28-2-2010"))

        periods = PeriodCalculator().calculate2(actions)
        assert periods == [Period("27-2-2010", "28-2-2010")]

    @staticmethod
    def test_SequenceOfStop_TakeTheLast():
        actions = []

        actions.append(Action.start("25-2-2010"))
        actions.append(Action.stop("26-2-2010"))
        actions.append(Action.stop("27-2-2010"))
        actions.append(Action.stop("28-2-2010"))
        actions.append(Action.start("1-3-2010"))
        actions.append(Action.stop("2-3-2010"))

        periods = PeriodCalculator().calculate2(actions)
        assert periods == [Period("25-2-2010", "28-2-2010"), Period("1-3-2010", "2-3-2010")]

    @staticmethod
    def test_CancelOfStopAfterStart_IgnoreIt():
        actions = []

        actions.append(Action.start("25-2-2010"))
        actions.append(Action.stop("26-2-2010"))
        actions.append(Action.start("1-3-2010"))
        actions.append(Action.cancel_stop("2-3-2010"))
        actions.append(Action.stop("3-3-2010"))

        periods = PeriodCalculator().calculate2(actions)
        assert periods == [Period("25-2-2010", "26-2-2010"), Period("1-3-2010", "3-3-2010")]

    @staticmethod
    def test_CancelOfStartAfterStop_IgnoreIt():
        actions = []

        actions.append(Action.start("25-2-2010"))
        actions.append(Action.stop("26-2-2010"))
        actions.append(Action.cancel_start("28-2-2010"))
        actions.append(Action.start("1-3-2010"))
        actions.append(Action.stop("3-3-2010"))

        periods = PeriodCalculator().calculate2(actions)
        assert periods == [Period("25-2-2010", "26-2-2010"), Period("1-3-2010", "3-3-2010")]

    @staticmethod
    def test_CancelOfStartAfterStart_RemoveStart():
        actions = []

        actions.append(Action.start("25-2-2010"))
        actions.append(Action.cancel_start("26-2-2010"))
        actions.append(Action.stop("27-2-2010"))
        actions.append(Action.start("1-3-2010"))
        actions.append(Action.cancel_start("2-3-2010"))
        actions.append(Action.start("3-3-2010"))
        actions.append(Action.stop("4-3-2010"))

        periods = PeriodCalculator().calculate2(actions)
        
        # The first and second "start" should be removed
        # In addition, the first "stop" should be removed because it be the first action 
        # after "start" removing

        assert periods == [Period("3-3-2010", "4-3-2010")]

    @staticmethod
    def test_CancelOfStopAfterStop_RemoveStop():
        actions = []

        actions.append(Action.start("25-2-2010"))
        actions.append(Action.stop("27-2-2010"))
        actions.append(Action.start("28-2-2010"))
        actions.append(Action.stop("1-3-2010"))
        actions.append(Action.cancel_stop("2-3-2010"))
        actions.append(Action.stop("4-3-2010"))

        periods = PeriodCalculator().calculate2(actions)
        assert periods == [Period("25-2-2010", "27-2-2010"), Period("28-2-2010", "4-3-2010")]

    @staticmethod
    def test_SequenceOfCancelOfStop_RemoveOnlyLastStop():
        actions = []

        actions.append(Action.start("25-2-2010"))
        actions.append(Action.stop("26-2-2010"))
        actions.append(Action.cancel_stop("27-2-2010"))
        actions.append(Action.cancel_stop("28-2-2010"))
        actions.append(Action.stop("1-3-2010"))

        periods = PeriodCalculator().calculate2(actions)
        assert periods == [Period("25-2-2010", "1-3-2010")]
    
    @staticmethod
    def test_SequenceOfCancelOfStart_RemoveOnlyLastStart():
        actions = []

        actions.append(Action.start("25-2-2010"))
        actions.append(Action.stop("26-2-2010"))
        actions.append(Action.start("27-2-2010"))
        actions.append(Action.cancel_start("28-2-2010"))
        actions.append(Action.cancel_start("1-3-2010"))
        actions.append(Action.start("2-3-2010"))
        actions.append(Action.stop("3-3-2010"))

        periods = PeriodCalculator().calculate2(actions)
        assert periods == [Period("25-2-2010", "26-2-2010"), Period("2-3-2010", "3-3-2010")]