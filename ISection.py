from openseespy.opensees import *

def ISection(secTag, matTag, d, tw, bf, tf, numSubdivWebL, numSubdivFlangeT):
    
    numSubdivWebT = 1
    numSubdivFlangeL = 1
    
    y1 = -d/2
    y2 = y1 + tf
    y4 = d/2
    y3 = y4 - tf
    z1 = -bf/2
    z2 = -tw/2
    z3 = tw/2
    z4 = bf/2
    
    section('Fiber', secTag)
    patch('quad', matTag, numSubdivFlangeL, numSubdivFlangeT, y1, z4, y1, z1, y2, z1, y2, z4)
    patch('quad', matTag, numSubdivFlangeL, numSubdivFlangeT, y3, z4, y3, z1, y4, z1, y4, z4)
    patch('quad', matTag, numSubdivWebT, numSubdivWebL, y2, z3, y2, z2, y3, z2, y3, z3)
    