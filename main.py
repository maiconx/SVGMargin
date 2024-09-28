import tkinter as tk
import tkinter.filedialog as fd

root = tk.Tk()
filez = fd.askopenfilenames(parent=root, title='Choose a file')

for i in filez:
    fin = open(i , "rt")
    data = fin.read()
    original_list = data
    char1 = 'viewBox="'
    char2 = '">'
    mystr = data
    viewBox = mystr[mystr.find(char1)+9 : mystr.find(char2)]
    vList = viewBox.split()
    vList_final = vList
    print(vList_final[0])
    if vList_final[0] == '0':
        vList_final[0] = str(float(vList_final[0])-0.5)
        vList_final[1] = str(float(vList_final[1])-0.5)
        vList_final[2] = str(float(vList_final[2])+1.0)
        vList_final[3] = str(float(vList_final[3])+1.0)

    vFinal = ' '.join(vList_final)
    print(vFinal)
    data = data.replace(viewBox, vFinal)

    fin.close()
    fin = open(i , "wt")
    fin.write(data)
    fin.close()
