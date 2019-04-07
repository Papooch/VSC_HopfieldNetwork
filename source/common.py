
def clamp(minv, maxv, value):
    return min(max(minv, value), maxv)

def rollover(minv, maxv, value):
    return minv + (value-minv)%(maxv-minv+1)