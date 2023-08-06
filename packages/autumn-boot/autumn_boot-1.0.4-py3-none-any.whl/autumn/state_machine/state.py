from typing import Callable, Dict

from ..repository.storable import Storable


class State:
    def __init__(self, name, context=None):
        self.name = name
        self.next_states = {}
        self.context: Storable = context
        self.transition_listeners: 'Dict[State, Callable[[Storable], None]]' = {}

    def add_allowed_transition(self, trigger, next_state):
        assert issubclass(type(next_state), State), "Only objects dervied from state must be submitted"
        assert trigger not in self.next_states, 'Only one state transition permitted per trigger'
        self.next_states[trigger] = next_state

    def is_transition_allowed(self, trigger):
        return trigger in self.next_states.keys()

    def get_transition_state(self, trigger) -> 'State':
        assert self.is_transition_allowed(trigger), f'Transition is not allowed from {self.name} with {trigger}'
        next_state = self.next_states[trigger]
        print(f'Transitioning from {self.name} to {next_state.name}')
        if next_state in self.transition_listeners:
            executable: Callable[[Storable], None] = self.transition_listeners[next_state]
            executable(self.context)

        return self.next_states[trigger]

    def on_transition_to(self, to_state: 'State', a_callable: Callable[[Storable], None]):
        assert to_state in self.next_states.values(), f'Transition from {self.name} to {to_state.name} is not allowed!' \
                                                      f'awailable states: {[state.name for state in self.next_states.values()]}'
        self.transition_listeners[to_state] = a_callable

    def __str__(self):
        return self.name

    def to_dict(self):
        allowed_states = dict([(trigger, state.name) for trigger, state in self.next_states.items()])
        return {
            'name': self.name,
            'allowed_stated': allowed_states
        }
