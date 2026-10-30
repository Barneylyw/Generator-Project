import femm
import math

femm.openfemm()
femm.opendocument(r"C:\Users\User\Desktop\New folder (2)\Crappy Generator 4-1.FEM")
rotate_angle = 15
last_angle = 0
fluxchange = 0
rpm = 352
turnspercoil = 765
pos_volts = 0
neg_volts = 0
delta_t = rotate_angle / (rpm * (1/60) * 360)   # change in time(s) of every rotate angle
print(delta_t)

deltaangle_over_deltatime_d = {}

volt_d = {}
total_volts = 0

positive_coilgroup_d = {}

coils = {
   "1a": (19, -3),
   "1b": (18, 3),
   "2a": (16, 11),
   "2b": (11, 12),
   "3a": (5.3, 16.5),
   "3b": (0,16),
   "4a": (-5.7, 15.1),
   "4b": (-11, 13),
   "5a": (-15, 8),
   "5b": (-17.5, 3),
   "6a": (-17.6, -3.2),
   "6b": (-16.5, -9),
   "7a": (-10.6, -12.6),
   "7b": (-7, -18),
   "8a": (0,-17),
   "8b": (5, -16),
   "9a": (14.6, -16.4),
   "9b": (14.6, -9),
}

fluxd = {
   
}

fluxchanged = {

}

def printdict (fluxd, angle, coils):
   print(angle)
   print(coils)


# finding how much flux each coil will experience at a certain angle
for angle in range(0, 360, rotate_angle):
    femm.mi_selectgroup(1)
    femm.mi_moverotate(0, 0, rotate_angle)
    femm.mi_analyze()
    femm.mi_loadsolution()
    fluxd[f"Angle: {angle}"] = {}
    for i in range (1 ,10):
 # select the coil region before integrating
      femm.mo_selectblock(*coils[f"{i}a"])
      femm.mo_selectblock(*coils[f"{i}b"])
      area = femm.mo_blockintegral(5)  ##coil area...?
      Bx = femm.mo_blockintegral(8)
      By = femm.mo_blockintegral(9)
      flux_x = Bx/(1*10**-3)
      flux_y = By/(1*10**-3)
      flux = math.sqrt(flux_x**2 +flux_y**2)
      ##idk = femm.mo_getcircuitproperties("Coil Circuit")
      print(f"Angle {angle}° -> Coil {i}: Flux = {flux:.10e} Wb (T m^2)","Bx:", Bx, "Wb By", By, "Wb") 
      fluxd[f"Angle: {angle}"][f"Coil {i}:" ] = f"Flux = {flux:.5e}"
      #print(area)
      #time.sleep(5)
      femm.mo_clearblock()  # clear selection so next loop works
    print()
    #print(fluxd)
    #print(Bx, By, area)
    femm.mo_clearblock()  # clear selection so next loop works
    femm.mo_close()


##computing difference in flux
for i in range(1,10): 
   print(f"Coil group {i}")
   fluxchanged[f"Coil group {i}"] = {}
   deltaangle_over_deltatime_d[f"Coil group {i}"] = {}
   volt_d[f"Coil group {i}"] = {}
   for angle in range(0, 360, rotate_angle):      ##print coil group's flux at angle 1, angle 2...
      ##print(f"Angle: {angle}", fluxd[f"Angle: {angle}"][f"Coil {i}:" ], "Wb")
      if angle != 0:    #finding change in flux
         last_angle = (angle - rotate_angle) % 360
         print(f"current angle: {angle} last angle: {last_angle}")
         #figuring out the change in flux
         fluxchange = float(fluxd[f"Angle: {angle}"][f"Coil {i}:" ].replace("Flux = ", "")) - float(fluxd[f"Angle: {last_angle}"][f"Coil {i}:" ].replace("Flux = ", ""))      #finding the change in flux between this angle and the last one
         fluxchange = f"{fluxchange:.3e}"
         #storing it in a dictionary
         fluxchanged [f"Coil group {i}"][f"ΔΦ between {angle} and {last_angle}:"] = fluxchange     ##storing it in a dictationary
         #print
         print(f"Angle: {angle}", fluxd[f"Angle: {angle}"][f"Coil {i}:" ], "Wb. ΔΦ between", angle ,"and", last_angle ,":", fluxchange)
         #figure out what ΔΦ/Δt between current angle and last angle is
         deltaangle_over_deltatime = float(fluxchange)/delta_t
         deltaangle_over_deltatime = float(f"{deltaangle_over_deltatime:.5}")
         print(f"Coilgroup {i}: ΔΦ/Δt between {angle} and {last_angle} is: {deltaangle_over_deltatime}")
         #storing it in a dictionary
         deltaangle_over_deltatime_d[f"Coil group {i}"][f"ΔΦ/Δt between {angle} and {last_angle}"] = deltaangle_over_deltatime
         #finding volts for each coil
         volt = deltaangle_over_deltatime * -turnspercoil
         volt_d[f"Coil group {i}"][f"Voltage between {angle} and {last_angle}"] = volt
         print(f"volts generated: {volt}V")
         print()
         
   print("---------------------------")

print(angle, last_angle)
last_angle = 0

for angle in range(0, 360, rotate_angle):
   last_angle = (angle - rotate_angle) % 360
   print(angle, last_angle)
   if angle != 0:
      for i in range(1,10): 
         print(f"Coil group {i}")
         total_volts += volt_d[f"Coil group {i}"][f"Voltage between {angle} and {last_angle}"]
         print(volt_d[f"Coil group {i}"][f"Voltage between {angle} and {last_angle}"])
         if (volt_d[f"Coil group {i}"][f"Voltage between {angle} and {last_angle}"]) > 0:
            positive_coilgroup_d[f"Coil group {i}"] = "Positive"
            
         if volt_d[f"Coil group {i}"][f"Voltage between {angle} and {last_angle}"] > 0:
            pos_volts += volt_d[f"Coil group {i}"][f"Voltage between {angle} and {last_angle}"]
         if volt_d[f"Coil group {i}"][f"Voltage between {angle} and {last_angle}"] < 0:
            neg_volts += volt_d[f"Coil group {i}"][f"Voltage between {angle} and {last_angle}"]
      print(f"positive voltages generated by positive coil groups between {angle} and {last_angle} is {pos_volts}")
      print(f"negative voltages generated by negative coil groups between {angle} and {last_angle} is {neg_volts}")
      neg_volts = 0
      pos_volts = 0
   print("positive coil groups:")
   print(positive_coilgroup_d)
   positive_coilgroup_d = {}
   print()

   #positive groups:
   #(group 1 through 5) & (1 + 7 through 9) & (4 through 7), when one of these group of coil groups are positive, the other groups
