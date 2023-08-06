import numpy as np 
import matplotlib.pyplot as plt
import astropy
import pandas as pd
import gilaa.plot as plot

def example():
    
    '''
    This function just shows a simple use case for the code.
    Saves the plots made to /data/
    
    '''

    #plotting abundances
    data=pd.read_csv("../data/ngc632.csv")
    star=plot(data)
    starname=star.data['star_id'][0:3]

    star.plot_abundance(starname,['o','ca','ba','c','ti','mg'],save=True,savename='../plots/test_abundances')

    #plotting with errorbars
    variables = ["al_fe", "ba_fe", "eu_fe"]
    stars= ["13321909-7822135", "13322043-3651561"]

    thou=plot("../data/top1000.csv")
    thou.errorPlot(variables,stars,save=True,savename="../plots/test_error")

    print("Done!")
