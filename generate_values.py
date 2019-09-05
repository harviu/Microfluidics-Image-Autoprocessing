import numpy as np
from image_process import hotspots, circle_detection


def calculate(image, ENLARGE=3, SHIFT=15):
    assert image.ndim == 3
    values = []
    chosens = []
    time_steps = image.shape[0]
    # culculate hotspots
    hot = hotspots(image)
    hv, hy, hx, hr = hot
    # print(hot)

    for i in range(time_steps):
        gfp = image[i, :, :]

        # detect circle in every frame to adjust selection
        detected = circle_detection(gfp, 1)
        min_loss = float("inf")
        chosen = None
        for circle_index in range(len(detected)):
            circle = detected[circle_index]
            v, y, x, r = circle
            loss = abs(y - hy) + abs(x - hx) + abs(r - hr) ** 2
            if loss < min_loss:
                min_loss = loss
                chosen = circle
        if min_loss > SHIFT:
            chosen = hot
        chosens.append(chosen[1:])
        h, y, x, r = chosen

        background = int(np.sum(gfp[y - 3:y + 3, x - 3:x + 3]) / 36)
        dots = []
        for row in range(y - (r + ENLARGE), y + (r + ENLARGE) + 1):
            for col in range(x - (r + ENLARGE), x + (r + ENLARGE) + 1):
                if (row - y) ** 2 + (x - col) ** 2 <= (r + ENLARGE) ** 2 and 0 <= row < gfp.shape[0] and 0 <= col < \
                        gfp.shape[1]:
                    dots.append(gfp[row, col])
        val = max(dots)
        val = int(val)
        values.append(val - background)
    return (values, chosens, hv)
