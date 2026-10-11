family = sys.argv[1]

base_path = 'results/significance/'
bib_path = os.path.join(base_path ,'bible/')
gam_path = os.path.join(base_path ,'game/')
gam_bal_path = os.path.join(gam_path ,'balanced/')
gam_unb_path = os.path.join(gam_path ,'unbalanced/')

bib = os.path.join()
gam_b = os.path.join()
gam_u = os.path.join()

# TODO: fixa ovanstående pythonskräp till paths som gör att GIVET en familj, alla p-värden hämtas från korrekt fil.