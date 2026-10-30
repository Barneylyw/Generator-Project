import femm
import math
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


femm.openfemm()
femm.opendocument(r"C:\Users\User\Desktop\New folder (2)\Crappy Generator 5 - 3.FEM")
rotate_angle = 1
last_angle = 0
fluxchange = 0
rpm = 352
turnspercoil = 2418
pos_volts = 0
neg_volts = 0
delta_t = rotate_angle / (rpm * (1/60) * 360)   # change in time(s) of every rotate angle
print(delta_t)

deltaangle_over_deltatime_d = {}

volt_d = {}
total_volts = 0

positive_coilgroup_d = {}

coils = {
   "1a": (64, -4),
   "1b": (64, 4),
   "2a": (64, 18),
   "2b": (58, 27),
   "3a": (57, 38),
   "3b": (51, 51),
   "4a": (39, 56),
   "4b": (25, 58),
   "5a": (18, 65),
   "5b": (4, 70),
   "6a": (-6, 70),
   "6b": (-20, 73),
   "7a": (-29, 63),
   "7b": (-42, 60),
   "8a": (-50, 50),
   "8b": (-60, 43),
   "9a": (-70, 30),
   "9b": (-72, 20),
   "10a": (-77, 6),
   "10b": (-77, -6),
   "11a": (-63, -15),
   "11b": (-65, -31),
   "12a": (-55, 38),
   "12b": (-52, -52),
   "13a": (-38, -56),
   "13b": (-31, -68),
   "14a": (-18.5, -69),
   "14b": (-7, -74),
   "15a": (7, -70),
   "15b": (18, -71),
   "16a": (29, -62),
   "16b": (42, -62),
   "17a": (50, -50),
   "17b": (57, -40),
   "18a": (64, -29),
   "18b": (70, -20),
}

fluxd = {
}

fluxchanged = {
}

def printdict (fluxd, angle, coils):
   print(angle)
   print(coils)


# finding how much flux each coil will experience at a certain angle
femm.main_minimize()

for angle in range(0, 360, rotate_angle):
    ##femm.openfemm()
    femm.mi_selectgroup(1)
    femm.mi_moverotate(0, 0, rotate_angle)
    femm.mi_analyze()
    femm.mi_loadsolution()
    fluxd[f"Angle: {angle}"] = {}
    for i in range (1 ,19):
 # select the coil region before integrating
      femm.mo_selectblock(*coils[f"{i}a"])
      femm.mo_selectblock(*coils[f"{i}b"])
      area = femm.mo_blockintegral(5)  ##coil area...?
      Bx = femm.mo_blockintegral(8)
      By = femm.mo_blockintegral(9)
      flux_x = Bx/(1*10**-3)
      flux_y = By/(1*10**-3)
      flux = math.sqrt(flux_x**2 +flux_y**2)    ##calcuate total flux
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
for i in range(1,19): 
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

##finding all positive voltages and adding them up
for angle in range(0, 360, rotate_angle):
   last_angle = (angle - rotate_angle) % 360
   print(angle, last_angle)
   if angle != 0:
      for i in range(1,19): 
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



wb = Workbook()
ws = wb.active
ws.title = "Voltage Data"

# Layout: pairs of coil groups side by side, each pair = 3 cols + 1 spacer
# Columns per group: Group# | Angle | Voltage  — then a blank col, then next group
# We'll put groups 1-9 on the left half and 10-18 on the right half
# Actually, lay out all 18 groups as columns sets across the sheet.

header_fill = PatternFill("solid", start_color="1F4E79", end_color="1F4E79")
header_font = Font(name="Arial", bold=True, color="FFFFFF", size=10)
data_font   = Font(name="Arial", size=10)
center      = Alignment(horizontal="center", vertical="center")
thin        = Side(style="thin", color="BFBFBF")
border      = Border(left=thin, right=thin, top=thin, bottom=thin)

COLS_PER_GROUP = 3   # Group# | Angle | Voltage
SPACER         = 1
STRIDE         = COLS_PER_GROUP + SPACER  # 4 columns per group block

def col_start(group_index):   # group_index = 0-based
    return group_index * STRIDE + 1

# Write headers for all 18 groups
for g in range(18):
    c = col_start(g)
    headers = [f"Group {g+1}", "Angle (°)", "Voltage (V)"]
    for offset, h in enumerate(headers):
        cell = ws.cell(row=1, column=c + offset, value=h)
        cell.fill   = header_fill
        cell.font   = header_font
        cell.alignment = center
        cell.border = border
    ws.column_dimensions[get_column_letter(c)].width     = 10
    ws.column_dimensions[get_column_letter(c+1)].width   = 10
    ws.column_dimensions[get_column_letter(c+2)].width   = 14
    ws.column_dimensions[get_column_letter(c+3)].width   = 2   # spacer

ws.row_dimensions[1].height = 18

# Fill data — mirrors the nested loop order in the original code
row_tracker = {}   # group_number -> current excel row

for g in range(1, 19):
    row_tracker[g] = 2   # data starts at row 2

for angle in range(0, 360, rotate_angle):
    last_angle_export = (angle - rotate_angle) % 360
    if angle != 0:
        for i in range(1, 19):
            voltage = volt_d[f"Coil group {i}"][f"Voltage between {angle} and {last_angle_export}"]
            r = row_tracker[i]
            c = col_start(i - 1)
            ws.cell(row=r, column=c,   value=i).border       = border
            ws.cell(row=r, column=c,   value=i).font         = data_font
            ws.cell(row=r, column=c,   value=i).alignment    = center
            ws.cell(row=r, column=c+1, value=angle).border   = border
            ws.cell(row=r, column=c+1, value=angle).font     = data_font
            ws.cell(row=r, column=c+1, value=angle).alignment= center
            ws.cell(row=r, column=c+2, value=round(voltage, 4)).border    = border
            ws.cell(row=r, column=c+2, value=round(voltage, 4)).font      = data_font
            ws.cell(row=r, column=c+2, value=round(voltage, 4)).alignment = center
            row_tracker[i] += 1

output_path = r"C:\Users\User\Desktop\New folder (2)\voltage_output_rotate angle 1 generator 5-3 r-59mm.xlsx"
wb.save(output_path)
print(f"\nExcel saved to: {output_path}")