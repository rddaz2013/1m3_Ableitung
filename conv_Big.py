#!/usr/bin/env python

# Author: Carl Sandrock
# https://github.com/alchemyst/datareaders/blob/master/lvm.py
# erweitert von RD

import StringIO
from string import ascii_lowercase

import numpy


def iterbuf(buf):
    stri = StringIO(buf)
    while True:
        nl = stri.readline()
        if nl != '':
            yield nl.strip()
        else:
            raise StopIteration


class lvm:

    def Get_Single_Data(self,infile):
        temp_list = []
        temp_file = StringIO.StringIO()

        NewChanncel = False
        for line in infile:
            if "Channels" in line:
                if NewChanncel:
                    temp_list.append(temp_file)
                    temp_file = StringIO.StringIO()
                    #print temp_file.getvalue()
                else:
                    NewChanncel = True

            if NewChanncel:
                temp_file.write(line+'\n')

        return temp_list

    def Get_Single_Data_Header(self,infile2):
        sectionheader = {}
        infile2.seek(0)
        for line in infile2:
            if not line.strip():
                continue

            if "***End_of_Header***" in line:
                break
            items = line.strip().split(self.delimiter)
            sectionheader[items[0]] = items[1:]
        else:
            raise
        return sectionheader


    def __init__(self, f):
        """
        Read an LVM file as documented in http://www.ni.com/white-paper/4139/en

        Note: Special blocks are ignored.
        """

        if hasattr(f, 'next'):
            self.filename = f.name
            self.filename_ext =f.name.split('.')[0]
            infile = f
        else:
            self.filename = f
            self.filename_ext =f.split('.')[0]
            infile = open(f)

        assert infile.next().startswith('LabVIEW Measurement'), "Invalid file"

        # FIXME: This should be read from the header
        self.delimiter = '\t'

        # Read header
        self.header = {}
        for line in infile:
            if "***End_of_Header***" in line:
                break
            key, value = line.strip().split(self.delimiter)
            self.header[key] = value.decode("utf8")
        else:
            raise

        # Anzahl Messungen unterteilen
        # StringIO Satz fue jeden Header
        # Suche 2x"***End_of_Header***"

        """
        # Read section headers

        """

        #print temp_file.getvalue()
        #print len(temp_list)

        datablock = self.Get_Single_Data(infile)

        #print datablock[1].getvalue()

        from xlwt import Workbook
        wb = Workbook(encoding='latin-1')
        Sheet1 = wb.add_sheet('DATA')
        Sheet2 = wb.add_sheet('Legende')

        data_num = 0
        start_row = 2
        start_first = True
        Commentlist = []
        L = list(ascii_lowercase)

        for datablock in datablock:

            part_header = self.Get_Single_Data_Header(datablock)

            #name_sheet = .replace(,'').

            #if '## Kanal 1 ##' in part_header['Y_Unit_Label'][0]:
            #    Sheet1.write(1,3,part_header['Y_Unit_Label'][0])

            #if '## Kanal 2 ##' in part_header['Y_Unit_Label'][0]:
            #    Sheet1.write(2,3,part_header['Y_Unit_Label'][0])


            #print name_sheet

            #Sheet1 = wb.add_sheet(part_header['Y_Unit_Label'][0])

            #print part_header['Y_Unit_Label'][0]
            #print part_header['X0'][0]
            #print part_header['Delta_X'][0]

            datablock.readline()
            t1 = datablock.readline()
            print t1
            datablock.readline()

            t2 = datablock.readline()
            print t2

            self.data = numpy.recfromtxt(datablock, delimiter=self.delimiter,
                                     usecols=range(1+int(part_header['Channels'][0])),
                                     names=['Zeit','Druck'],
                                     dtype=float)

            self.data['Zeit'] -= float(part_header['X0'][0])
            print t1,t2,part_header['Y_Unit_Label'][0]

            #print self.data['Zeit']
            #print self.data['Druck']

            start_cell = 4

            Sheet1.write(start_cell-1,start_row,'('+str(L[start_row])+')')
            Sheet2.write(start_row*4,1,'('+str(L[start_row])+')')
            Sheet2.write(start_row*4,2,part_header['Y_Unit_Label'][0])
            Sheet2.write((start_row*4)+1,2,t1)
            Sheet2.write((start_row*4)+2,2,t2)

            for i,d in self.data:
                if start_first:
                    Sheet1.write(start_cell,start_row-1,i)
                Sheet1.write(start_cell,start_row,d)
                start_cell += 1


            start_first = False
            start_row += 1
                #print i,d





        #Sheet1.write(3,3,'Zeit [s]')
        #Sheet1.write(3,4,'Druck [bar]')
        #Sheet1.write(3,5,'Zeit [s]')
        #Sheet1.write(3,6,'Druck [bar]')



        #data_num = 0

        #from xlwt import Workbook
        #wb = Workbook()
        #Sheet1 = wb.add_sheet('Sheet1')
        #Sheet1.write(0,0,'Hello')
        wb.save(self.filename_ext+'.xls')








        """print self.sectionheader

        # TODO: Skip special blocks

        # Read data
        # FIXME: This ignores the comment column
        self.data = numpy.recfromtxt(infile, delimiter=delimiter,
                                     usecols=range(1+int(self.sectionheader['Channels'][0])),
                                     names=True,
                                     dtype=float)

        print self.data"""

    def __repr__(self):
        return "lvm('%s')" % self.filename

if __name__ == '__main__':
    print lvm('data040914.lvm')