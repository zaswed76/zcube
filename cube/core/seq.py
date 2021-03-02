
import random
class Seq:
    def __init__(self):
        self._data = list()

    def set_data(self, start, end):
        self._data = list(range(start, end))

    def set_data_on_seq(self, seq):
        # print(seq, "-----------------")
        self._data.clear()
        for t in seq:
            start = int(t + "0")
            end = start + 10
            seq = range(start, end)
            self._data.extend(seq)
        self._data.sort()




    @property
    def data(self):
        return self._data

    def shuffle(self):
        random.shuffle(self._data)

    def sort(self):
        self._data.sort()
if __name__ == '__main__':
    s = Seq()
    s.set_data_on_seq(['0'])
    print(s.data)
