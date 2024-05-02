class TableRepr:
    def __repr__(self):
        attrs = [f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith("_")]
        line = f'<{self.__class__.__name__} {", ".join(attrs)}>'
        return line


# class TableCast:
#     def get_dict(self):
#         result = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

#         for relationship in self.__mapper__.relationships:
#             related_obj = getattr(self, relationship.key)
#             if isinstance(related_obj, list):
#                 result[relationship.key] = [item.get_dict() for item in related_obj]
#             else:
#                 result[relationship.key] = related_obj.get_dict()

#         return result
