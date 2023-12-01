from picowork.pscene import *
from picowork.pspriteobject import *
from picowork.pscrollpattern import *
from picowork.pfixedbackground import *
from tilemapgeneration import *
from tilemap import *
from portal import *


class PSceneDungeon(PScene):
    def __init__(self):
        super().__init__()
        background_sky = PFixedBackground('skybox.png')
        self.add_element(background_sky)

        background = PScrollPattern('bg01_far.png', 20)
        background.set_position(Vector2(0, 20))
        self.add_element(background)

        background_near0 = PScrollPattern('bg01_mid.png', 18)
        background_near0.set_position(Vector2(0, 12))
        self.add_element(background_near0)

        background_near1 = PScrollPattern('bg01_mid.png', 13)
        background_near1.set_position(Vector2(0, 11))
        self.add_element(background_near1)

        background_near2 = PScrollPattern('bg01_mid.png', 10)
        background_near2.set_position(Vector2(0, 10))
        self.add_element(background_near2)

        self.tilemap = Tilemap(160, 100, 'terr02_%02d.png', ['fill03.png', 'fill02.png'])
        self.add_element(self.tilemap)

        self.player = Player(self.tilemap)
        self.player.set_position(Vector2(18.5, 50))
        self.add_element(self.player, 2)

        import scenemanagement
        self.portal = Portal(self.player, scenemanagement.load_scene_village)
        self.portal.set_position(Vector2(18.5, 45))
        self.add_element(self.portal)

        camera._position = self.player.get_position()

    def generate_dungeon(self):
        return generate_tilemap(self.tilemap, self.tilemap._w, self.tilemap._h, 13)

    def update(self, delta_time):
        new_campos = camera._position + (self.player.get_position() - camera._position) * delta_time * 8

        magnitude = clamp(-0.5, (new_campos - camera._position).x * 50, 0.5)

        camera._position = new_campos
        camera._rotation = magnitude
        camera._size = 4 # + 4 * (t % 1) ** 0.05

        self.player.update(delta_time)
        self.portal.update(delta_time)