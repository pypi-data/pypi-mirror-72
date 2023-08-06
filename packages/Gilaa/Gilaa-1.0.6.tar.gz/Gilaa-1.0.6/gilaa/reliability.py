import pandas as pd
def keepReliableAbundances(df,elem):
    if not isinstance(elem, str):
        print("The element name must be a string")
    elif not isinstance(df, pd.core.frame.DataFrame):
        print("Argument must be a Pandas data frame")
    else:
        elemLower=elem.lower()
        reliables = []
        if "flag_" + elemLower + "_fe" in df.columns:
            for i in range(len(df["flag_"+elemLower+"_fe"])):
                    if df["flag_"+elemLower+"_fe"][i] == 0:
                        #print("Elemental abundance of " + elemLower + " is reliable for star " + df["star_id"][i])
                        reliables.append(df["star_id"][i])
                    #else:
                        #print("Elemental abundance of " + elemLower + " is not reliable for star " + df["star_id"][i])
            return reliables
        else:
            print("The elemental abundance for this element is not available")
        
