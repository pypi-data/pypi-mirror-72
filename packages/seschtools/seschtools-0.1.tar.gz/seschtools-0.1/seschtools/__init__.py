import base64
import json
import ast
import re
import pandas as pd
from tqdm import tqdm 
import time



'''
Usage : import seschtools
To read survery data file : seschtools.read_file('FILENAME') # Either filename with full pathname must be supplied or file must be present in the current working directory
It returns Dictionary with following key names having data as values .
FSU : Has FSU Number
SchFrame : is the Listing schedule
SchSampleHH : Particulars of Sample households
Schdl : contains All Schedules' blocks as Dataframe
'''
'''

### Iteration through each block of all the Schedules 
for schtype in Schdl: # Iterate over Schedules by type
    print(schtype)
    for schd in Schdl[schtype]: # Iterate over Schedule in each sch type
        print(schd)
        for blk in Schdl[schtype][schd]: # Iterate over Block of each sch
            # Do something
            print(len(Schdl[schtype][schd][blk]))  # Get Block data as pandas dataframe


#Schdl['33.1']['1']['5']                    
'''   


def read_nssfile(file, genFile=False): # Decodes file from base64 string into text
    if '.nss' in file : # check for valid file name 
        with open(file, 'rb') as f:
            data=f.read()
        decoded_data = base64.decodebytes(data).decode("utf-8")
        tag = re.compile('<.*?>'); decoded_data = re.sub(tag, '', decoded_data) # Remove html tags
        decoded_data = decoded_data.replace('\\\\','')
        print(type(decoded_data))
        #decoded_data = decoded_data.replace('\"','"')
        if genFile: # Creates text file having decoded survey data
            file=file.replace('.nss','.txt')
            with open(file, 'w') as f:
                f.write(decoded_data)
            with open(file) as f_in:
                data=json.load(f_in)
        else:
            data=json.loads(decoded_data)
        return data       
    else:
        print("\n   --  File name must end with '.nss' . \n")
        exit()


def getdata(datastr): # Gives SchData and its info
    datastr=datastr.replace('"address":"{"schedule":','"address":{"schedule":').replace('","data":', ',"data":').replace('"data":{"data":"','"data":{"data":').replace('","dataStatusArray":',',"dataStatusArray":')
    datastr=datastr.replace('false','False').replace('null','False').replace('true','True')
    datadict = ast.literal_eval(datastr) 
    datainfo = datadict['address']
    if datadict['data'].get('data') is None : # No Data
        data = datadict['data']
    elif datadict['data'].get('data') is [] : # If data is [] 
        data = []
    else:
        data = datadict['data']['data']
    return datainfo, data



def getFSUInfo(SchData): # Gives all FSU related info
    fsuInfo=SchData[2] # Get FSU info dict from data
    sch00=SchData[3]
    swver=SchData[1]['version']
    fsuInfo=fsuInfo[0]['data']['records'][0]
    schStartDate=getdata(sch00['00|0|2'])[1][2]['value']
    schEndDate=getdata(sch00['00|0|2'])[1][3]['value']
    # SchData[2][0]['data']['records'][0]['FSU']
    print('\n\n\n      FSU : '+fsuInfo['FSU'])
    print('    Place : '+fsuInfo['tvn']+'('+fsuInfo['tvc']+'), '+( fsuInfo['tehn']+'('+fsuInfo['tehc']+'), ' if fsuInfo['tehn'] else '' )+fsuInfo['dn']+'('+fsuInfo['dc']+'), '+fsuInfo['st'] )

    #print('FSU : '+fsuInfo['FSU'])
    print('\n   -- Done by : '+fsuInfo['jso_name']+' ['+fsuInfo['JSO']+']  using '+swver)
    print('   -- From  '+schStartDate+'  to  '+schEndDate)
    print('\n   -- SSO : '+fsuInfo['sso_name']+' ['+fsuInfo['SSO']+']\n\n')
    
    print('      MPCE cut off : '+fsuInfo['mpce_cut_off'] )
    

    '''
	x FSU : FSU 18815
    x State : st 
    x district : dn , no : dc 
    x sub-district/tehsil/town: tehn, no. tehc
    x village name: tvn, tvc
    Sample sub-unit no. : su_no
    sunit
    hh
    nss
    rep
    
    frame code: fc

    stratum: strm
    sub stratum : sstrm
    sub round : subr
    
    x mpce cut off : mpce_cut_off
    
    population of village/number of households of UFS block:
    : pop
    
 
    investigator unit no: iv
    block no: bl
        
'''
    
    
def getschFrame(sch00): # Gives SCH Frame
    schframeinfo,schFrame=getdata(sch00['00|0|5A'])
    # schframeinfo,schFrame=getdata(sch00['00|0|6'])
    schFrameLabels=['house number',  'HH SNo.', 'name of head of the household', 'household size','land possessed', 'value of agricultural production', 	'indebted to institutional agencies', 'indebted to non−institutional agencies', 'monthly consumer expenditure',	'MPCE', 'MPCE code','SSSNo. 33.1', 'SSSNo. 18.2', '33.1 Selected HH', '18.2 Selected HH' ]
    schFrameLabels=schFrameLabels if len(schFrame[0])==len(schFrameLabels) else [ schFrameLabels[i] for i in [0,1,2,3,6,7,8,9,10,12,14] ]
    SCHFRAME={}
    for HH in schFrame:
        if not all(v is '' for v in HH): # Check for empty row
            HH[1]=HH[1].replace('(','').replace(')','')
            SCHFRAME[HH[1]]={}
            n=1
            for label in schFrameLabels:
                SCHFRAME[HH[1]][label]=HH[n]
                n+=1
    schFrameDF=pd.DataFrame(SCHFRAME).T
    schFrameDF.index=schFrameDF['HH SNo.']
    return schFrameDF 

def dictdepth(dicti) : # Tells Depth of the passed Dictionary
    depth=0
    if dicti:
       while isinstance(dicti, dict):
           for k in dicti:
               dicti=dicti[k]
               depth+=1
               break
    return depth

def getschsamplehh(sch00):
    SchSampleHHlabel={'H':'listed', 'h':'selected', 'hhlist':'selected HH', 'population':'population', 'o':'originally selected', 's':'substituted', 'st':'total', 'c':'casualty', 'r':'replaced'}
    SchSampleHH={}
    for schtype in ['33.1', '18.2']:
       if len(getdata(sch00['00|0|6'])[1]['h'+schtype.replace('.','')]['H']) > 1 : # Check for empty schedule type
            SchSamplehhDF=pd.DataFrame(getdata(sch00['00|0|6'])[1]['h'+schtype.replace('.','')])[1:]
            SchSamplehhDF['hhlist']=SchSamplehhDF['hhlist'].apply(lambda item: ' '.join('['+str(n+1)+'. '+i+' ]' for n,i in enumerate([ '---'.join(str(i).strip() for i in lst if i) for lst in item ]))) # Make HH list items into string
            SchSamplehhDF.columns = [ SchSampleHHlabel[col] for col in SchSamplehhDF.columns]
            SchSampleHH[schtype]=SchSamplehhDF
    return SchSampleHH


def getschdl(SchData):
    FSU=SchData[2][0]['data']['records'][0]['FSU']
    Schs=SchData[4:]  # Get all schedules from Sch data
    Schdl={}
    with tqdm(total=100) as pbar:
         for sch in Schs: # All schedules
            for schblk in sch: # Block by block for Each schedule
                pbar.set_description("  Processing.. ["+FSU+'] : '+schblk.split('-',1)[-1])
                pbar.update(100/(len(Schs)*len(sch)))
                time.sleep(0.1/(len(Schs)*len(sch)))
                #print(schblk)
                schtype=schblk.split('-')[1]
                Schdl.setdefault(schtype,{}) # Set Sch 33.1 & 18.1 as dict key
                _, schnum, schblock=schblk.split('|')
                Schdl[schtype].setdefault(schnum,{}) # Set Sch number as dict key        
                #SCH[schtype][schnum].setdefault(schblock,{}) # Set Sch block as dict key
                schInfo, schData = getdata(sch[schblk])
                schblktable={}
                if schData: # For non empty schedules
                    if isinstance(schData[0],list): # Having List data only
                        for schitem in schData: # Iterate over Items (list type)
                            #print(schitem)
                            if 'item' not in schitem[0]:                            
                                if '-' in schitem[0]: # if item & col are given
                                    item,col=schitem[0][1:].split('-') # Get item & col position from first element of list schitem 
                                    schblktable.setdefault(item,{}) # Set item as key 
                                    #print(schitem,schitem[0],item,schitem[1])
                                    for colEntry in schitem[1:-1]: #Exclude 1st & extra last element
                                        schblktable[item][col]=colEntry
                                elif '-' not in schitem[0] : # Entries w/o column e.g. blk 0, 4
                                    item=schitem[0][1:] # Entry No.
                                    #for itemEntry in schitem[1:-1]: 
                                    schblktable[item]=schitem[1]  # Take 2nd element only
                            elif 'item' in schitem[0] : # For entries w/o col with item str i.e.blk 1
                                item=schitem[0].split('item')[-1]  # Entry No.
                                schblktable[item]=schitem[1]  # Take 2nd element only
                            #print(schitem)
                            #Schdl[schtype][schnum][schblock]=schtableDF
                            # if 'item' in schitem[0] or '-' not in schitem[0]: # Block entries
                            #     schtableDF=pd.Series(schblktable)
                            #     Schdl[schtype][schnum][schblock]=schtableDF
                            #     print(schblk)
                            #     print(schitem)                        
                            #print(schblktable)
                    
                if dictdepth(schblktable) > 1: # Create its DataFrame if there is dictionary inside dictionary i.e. depth=2
                    schtableDF=pd.DataFrame(schblktable).T
                elif dictdepth(schblktable) == 1:
                    schtableDF=pd.Series(schblktable)
                Schdl[schtype][schnum][schblock]=schtableDF
    return Schdl

def read_file(file, verbose=True): # The Main Function that Reads schedule File & returns schedule data as Dataframe
    SchData=read_nssfile(file)  # Get data from Survey data file present as List
    sch00=SchData[3]  # Get sch0.0 dict from data
    FSU=SchData[2][0]['data']['records'][0]['FSU']
    
    SchFrameDF=getschFrame(sch00)
    SchSampleHH=getschsamplehh(sch00)
    Schdl=getschdl(SchData)
    if verbose:
        getFSUInfo(SchData)
        print()
        for st in Schdl:
            print('      Total Sch:['+st+'] :: '+str(len(Schdl[st])))
    
    #return FSU, SchFrameDF, SchSampleHH, Schdl  # as Tuple
    return { 'FSU':FSU, 'SchFrame':SchFrameDF, 'SchSampleHH':SchSampleHH, 'Schdl':Schdl }  # as Dictionary
    # Returns FSU No., Schedule Frame, Sample Households, Schedules
    
 
if __name__ == '__main__':
    file='18815_ROUND77v2_FINAL_S_1306_1515.v2.nss'
    #'26940_ROUND77v2_S_1406_1854.v2.nss'
    
    #FSU, SchFrameDF, SchSampleHH, Schdl = readsch(file)
    schData = read_file(file)
    





