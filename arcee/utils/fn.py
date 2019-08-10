__all__ = ['Filter', 'Map', 'ToTuple', 'Any', 'JoinString', 'All', 'FlatMap', 'ToSet']


class Filter:
    def __init__(self, fn):
        self.fn = fn

    def __ror__(self, other):
        return filter(self.fn, other)


class Map:
    def __init__(self, fn):
        self.fn = fn

    def __ror__(self, other):
        return map(self.fn, other)


class JoinString:
    def __init__(self, string):
        self.string = string

    def __ror__(self, other):
        return self.string.join(other)


class All:
    def __init__(self, fn):
        self.fn = fn

    def __ror__(self, other):
        return all(map(self.fn, other))


class Any:
    def __init__(self, fn):
        self.fn = fn

    def __ror__(self, other):
        return any(map(self.fn, other))


class __ToTuple:
    def __ror__(self, other):
        return tuple(other)


class __ToSet:
    def __ror__(self, other):
        return set(other)


class FlatMap:
    def __init__(self, fn):
        self.fn = fn

    def __ror__(self, other):
        result = []
        for i in other:
            list_j = []
            for j in i:
                list_j.append(self.fn(j))
            result += list_j
        return result


ToTuple = __ToTuple()
ToSet = __ToSet()