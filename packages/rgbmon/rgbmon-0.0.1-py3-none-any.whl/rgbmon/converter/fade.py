import math

import core.utils


class Converter:
    def __init__(self, config, backend):
        # TODO: check if colors > 1
        self.backend = backend
        self.leds = backend.get_led_list(config["leds"])
        self.colors = map(lambda c: core.utils.Color.from_string(c), config["colors"])

    def convert(self, value):
        # TODO: rewrite to use utils.Color
        segment_size = 100.0 / (len(self.colors) - 1)
        segment = math.floor(value / segment_size)
        if segment >= segment_size:
            segment = segment_size - 1

        start = self.colors[segment]
        end = self.colors[segment + 1]
        r1,g1,b1 = tuple(int(start[i:i+2], 16) for i in (0, 2, 4))
        r2,g2,b2 = tuple(int(end[i:i+2], 16) for i in (0, 2, 4))


        v = (value - segment_size * segment) / segment_size
        r3 = int((r1 * (1 - v) + r2 * v))
        g3 = int((g1 * (1 - v) + g2 * v))
        b3 = int((b1 * (1 - v) + b2 * v))

        data = {}
        data['r'] = r3
        data['g'] = g3
        data['b'] = b3

        print(data)

        out = []
        for led in self.leds:
            out.append((led, data))
        return out