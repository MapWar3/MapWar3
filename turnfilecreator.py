#this provides a framework for creating turnfiles

#UNTESTED FOR SYNTAX ERRORS
import cPickle

class Turn: #THIS MAY GET MIXED UP WITH THE Turn VARIABLE IN ORDER.PY CHANGE THE NAME OF THE ITERATOR VARIABLE.
    def __init__(self,nationname='', conquered = [], struct = {}):
        self.nationname = nationname
        self.conquered = conquered #list of zone id's or something
        self.struct = struct #dictionary for constructed structures {zone_id,(structure_type,level)}

def createturn(name='',conquered = [], struct={}):
    T = Turn(name,conquered,struct)
    with open(T.name, 'wb') as file:
        cPickle.dump(T,file)