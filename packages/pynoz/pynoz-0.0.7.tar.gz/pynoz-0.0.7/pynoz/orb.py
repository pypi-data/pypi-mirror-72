def get_via_pl_from_root(root,pl):
    orb = root
    for i in range(0,len(pl)):
        an = pl[i]
        if(hasattr(root,an)):
            orb = getattr(orb,an)
        else:
            return(undefined)
    return(orb) 


def set_via_pl_from_root(root,pl,creat_leaf):
    orb = root
    lngth = len(pl)
    for i in range(0,lngth):
        an = pl[i]
        if(hasattr(orb,an)):
            orb = getattr(orb,an)
        else:
            norb = Orb()
            if(i == (lngth - 1)):
                leaf = creat_leaf(pl)
                setattr(orb,an,leaf)
            else:
                setattr(orb,an,norb)
            orb = norb
    return(orb)


def is_leaf(orb):
    lngth = org.__dict__.__len__()
    return(lngth == 0)


def get_children(orb):
    ks = orb.__dict__.keys()
    children = []
    for i in range(len(ks)):
        an = ks[i]
        child = getattr(orb,an)
        children = children +[child]
    return(children)

class Orb():
    pass    

