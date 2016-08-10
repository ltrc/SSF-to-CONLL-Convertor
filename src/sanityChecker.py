#!/usr/bin/env python -*- coding: utf-8 -*-

__Author__ = "Riyaz Ahmad Bhat"
__Email__  = "riyaz.ah.bhat@gmail.com"

class SanityChecker (object) :

    def ifCycle_ (self, node_): 
        parent_ = self.modifierModified[node_]
        if parent_ == None:
            return
        else:
            self.ifCycle_(parent_)

    def treeSanity(self):
        if (self.nodeList) < 2:
            return "#single chunk sentence"
        else:
            if self.modifierModified.values().count(None) == 0:
                return "#Root-less tree"
            elif self.modifierModified.values().count(None) > 1 or len(\
                    [None for i in self.nodeList if i.depRel == None]) > 1:
                return "#Forest, mulitple roots"
            elif len(set(self.modifierModified.values()) - set(self.modifierModified.keys())) > 1:
                difference = set(self.modifierModified.values()) - set(self.modifierModified.keys())
                difference.remove(None)
                return "#Unknown head(s) as %s" % ("\t".join(difference))
            else:# cycle
                for node_ in self.modifierModified.keys():
                    try:
                        self.ifCycle_(node_)
                    except Exception,e:
                        return "#cycle in %s\t%s" % (node_, self.modifierModified[node_])
