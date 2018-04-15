"""Функции всякого порядка.
    В питоне арность (местность, количество аргументов) функции произвольна
    и даже не ограничена: такие функции, как print(), принимают столько
    аргументов, сколько им дадут. Поэтому карринг в его первозданном виде
    - затруднён, а то и невозможен: когда остановиться?

    Данный модуль позволяет  разложить arity-местной функции на цепочку
    одноместных и свернуть цепочки одноместных функций в arity-местную.
"""

class ReadOnlyState:
    """Состояние, которое, по нашему соглашению, мы после инициализации не
    изменяем. Это позволяет сначала передать часть аргументов, а потом
    работать с ReadOnlyState, не боясь, что в будущем оно изменится.
    """

    def __init__(self, fun, arity, *args):
        assert arity >= 0, "atiry should be >= 0"
        self.arity = arity
        self.args = [] + list(args)
        self.fun = fun

    def get_next(self, *input_args):
        """Метод позволяет получить следующий ReadOnlyState в случае, если
        количество переданных аргументов меньше арности. Это позволяет
        сначала передать часть аргументов, а потом работать с полученым
        ReadOnlyState независимо.

        Результатом данной функции является или ReadOnlyState или результат.
        """
        args = self.args[:]
        arity = self.arity
        fun = self.fun

        if input_args:
            args += list(input_args)

        if len(args) < arity:
            return ReadOnlyState(fun, arity, *args).get_next

        assert arity == len(args), "incorrect number of args"
        return fun(*args)


def curry_explicit(fun, arity):
    """Разложение arity-местной функции на цепочку одноместных."""
    return ReadOnlyState(fun, arity).get_next


def uncurry_explicit(fun, arity):
    """Свертка цепочки одноместных функций в arity-местную."""
    return ReadOnlyState(fun, arity).get_next
