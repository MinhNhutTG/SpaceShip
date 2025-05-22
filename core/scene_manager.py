import pygame

# class SceneManager:
#     def __init__(self, initial_scene):
#         self.scene = initial_scene
#
#     def run(self, screen):
#         clock = pygame.time.Clock()
#         while self.scene and self.scene.is_running:
#
#             events = pygame.event.get()
#             self.scene.handle_events(events,screen)
#             self.scene.update()
#             self.scene.render(screen)
#             pygame.display.flip()
#             clock.tick(60)

class SceneManager:
    def __init__(self, initial_scene):
        self.current_scene = initial_scene
    def change_scene(self, new_scene):
        self.current_scene = new_scene