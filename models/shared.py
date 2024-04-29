class TableRepr:
    def __repr__(self):
        attrs = [f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith("_")]
        line = f'<{self.__class__.__name__} {", ".join(attrs)}>'
        return line
