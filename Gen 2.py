import femm
import math
femm.openfemm()
femm.opendocument(r"C:\Users\User\Desktop\New folder (2)\Crappy Generator 2.FEM")
rotate_angle = 5

# now the FEMM GUI will stay open — you can see it live
for angle in range(0, 360, rotate_angle):
    femm.mi_selectgroup(1)
    femm.mi_moverotate(0, 0, rotate_angle)
    femm.mi_analyze()
    femm.mi_loadsolution()

 # select the coil region before integrating
    femm.mo_selectblock(6, 0)
    area = femm.mo_blockintegral(5)  ##coil area...?
    Bx = femm.mo_blockintegral(8)
    By = femm.mo_blockintegral(9)
    flux_x = Bx/(1*10**-3)
    flux_y = By/(1*10**-3)
    flux = math.sqrt(flux_x**2 +flux_y**2)
    ##idk = femm.mo_getcircuitproperties("Coil Circuit")
    print(f"Angle {angle}° -> Flux = {flux:.10e} Wb","Bx:", flux_x, "Wb By", flux_y, "Wb") 
    #print(Bx, By, area)
    femm.mo_clearblock()  # clear selection so next loop works
    femm.mo_close()