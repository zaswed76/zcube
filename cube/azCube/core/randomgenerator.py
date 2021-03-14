
import random

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import BaseListItem
from kivymd.uix.textfield import MDTextField




class RandomGenerator:
    def __init__(self):
        pass

    def not_repeat(self, start, end, count):
        lst = list()
        r = count//(end-start)
        m = count%(end-start)

        for i in range(0, r):
            lst.extend(random.sample(range(start, end), end-start))

        if m:
            # print(start,end,m)
            lst.extend(random.sample(range(start, end), m))
        return [str(x) for x in lst]

    def g2(self, start, end, count):
        r = [random.randint(0, 20) for _ in range(20)]
        random.shuffle(r)
        return r

    def format(self, seq, sep="."):
        return sep.join(seq)


if __name__ == '__main__':
    g = RandomGenerator()
    r = g.not_repeat(0, 3, 11)
    print("".join(r))
    print(len(r))
    res = "0.9.7.3.6.7.8.3.9.0"