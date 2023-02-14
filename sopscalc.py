from shapely.geometry import Point, LineString, MultiPoint
from shapely.ops import nearest_points
import numpy as np
from OSGridConverter import grid2latlong
#import csv2dxf
import csv

def sortListFile():
  listcoords=[]
  fileOut = open('shape_coords.txt', 'w')
  
  file = open('List.csv', 'r')
  file = file.read().split('\n')
  file.pop(0)
  for line in file:
    line=line.replace('"','')
    line=line.replace('m',',')
    line=line.replace(',, ',',')
    line=line.split(',')
    #print(line)
    try:
      out=line[1]+','+line[2]+','+line[3]+'\n'
      print (out)
      listcoords.append(out)
      #fileOut.write(out)
      
    except:
      pass
  print (len(listcoords))
  listcoords = list(dict.fromkeys(listcoords))
  print (len(listcoords))

  for out in listcoords:
    fileOut.write(out)
  #input()


def run():
    def max_min_med(data):
        if data:
            data = np.array(data)
            min = int(np.amin(data))
            max = int(np.amax(data))
            mean = int(np.mean(data))
            return min, mean, max

    def read_file(filename, count, out_file):
        #global out_file, count
        file = open(filename, 'r')
        file = file.read().split('\n')
        print (len(file))
        #input()
        count = count + 1
        xp = []
        yp = []
        ch_buf = []
        sop_buf = []
        for data in file:
                #print (data)
                coord = data.split(',')
                if data:
                    x = float(coord[0])
                    y = float(coord[1])
                    z = float(coord[2])
                    sop = x, y, z
                    xp.append(x)
                    yp.append(y)
                    point = x, y
                    ch, offset, os_grid, wgs_grid = main_CH(point)
                    print(data, ch, offset)
                    #ch_buf.append(float(ch.split(':')[1]))
                    ch_buf.append(float(ch))
                    sop_buf.append(str(sop) + ',' + ch)
        if ch_buf:
                #min, mean, max = max_min_med(ch_buf)
                #print(min, mean, max)
                sop_no = 1
                for coord in sop_buf:
                    coord = coord.replace('(',
                                          '').replace(')',
                                                      '').replace(' ', '')
                    out = str(count) + ',' + str('NA') + ',' + str(
                        'NA') + ',' + str('NA') + ',' + str(
                            sop_no) + ',' + coord + ','
                    out=out+str(os_grid[0])+','+str(os_grid[1])+','+str(wgs_grid[0])+','+str(wgs_grid[1])+','
                    #out = out + '=HYPERLINK("https://maps.google.com/maps?z=12&t=h&q=loc:' + str(
                    #    wgs_grid[0]) + '+' + str(wgs_grid[1]) + '")\n'
                    out = out + 'https://maps.google.com/maps?z=12&t=h&q=loc:' + str(
                        wgs_grid[0]) + '+' + str(wgs_grid[1]) + '\n'
                    out_file.write(out)
                    sop_no = sop_no + 1    
            

    def main_CH(point):
        def getdata(point, line, destinations):
            offset = (open('CH_Offset.txt', 'r'))
            offset = offset.read()
            # print(offset)
            p1 = Point(point)
            CH = line.project(p1)

            # gets distance to axis
            p2 = (line.interpolate(CH))
            #print('Snake Grid point to CH Proj:',p2.coords[0])
            dist_line = LineString([p1, p2])
            dist_line = round(dist_line.length, 3)
            #print('Point Offset to CH:',dist_line)
            #############################

            # nearest point
            nearest_geoms = nearest_points(p2, destinations)
            near_idx0 = (nearest_geoms[1]).coords[0]
            #print('Snake Grid Axis Nearstpoint:',near_idx0)

            #CH = 'A:' + str(round(CH + int(offset)))
            CH = str(round(CH + int(offset)))
            print('Chainage: ' + str(CH))

            return CH, dist_line, p2, near_idx0

        def getAxisCoords(axis_file_name):
            coords = []
            with open(axis_file_name, "r") as file:
                for line in file:
                    line = line.replace('\n', '')
                    x = float(line.split(',')[0])
                    y = float(line.split(',')[1])
                    xy = (x, y)
                    coords.append(xy)
            return coords

        coords = getAxisCoords(axis_file_name="CH_Axis_12700.txt")
        line = LineString(coords)
        #print('Snake Grid Axis Length: ',line.length)
        destinations = MultiPoint(coords)

        chainage, dist, p2, near_point = getdata(point, line, destinations)
        id = coords.index(near_point)

        coords_os = getAxisCoords(axis_file_name="CH_Axis_12700_OS.txt")
        coords_wgs = getAxisCoords(axis_file_name="CH_Axis_12700_WGS84.txt")
        #print(coords[id])
        #print(coords_os[id])
        #print(coords_wgs[id])
        snake_point = point
        snake_ch_point = coords[id]
        os_ch_point = coords_os[id]
        wgs_ch_point = coords_wgs[id]
        ####### OS conversion
        ## snake ch grid point -------- os ch grid point
        ## snake grid point    -------- X (os grid equivalent)
        posx = (snake_point[0] * os_ch_point[0]) / snake_ch_point[0]
        posy = (snake_point[1] * os_ch_point[1]) / snake_ch_point[1]
        os_grid = posx, posy
        print('OS      :', os_grid)
        ####### wgs conversion
        #pwgsx=(snake_point[0]*(wgs_ch_point[0]*10000))/snake_ch_point[0]
        #pwgsy=(snake_point[1]*(wgs_ch_point[1]*10000))/snake_ch_point[1]
        #wgs_grid=pwgsx/10000,pwgsy/10000
        if posx >= 400000:
            zone = 'SE'
        else:
            if posy >= 400000:
                zone = 'SD'
            else:
                zone = 'SJ'
        posx = str(int(posx))[1:]
        posy = str(int(posy))[1:]
        conv = zone + ' ' + posx + ' ' + posy
        #print (conv)
        wgs_grid = str(grid2latlong(conv))
        print(wgs_grid)
        wgs_grid = wgs_grid.split(':')
        #wgs_grid=wgs_grid[0],wgs_grid[1]
        #print(wgs_grid)
        print('WGS84   :', zone, wgs_grid[0], zone, wgs_grid[1])
        #input()

        return chainage, dist, os_grid, wgs_grid

    count = 0
    out_file_name = '_SOP_report_.csv'
    out_file = open(out_file_name, 'w')
    out_file.write(
        'LOC Suite No.,Start CH,End CH,Average CH,SOP no.,SOP X,SOP Y,SOP Z,Chainage,Google Maps\n'
    )

    ##start
    filename = 'shape_coords.txt'
    read_file(filename, count, out_file)
    out_file.close()


def sortEndFile():
  #file = open('_SOP_report_.csv', 'r')
  #file = file.read().split('\n')
  #heading=file[0]
  #file.pop(0)
  file = open('_SOP_report_sorted.csv', 'w')
  reader = csv.reader(open("_SOP_report_.csv"), delimiter=",")
  sortedlist = sorted(reader, key=lambda row: row[8], reverse=False)
  #import operator
  #sortedlist = sorted(reader, key=operator.itemgetter(9), reverse=True)
  #print (sortedlist)
  #sortedlist=reader
  #sortedlist.pop(0)
  count=1
  #input()
  for line in sortedlist:
    
    #line.pop(-1)
    file.write(str(count)+',')
    for data in line[5:9]:
      print (data)
      file.write(data+',')
    file.write('\n')
    count=count+1
    

  
    
  
  
#sortListFile()
#run()
#sortEndFile()

#csv2dxf.csvtodxf()
