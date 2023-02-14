import ezdxf

def csvtodxf():
    csv_list=['_SOP_report_sorted.csv']
    drawing = ezdxf.new(dxfversion='R2010')
    drawing.layers.new('ZZ-Non_Plot', dxfattribs={'color': 1})

    def creatData(SOP, new_item):  # create geometry
        modelspace = drawing.modelspace()
        modelspace.add_circle((SOP), (0.1), dxfattribs={'layer': 'MH'})
        modelspace.add_mtext(new_item,
                             dxfattribs={
                                 'layer': 'ZZ-Non_Plot',
                                 'char_height': 0.08,
                                 'insert': (SOP)
                             })
        return

    # schedule report data
    for item in csv_list:
        csv_file = open(item, 'r')
        csv_file = csv_file.read().split('\n')
        #csv_file.pop(0)
        for data in csv_file:
          if data:
            try:
                #print(data)
                #text= lineData.replace(',','\P')
                x = float(data.split(',')[1])
                y = float(data.split(',')[2])
                z = float(data.split(',')[3])
                #name='Loc Suite No.'+data.split(',')[0]+'\P'
                sopNo='SOP No.'+data.split(',')[0]+'\P'
                CH='CH '+data.split(',')[4]+'\P'
                #eCH='End CH'+data.split(',')[2]+'\P'
                print(x,y,z,CH,sopNo)
           # input()
            #try:
                SOP = x,y,z
                #print(SOP)
                new_item = sopNo+CH+str(x)+'\P'+str(y)+'\P'+str(z)
                #print(newMH)
                creatData(SOP, new_item)
            except:
                pass

    # save file
    drawing.saveas('Report_QA.dxf')




