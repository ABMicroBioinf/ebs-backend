class FlattenMixin(object):
    def to_representation(self, obj):
        assert hasattr(
            self.Meta, "flatten"
        ), 'Class {serializer_class} missing "Meta.flatten" attribute'.format(
            serializer_class=self.__class__.__name__
        )
        rep = super(FlattenMixin, self).to_representation(obj)
        for field in self.Meta.flatten:
            objrep = rep.pop(field)
            #print(type(objrep))
            #print(objrep)
            if objrep is None:
                continue
            if isinstance(objrep, dict):
                for key in objrep:
                    rep[field + "__" + key] = objrep[key]
            elif isinstance(objrep, list):
                i = 0
                for item in objrep:
                    for key in item:
                        rep[field + "_" + str(i) + "__" + key] = item[key]
                    i += 1
        return rep
