import pandas as pd
'''
Below I have constructed a class whose methods perform the necessary data 
manipulations to produce the results. The results are displayed when running 
main.
'''
class Portfolio_Calc:
    
    def __init__(self,security_path,holding_path):
        
        self.path1 = security_path
        self.path2 = holding_path
        
    #This method converts the txt files to pandas DataFrames for manipulation
    
    def load_files(self,delimiter = '|'):
        security = pd.read_csv(self.path1,sep=delimiter,header=None)
        security.columns = ['SecurityID','Ticker','Name','Sector',
                            'Security Market Price']
        
        holdings = pd.read_csv(self.path2,sep=delimiter,header=None)
        holdings.columns = ['SecurityID','Quantity','Cost Basis']
        return security,holdings
    
    
    
    #the merge data method creates a third DataFrame 'merged_data' formed from
    #a left_join of holdings and security. This way we only keep records that
    #are in the portfolio and augment the holdings data with security market
    #price and sector which will be necessary for the calculations we must make
    
    def merge_data(self,security,holdings,column = 'SecurityID'):
        
        merged_data = pd.merge(holdings,security,on=column,how='left')
        
        #now that the dataframes are merged we perform a groupby in order to 
        #replace the Quantity in each row with the sum of the Quantity for 
        #each Security. Finally we drop rows with duplicated security ids
        
        ef = merged_data.groupby('SecurityID').sum().Quantity
        merged_data['Quantity'] = merged_data.apply(lambda row :
                                                    ef[row['SecurityID']],axis=1)
        
        merged_data.drop_duplicates(['SecurityID'],inplace=True)
        return merged_data
    
    
    #the Portfolio_market_value method simply adds a Value column to merged_data
    #the Value column is the product of the quantity of each security multiplied
    #by its market price.
    
    def Portfolio_market_value(self,data):
        data['Value'] = data['Quantity'] * data['Security Market Price']
        return round(sum(data['Value']),2)
    
    
    #we perform a second groupby on merged_data except this groupby is by Sector
    #the code obtains the sum of 'Value' across all rows (securities) in the 
    #same sector. The result is a total market value in each sector
    
    def Sector_Groups(self,data):
        Sector_Sums = data.groupby('Sector').sum().Value
        Sector_Sums = pd.DataFrame(Sector_Sums)
        Sector_Sums.reset_index(inplace=True)
        return Sector_Sums
    
    #we take the result of the previous method and obtain a portfolio weight by
    #dividing sector value by total portfolio market value
    
    def Portfolio_sector_weights(self,data):
        Total_val = sum(data['Value'])
        data['Weight'] = data['Value'] / Total_val
        return data
        
        
        
if __name__=="__main__":
    
    #When running these calculations, the only alteration that must be made is 
    #that the parameters of the initial call of the Portfolio_Calc Class need 
    #to be changed to the respective paths for the securitydata and holdingdata
    #txt files on the user's local device
    
    result = Portfolio_Calc('/Users/tarikrashada/Downloads/securityData.txt',
                            '/Users/tarikrashada/Downloads/holdings.txt')
    
    security,holdings = result.load_files()
    
    merged_data = result.merge_data(security,holdings)
    
    Port_val = result.Portfolio_market_value(merged_data)
    
    print("The Portfolio Market Value is: $" + str(Port_val))
    #16486124.78
    
    sector_sums = result.Sector_Groups(merged_data)
    #print(sector_sums)
    
    Port_weights = result.Portfolio_sector_weights(sector_sums)
    print(Port_weights)
    
    result_file = open("result_file.txt","w")
    result_file.write("The Portfolio Market Value is: $" + str(Port_val))
    
    for i in range(len(Port_weights)):
        result_file.write("\nThe Portfolio Weight for the "+
                          str(Port_weights.loc[i,'Sector'])+" Sector is: "
                          +str(round(Port_weights.loc[i,'Weight']*100,2))+ "%.")
        
    result_file.close()
