from .state import State
from ..repository.storable import Storable


class StateMachine:
    def __init__(self, context, starting_state, states):
        self.initial_state = starting_state
        self.current_state = starting_state
        self.states = states
        self.context: Storable = context

    def next(self, trigger):
        self.current_state = self.current_state.get_transition_state(trigger)

    def __str__(self):
        return str(self.current_state)

    def to_dict(self):
        def get_all_connections(starting_state, arr=None, traversed=None):
            if traversed is None:
                traversed = []
            if arr is None:
                arr = []
            if starting_state not in traversed:
                for trigger, allowed_state in starting_state.next_states.items():
                    arr.append((starting_state.name, trigger, allowed_state.name))
                    traversed.append(starting_state)
                    get_all_connections(allowed_state, arr=arr, traversed=traversed)

            return arr

        states = [state.name for state in self.states]
        connections = get_all_connections(self.initial_state)

        return {
            'states': states,
            'connections': connections,
            'current_state': self.current_state.name,
            'starting_state': self.initial_state.name
        }

    @classmethod
    def from_dict(cls, data):
        states = dict([(name, State(name)) for name in data['states']])

        for (from_state_name, trigger, to_state_name) in data['connections']:
            from_state = states[from_state_name]
            to_state = states[to_state_name]
            from_state.add_allowed_transition(trigger, to_state)

        current_state = states[data['current_state']]
        instance = cls(None, current_state, states.values())
        instance.initial_state = states[data['starting_state']]

        return instance
