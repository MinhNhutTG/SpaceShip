
class Scene:
    def __init__(self,manager):
        self.is_running = True
        self.manager = manager

    def handle_events(self, events,screen):
        pass

    def update(self,screen):
        pass

    def render(self, screen):
        pass