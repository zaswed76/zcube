from kivy.uix.recycleview import RecycleView


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        print("AAAAAAAAAAAAAAAAAAAAAAA")
        self.data = [{'text': str(x)} for x in range(100)]