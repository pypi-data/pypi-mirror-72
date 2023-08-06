import pandas as pd
import numpy as np

import skrf as srf
import rftool.utility as util

def csv2network(path, port=''):
    """
    Converts CSV files from Sigilent Vector Spectrum Analyzers to a Scikit RF networks.
    Currently only supporting one trace at a time (Log Mag and Phase).

    path is the path to the csv file.
    MeasType selects the trace to analyze, string e.g., 'S11'.
    """
    # Create data frame from CSV
    df = pd.read_csv(path, sep=',', names=['Frequency','Value'])

    # Find number of traces
    temp = df[df['Frequency'].str.contains('Trace Name')]
    numbOfTraces  = temp.shape[0]
    rowNumb = temp.index.values.tolist()

    # Separate the various traces
    traces = []
    for i in range(0,numbOfTraces):
        if i<numbOfTraces-1:
            traces.append(df.loc[rowNumb[i]:rowNumb[i+1]-1,:])
        else:
            traces.append(df.loc[rowNumb[i]:,:])

    # Extract frequency axis (assumed to be the same for all traces)
    dataStartIndex = df[df['Frequency'] == 'Trace Data'].index[0]+2
    freq = traces[0].loc[:,'Frequency'].loc[dataStartIndex:].astype(float).to_numpy()*1e-9 # conversion to GHz
    

    pre_defined_kwargs = {'z0': 50, 'frequency': freq}
    s_deg = 0 # If no Phase trace is found, tthe default phase i 0 deg.
    # Extract traces
    for idx, trace in enumerate(traces):
        # Identify the trace type:
        tracePort = trace.loc[df['Frequency'] == 'Meas Type'].values[0][1]
        dataStartIndex = trace[trace['Frequency'] == 'Trace Data'].index[0]+2
        traceType = trace[trace['Frequency']=='Format']['Value'].to_list()[0]

        if(port==tracePort):
            # Add to Network object
            if traceType == 'Log Mag':
                s_db=trace.loc[:,'Value'].loc[dataStartIndex:].astype(float).to_numpy()
            elif traceType == 'Phase':
                #n.s_deg = [1,2,3]#trace.loc[:,'Value'].iloc[dataStartIndex:].astype(float).to_numpy()
                s_deg=trace.loc[:,'Value'].loc[dataStartIndex:].astype(float).to_numpy()

    sParam = util.db2mag(s_db)*np.exp(1j*s_deg/360*2*np.pi)

    # Create Network object
    n = srf.Network() 
    n.f, n.s, n.z0 = freq, sParam, 50
    return n