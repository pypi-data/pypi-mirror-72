from ..repository.storable import Storable
from .state import State
from .state_configurator import StateConfigurator
from .state_machine import StateMachine


class StateMachineBuilder:
    def __init__(self, context: Storable):
        self.starting_state = None
        self.states = {}
        self.context = context

    def add_state(self, *args):
        for name in args:
            assert name not in self.states
        for name in args:
            self.states[name] = State(name, context=self.context)

    def configure(self, name):
        assert name in self.states

        return StateConfigurator(self.states[name], self)

    def set_initial_state(self, name):
        assert name in self.states

        self.starting_state = self.states[name]

        return self

    def build(self):
        assert self.starting_state, 'No starting state defined!'

        return StateMachine(self.context, self.starting_state, self.states.values())
