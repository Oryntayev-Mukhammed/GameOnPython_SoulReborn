class GameStateMachine:
    def __init__(self, states, initial_state):
        self.states = states
        self.current_state = initial_state

    def change_state(self, new_state):
        self.current_state = self.states[new_state]

    def update(self, game_state_machine):
        self.current_state.update(game_state_machine)

    def handle_event(self, event, game_state_machine):
        self.current_state.handle_event(event, game_state_machine)

    def edit(self):
        self.current_state.edit()


