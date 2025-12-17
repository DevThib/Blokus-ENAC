import possibilites_jeu_version as pjv
import orientation_angles as oa
def clicable(mat,version) :
    liste_dep=pjv.possibilites(mat,version)
    oreilles_version=oa.orientation(version)
    liste_arr=[]
    for k in liste_dep :
        l = liste_dep[k]
        for j in oreilles_version :
            if j[2]==(-k[0],-k[1]) :
                new_x =l[0]-j[0]+k[0]
                new_y =l[1]-j[1]-k[1]
                liste_arr.append((new_x,new_y))
    return liste_arr

    