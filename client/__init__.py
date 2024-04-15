import st3m.run, random, math
import urequests

from st3m.application import Application, ApplicationContext
from st3m.input import InputState
from ctx import Context

import os

# 1 speakerbar onoff
# 2 speakerbar up/down (based on position)
# 3 speakerbar input cycle

# 4 projector on/off
# 5 projector input cycle
# 6

# 7 everything off macro
# 8 game mode macro (maybe lights in future)

# 9 fan speed
# 10: fan on/off

URL_BASE = ""

commands = {
    1: { "url": "speakerbar/onff", "name": "Speaker On/Off" },
    1: { "url": "speakerbar/onff", "name": "Speaker On/Off" },
}

class Remote(Application):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        self.command = ""

    def think(self, ins: InputState, delta_ms: int) -> None:
        pass

    def draw(self, ctx: Context) -> None:
        tile_dim = self.tile_dim
        ctx.image_smoothing = False
        ctx.rectangle(-120, -120, 240, 240).rgb(0, 0.34, 0.72).fill()
        if self.scale > 1.0:
            z = 0
            scale = self.scale
        else:
            logscale = math.log(self.scale, 0.5)
            z = math.floor(logscale)
            scale = 2 ** (-(logscale - z))
        # we can not rely on transforms, the happy path for ctx.image is
        # working without any scale factor - sorry

        u = self.x / (2 ** (z)) / 64
        v = self.y / (2 ** (z)) / 64

        u_int = math.floor(u)
        v_int = math.floor(v)

        u_fraction = u - u_int
        v_fraction = v - v_int

        scale *= 2.3
        tiles_folder = "/sd/map/"

        for col in range(self._tc):
            for row in range(self._tc):
                if (u_int + col - self._tch) >= 0 and (v_int + row - self._tch) >= 0:
                    tile_path_fragment = (
                        str(u_int + col - self._tch)
                        + "/"
                        + str(v_int + row - self._tch)
                        + "/"
                        + str(z)
                        + ".png"
                    )
                    tile_path = tiles_folder + tile_path_fragment
                    try:
                        os.stat(tile_path)
                    except OSError:
                        response = urequests.get("http://pippin.gimp.org/tmp/flow3r-map/" + tile_path_fragment)

                        try:
                            os.mkdir(tiles_folder)
                        except OSError:
                            True
                        try:
                            os.mkdir(tiles_folder + str(u_int + col - self._tch))
                        except OSError:
                            True
                        try:
                            os.mkdir(
                                tiles_folder
                                + str(u_int + col - self._tch)
                                + "/"
                                + str(v_int + row - self._tch)
                            )
                        except OSError:
                            True
                        print(
                            tiles_folder
                            + str(u_int + col - self._tch)
                            + "/"
                            + str(v_int + row - self._tch)
                        )
                        print(tile_path)
                        f = open(tile_path, "w")
                        f.write(response.content)
                        f.close()

                    ctx.image(
                        tile_path,
                        ((col - self._tch - u_fraction) * tile_dim) * scale,
                        ((row - self._tch - v_fraction) * tile_dim) * scale,
                        tile_dim * scale + 1,
                        tile_dim * scale + 1,
                    )


if __name__ == "__main__":
    st3m.run.run_view(Map(ApplicationContext()))
