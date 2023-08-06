from typing import Callable

from ..repository.storable import Storable
from .state import State


class StateConfigurator:
    def __init__(self, state, state_machine_builder):
        self.state: State = state
        self.permitted_states = {}
        self.state_machine_builder = state_machine_builder
        self.context = state_machine_builder.context

    def permit(self, trigger, name):
        assert trigger not in self.permitted_states.keys(), 'Only one state transition permitted per trigger'
        assert name in self.state_machine_builder.states, 'State machine does not contain state for ' + name
        self.state.add_allowed_transition(trigger, self.state_machine_builder.states[name])

        return self

    def on_transition_to(self, to_state: str, a_callable: Callable[[Storable], None]):
        assert to_state in self.state_machine_builder.states, 'State is not configurable'
        self.state.on_transition_to(self.state_machine_builder.states[to_state], a_callable)

    def ignore(self, trigger):
        self.state.add_allowed_transition(trigger, self.state)
