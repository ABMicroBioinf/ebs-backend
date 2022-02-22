import json
class FlattenMixin(object):
    def to_representation(self, obj):
        assert hasattr(
            self.Meta, "flatten"
        ), 'Class {serializer_class} missing "Meta.flatten" attribute'.format(
            serializer_class=self.__class__.__name__
        )
        rep = super(FlattenMixin, self).to_representation(obj)
        #print(rep)
        for field in self.Meta.flatten:
            #print(field)
            objrep = rep.pop(field)
            # print("objrep ******************************************************")
            # print(type(objrep))
            # print(objrep)
            
            if objrep is None:
                continue
            if field in ['RawStats', 'QcStats', 'profile']:
                objrep = json.loads(objrep)
            
            if isinstance(objrep, dict):
                for key in objrep:
                    rep[field + "__" + key] = objrep[key]
                    
            elif isinstance(objrep, list):
                rep[field] = objrep
                #i = 0
                #for item in objrep:
                #    for key in item:
                #        rep[field  + "__" + key + "_" + str(i)] = item[key]
                #    i += 1
            else:
                print("")
                #print(field, rep)
        return rep
