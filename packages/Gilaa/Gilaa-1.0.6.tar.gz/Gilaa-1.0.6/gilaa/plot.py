import numpy as np 
import matplotlib.pyplot as plt
import astropy
import pandas as pd

def read_input(filename):
    '''
    This function takes in a csv file containing the data desired to analysed and
    returns a pandas dataframe containing the data. 

    Args: 
        filename (str): The path to the file
    
    Output: 
        data (DataFrame): The data in the form of a pandas Dataframe
    '''
    data=pd.read_csv(filename)
    return data



class plot(object):
    '''
    A class to do all the plotting from.
    Args:
        data (pandas DataFrame): a dataframe containing the data desired to be
                                 plotted.
    
    '''
    def __init__(self, data):
        if(isinstance(data, str)):
            self.data=read_input(data)
        else:
            self.data=data

    def plot_abundance(self,starname,elements,save=False,savename=False):
        '''
        Plots the elemental abundances of a given star as a bar plot.
        Args: 
            starname (list) : The star-id's of the star for which the user wishes
                             to plot abundances
            elements (list): A list signifying which elemental abundances
                             the user wishes to plot. Must be in the format
                             of the galah datafiles
            save (Boolean) : Indicates whether the created plot should be 
                             saved or not. The default setting is False.
            savename (str) : If save is set to True, a savename must be 
                             provided.
        Returns:
            abundances (list): A list of dictionaries contaning the abundances
                               for each star.
    
        '''
        
        for i in starname:
            print("Starnames: {}".format(i))
        for i in elements:
            print("Elements: {}".format(i))

        #create a list of the column labels corresponding to the desired labels

        labels=[]

        for i in elements:
            print(i)
            label=i.lower()+'_fe'

            assert (label in self.data.columns), "{} not found in data file".format(label)
            labels.append(label)


        #get abundance values for the star:

        self.data.set_index('star_id',inplace=True)
        star_data = [[], [], []]
        abundances=[{}, {}, {}]

        for i in range(len(starname)):
           star_data[i]=self.data.loc[starname[i]]
           for label in labels:
                abundances[i][label]=star_data[i][label]

        # sort alphabetically
        alph_keys=sorted(abundances[0].keys(), key=lambda x:x.lower())
        values = [[], [], []]
        for i in range(len(starname)):
            values[i]=[abundances[i][k] for k in alph_keys]


        data=self.data[[i for i in labels]]
        data=data.loc[[i for i in starname]]

        for i,val in enumerate(starname):
            starname[i]='2MASS-{}'.format(val)
        title="Chemical abundances of " + ', '.join(starname) + '.'

        data.plot(y=[i for i in labels], kind="bar",figsize=(13,17),title=title)

        plt.axhline(y=0, color='k',linestyle='-')
        plt.savefig('{}.png'.format(savename))
        plt.show()

        return abundances

    def errorPlot(self,star_ids,variables,save=False,savename=False):
        '''
        PLots error bars.

        Args:
            star_ids  (list): A list of star-id's the user wishes to generate the 
                              plot for
            variables (list): A list of strings represented the stellar parameters
                              the user is interested in 
            save (Boolean) : Indicates whether the created plot should be 
                             saved or not. The default setting is False.
            savename (str) : If save is set to True, a savename must be 
                             provided.
        
        Returns: 
            id_var_err (dict) : Dictionary containing information about the 
                                errors associated with each of the parameters
                                in variables.

        '''
        
        data=self.data

        if not (isinstance(variables, list)):
            print("Variable names must be a list of strings")
        elif not (isinstance(star_ids, list)):
            print("Star ID must be a list of strings")
        elif not isinstance(data, pd.core.frame.DataFrame):
            print("Argument must be a pandas dataframe")
        else:
            with_uncer = []
            for variable in variables:
                if not variable in data.columns:
                    print(variable + "is not a valid variable name")
                if "e_" + variable in data.columns:
                    with_uncer.append(variable)
                else: 
                    print("The variable " + variable + "does not have an associated uncertainty")
            id_var_err = {}
            #indeces = [data[data["star_id"] == starid].index[0] for starid in star_ids]
            for star_id in star_ids:
                index = data[data["star_id"] == star_id].index[0]
                id_var_err[star_id] = [[data[x][index] for x in with_uncer], [data["e_" + x][index] for x in with_uncer]]
            
            #make figure
            fig = plt.figure()
            x_marks = np.arange(len(with_uncer))
            for star_id in star_ids:
                plt.errorbar(x_marks, id_var_err[star_id][0], yerr=id_var_err[star_id][1], label=star_id, marker="o")
            plt.xticks(x_marks, with_uncer)
            plt.show()
            if save:
                plt.savefig('{}.png'.format(savename))

            return id_var_err



