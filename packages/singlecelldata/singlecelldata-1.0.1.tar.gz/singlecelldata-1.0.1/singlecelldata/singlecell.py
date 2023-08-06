# Import Packages
import pandas as pd
import numpy as np



class SingleCell:
    """
    A python class for managing single-cell RNA-seq datasets.


    Attributes
    ----------
    dataset : str
        A string for the name of the dataset.

    data : Pandas Dataframe
        The main dataframe or assay for storing the gene expression counts. The shape of this 
        dataframe is (d x n) where d is the number of genes (features) and n is the 
        number of cells (samples).
    
    celldata : Pandas Dataframe
        The dataframe or assay used to store more data (metadata) about cells. The shape of this dataframe
        is (n x m), where m is number of columns representing different types of information
        about the cells, such as cell types etc.

    genedata : Pandas Dataframe
        The dataframe or assay used to store more data (metadata) about genes. The shape of this dataframe
        is (d x m), where m is number of columns representing different types of information
        about the genes such as gene names etc.
    
    dim : tuple
        Variable representing the dimensionality of the data assay. It is (d, n).
        


    Methods
    -------







    """
    
    dataset = None      
    data = None         
    celldata = None   
    genedata = None     
    dim = None

    spike_ins_names = np.array([])


    
    def __init__(self, dataset, data, celldata = None, genedata = None):
        """
        Parameters
        ----------

        dataset : str
            The name of the single-cell dataset.

        data : Pandas Dataframe
            The main dataframe storing the gene expression counts/values.

        celldata : Pandas Dataframe, optional
            The dataframe or assay used to store more data (metadata) about cells. By default, a
            dataframe will be created with one column 'cell_names' storing the cell names as 
            Cell1, Cell2, ..., Celln.

        genedata : Pandas Dataframe, optional
            The dataframe or assay used to store more data (metadata) about genes. By default, a
            dataframe will be created with one column 'gene_names' storing the gene names as 
            Gene1, Gene2, ..., Gened.

        """
    
        # TODO: Validate inputs

        self.dataset = dataset
        self.data = data
        self.dim = data.shape

        if (type(genedata) is type(None)):
            num_genes = data.shape[0]
            gene_names = []
            for i in range(num_genes):
                gene_names.append('Gene' + str(i+1))

            self.genedata = pd.DataFrame(gene_names, index = data.index, columns = ['gene_names'])

        else:
            self.genedata = genedata

        if (type(celldata) is type(None)):
            num_cells= data.shape[1]
            cell_names = []
            for i in range(num_cells):
                cell_names.append('Cell' + str(i+1))

            self.celldata = pd.DataFrame(cell_names, index = data.columns, columns = ['cell_names'])
            
        else:
            self.celldata = celldata


    def print(self): # Print the single cell object summary
        """ 
        Prints a summary of the single-cell dataset. 
        
        """

        print ("------------------------------------------------------------------------------")
        print ("Dataset: ", self.dataset)
        print ("------------------------------------------------------------------------------")
        print ("Dimension: ", self.dim)
        print ("Cell Metadata: ", self.celldata.columns.values)
        print ("Gene Metadata: ", self.genedata.columns.values)
        print ("------------------------------------------------------------------------------")
                

    def __getcolslice(self, key):
        # if key is a string
        if (type(key) is str):
            new_data = self.data.loc[:, key]
            new_celldata = self.celldata.loc[key, :]
            new_genedata = self.genedata

        # if key is an int
        elif (type(key) is int):
            new_data = self.data.iloc[:, key]
            new_celldata = self.celldata.iloc[key, :]
            new_genedata = self.genedata

        # if key is a slice object
        elif (type(key) is slice):

            if (type(key.start) is str):
                new_data = self.data.loc[:, key]
                new_celldata = self.celldata.loc[key, :]
                new_genedata = self.genedata

            else:
                new_data = self.data.iloc[:, key]
                new_celldata = self.celldata.iloc[key, :]
                new_genedata = self.genedata

        # if key is a list
        elif (type(key) is list):
            if (type(key[0]) is str):
                new_data = self.data.loc[:, key]
                new_celldata = self.celldata.loc[key, :]
                new_genedata = self.genedata

            else:
                new_data = self.data.iloc[:, key]
                new_celldata = self.celldata.iloc[key, :]
                new_genedata = self.genedata

        else:
            raise ValueError("Unknown/unsupported type for parameter key; use either a slice object or a default python list!")
        
        return new_data, new_celldata, new_genedata




    def __getitem__(self, key):
        """
        This method implements slicing operation.  

        """

        if (type(key) is tuple):
            row, col = key
            c_data, c_celldata, c_genedata = self.__getcolslice(col)

            # Row slicing is only by int or int list or int slice object

            # if row is a string
            if (type(row) is str):
                raise ValueError("Cannot slice rows using string!")

            # if row is an int
            elif (type(row) is int):
                raise ValueError("Cannot slice rows using a single int. Use an int list instead!")

            # if row is a slice object
            elif (type(row) is slice):

                if (type(row.start) is str):
                    raise ValueError("Cannot slice rows using string!")

                else:
                    new_data = c_data.iloc[row, :]
                    new_celldata = c_celldata
                    new_genedata = c_genedata.iloc[row, :]

            # if row is a list
            elif (type(row) is list):
                if (type(row[0]) is str):
                    raise ValueError("Cannot slice rows using string!")   

                else:
                    new_data = c_data.iloc[row, :]
                    new_celldata = c_celldata
                    new_genedata = c_genedata.iloc[row, :]

            elif (type(row) is np.ndarray):
                if (type(row[0]) is str):
                    raise ValueError("Cannot slice rows using string!")   

                else:
                    new_data = c_data.iloc[row, :]
                    new_celldata = c_celldata
                    new_genedata = c_genedata.iloc[row, :]
            
            else:
                raise ValueError("Unknown type used to slice rows! Row slicing can only be done using int, int list or numpy array!")

        else:
            new_data, new_celldata, new_genedata = self.__getcolslice(key)



        # Create a new SingleCell object and return the sliced assays
        new_sc = SingleCell(self.dataset, new_data, new_celldata, new_genedata)

        return new_sc


    def __setitem__(self, key, value):
        pass


    def __delitem__(self, key):
        pass


    """
    METHOD: getLogCounts() - Depreciated 23/06/2020
    ----------------------

    Returns a numpy array of the log (base2) of the counts in the data dataframe. This method is called form the
    class instance and requires no input arguments. 



    def getLogCounts(self):
        
        data = self.data.values

        # Check is gene filtering has been performed
        if (self.checkGeneDataColumn("gene_filter") == True):
            gene_filt = self.genedata["gene_filter"].values
            data = data[gene_filt, :]

        # Check is cell filtering has been performed
        if (self.checkCellDataColumn("cell_filter") == True):
            cell_filt = self.celldata["cell_filter"].values
            data = data[:, cell_filt]

        return np.log2(data + 1)
    """
    

    def getCounts(self):
        """
        Returns a Numpy array of the counts/data in the data dataframe. This method is called from the
        class instance and requires no input arguments. 

        Returns
        -------

        Numpy array
            A (d x n) array of gene expression counts/data. 

        """
        
        data = self.data.values

        # Check is gene filtering has been performed
        if (self.checkGeneData("gene_filter") == True):
            gene_filt = self.genedata["gene_filter"].values
            data = data[gene_filt, :]
       
        # Check is cell filtering has been performed
        if (self.checkCellData("cell_filter") == True):
            cell_filt = self.celldata["cell_filter"].values
            data = data[:, cell_filt]

        return data  
    

    
    def setCounts(self, new_counts):
        """
        Sets the new counts values in the data dataframe. 

        Parameters
        ----------

        new_counts : Numpy array
            A numpy array with the shape = dim, representing new count values. The data dataframe will 
            be updated with the new count values.  

        """
        # Update the data values for the cells and genes that were used
        # Check is cell filter is available
        # if (self.checkCellDataColumn("cell_filter") == True):
        #     cell_filt = self.celldata["cell_filter"].values
        #     cell_idx = np.where(cell_filt)

        #     # Check is gene filter is available
        #     if (self.checkGeneDataColumn("gene_filter") == True):
        #         gene_filt = self.genedata["gene_filter"].values
        #         for i in range(cell_idx):
        #             self.data.values[gene_filt, cell_idx[i]] = new_counts[:, i]
            
        #     else:
        #         for i in range(cell_idx):
        #             self.data.values[:, cell_idx[i]] = new_counts[:, i]

        # else: # if cell filter is not available

        #     # Check is gene filter is available
        #     if (self.checkGeneDataColumn("gene_filter") == True):
        #         gene_filt = self.genedata["gene_filter"].values
        #         for i in range(self.dim[1]):
        #             self.data.values[gene_filt, i] = new_counts[:, i]
            
        #     else:
        #         for i in range(self.dim[1]):
        #             self.data.values[:, i] = new_counts[:, i]
        df = pd.DataFrame(new_counts, index = self.data.index, columns = self.data.columns)
        self.data = df


    def checkCellData(self, column):
        """
        Checks whether a column exists in the celldata dataframe. 

        Parameters
        ----------

        column : str
            The name of the column. 

        Returns
        -------

        bool
            True if column exists in the dataframe, False otherwise.  

        """

        cell_data_cols = self.celldata.columns.values
        
        status = False
        
        for i in cell_data_cols:
            if (i == column):
                status = True
                
        return status
    

    def checkGeneData(self, column):
        """
        Checks whether a column exists in the genedata dataframe. 

        Parameters
        ----------

        column : str
            The name of the column. 

        Returns
        -------

        bool
            True if column exists in the dataframe, False otherwise.  

        """

        gene_data_cols = self.genedata.columns.values

        status = False

        for i in gene_data_cols:
            if (i == column):
                status = True

        return status




    def isSpike(self, spike_type, gene_names_column):
        """
        Prints a message if spike-ins are detected in the dataset. Creates 
        a filter to remove spike-ins from the dataset when counts/data is 
        returned using getCounts() method.   

        Parameters
        ----------
        spike_type : str
            A string representing the type of spike-in. 

        """
        
        mask = np.zeros(self.dim[0], dtype=bool)
        
        if (self.checkGeneData(gene_names_column)):
            gene_labels = self.genedata[gene_names_column].values
            mask = pd.Series(gene_labels).str.contains(spike_type).tolist()
            
            # ser = self.genedata.duplicated(subset="feature_symbol")
            total = np.sum(mask)
            if (total > 0):
                print("Spike-ins '", spike_type, "' exists in the dataset!")
                self.spike_ins_names = np.append(self.spike_ins_names, spike_type)

                if (self.checkGeneData("gene_filter") == True):
                    gene_filt = self.genedata["gene_filter"].values[mask]
                    gene_filt[mask] = False
                    self.genedata["gene_filter"] = gene_filt

                else:
                    gene_filt = np.ones(self.dim[1], dtype = bool)
                    gene_filt[mask] = False
                    df = pd.DataFrame(data = gene_filt, columns = ["gene_filter"], index = self.genedata.index)
                    self.genedata = pd.concat([self.genedata, df], axis = 1)

            else:
                print("Spike-ins '", spike_type, "' does not exist in the dataset!")
            
        else:
            print(gene_names_column," column not found in gene meta-data!")
        
    
        
    def addGeneData(self, col_data, col_name):
        """
        Adds a column in the genedata dataframe. 

        Parameters
        ----------

        col_data : List or Numpy array
            The data to be added to the genedata dataframe. The size of the List 
            or Numpy array should be equal to d.

        col_name : str
            The name of the data column. 

        """

        self.removeGeneData(col_name)

        # To do: check the col_data to see if it matches the required shape.
        # Check if Gene Filter has been applied 
        if (self.checkGeneData("gene_filter")):
            gene_filt = self.genedata["gene_filter"].values
            data = np.zeros(self.dim[0])
            data[gene_filt] = col_data
            df = pd.DataFrame(data = data, columns = [col_name], index = self.genedata.index)

        else:
            df = pd.DataFrame(data = col_data, columns = [col_name], index = self.genedata.index)

        self.genedata = pd.concat([self.genedata, df], axis = 1)
        


    def addCellData(self, col_data, col_name):
        """
        Adds a column in the celldata dataframe. 

        Parameters
        ----------

        col_data : List or Numpy array
            The data to be added to the celldata dataframe. The size of the List 
            or Numpy array should be equal to n.

        col_name : str
            The name of the data column. 

        """

        self.removeCellData(col_name)
        # To do: check the col_data to see if it matches the required shape.
        # Check if Cell Filter has been applied 
        if (self.checkCellData("cell_filter")):
            cell_filt = self.celldata["cell_filter"].values
            data = np.zeros(self.dim[1])
            data[cell_filt] = col_data
            df = pd.DataFrame(data = data, columns = [col_name], index = self.celldata.index)

        else:
            df = pd.DataFrame(data = col_data, columns = [col_name], index = self.celldata.index)

        self.celldata = pd.concat([self.celldata, df], axis = 1)


    def removeCellData(self, column):
        """
        Removes a column from the celldata dataframe. First checks
        whether the column exists in the celldata dataframe.

        Parameters
        ----------

        column : str
            The name of the data column. 

        """

        if (self.checkCellData(column)):
            self.celldata = self.celldata.drop([column], axis=1)
            print ("Removing '", column, "' from CellData assay")

    

    def removeGeneData(self, column):
        """
        Removes a column from the genedata dataframe. First checks
        whether the column exists in the genedata dataframe.

        Parameters
        ----------

        column : str
            The name of the data column. 

        """

        if (self.checkGeneData(column)):
            self.genedata = self.genedata.drop([column], axis=1)
            print ("Removing '", column, "' from GeneData assay")



    def getCellData(self, column):
        """
        Returns data stored in the celldata dataframe. 

        Parameters
        ----------

        column : str
            The name of the data column.

        Returns
        -------

        Numpy array 
            A n-dimensional array containing cell data by the column name.
        
        Raises
        ------

        ValueError
            If column does not exist in the celldata dataframe.

        """

        if (self.checkCellData(column)):
            data =  self.celldata[column].values

            if (self.checkCellData("cell_filter") == True):
                cell_filt = self.celldata["cell_filter"].values
                data = data[cell_filt] 

            return data

        else:
            raise ValueError ("'", column, "' does not exist in CellData assay")
    


    def getGeneData(self, column):
        """
        Returns data stored in the genedata dataframe. 

        Parameters
        ----------

        column : str
            The name of the data column.

        Returns
        -------

        Numpy array 
            A d-dimensional array containing gene data by the column name.
        
        Raises
        ------

        ValueError
            If column does not exist in the genedata dataframe.

        """

        if (self.checkGeneData(column)):
            data = self.genedata[column].values

            if (self.checkGeneData("gene_filter") == True):
                gene_filt = self.genedata["gene_filter"].values
                data = data[gene_filt] # 19/08/2019 - corrected error here in the code (bugfix, that prevented returning data stored in genedata assay)
            
            return data
            
        else:
            raise ValueError ("'", column, "' does not exist in GeneData assay")  

  

    
    def getDistinctCellTypes(self, column):
        """
        Returns the unique cell type information stored in the celldata dataframe.

        Parameters
        ----------

        column : str
            This parameter is the column name of the cell labels in the celldata assay.

        Returns
        -------

        Numpy array
            Containing unique values in the celldata dataframe under the column passed into 
            this function.  

        """

        cellarray = self.getCellData(column)
        # cells = cellarray

        # cell_types = np.array([]) # Distinct cell labels in the cellarray

        # # Find distinct cell lables in the cell array
        # while (cells.size != 0):
        #     cell_types = np.append(cell_types, cells[0])
        #     mask = cells != cells[0]
        #     cells = cells[mask]

        # cell_types = np.sort(cell_types)
        
        # return cell_types
        return np.unique(cellarray)




    def getNumericCellLabels(self, column):
        """
        Returns the numeric (int) cell labels from the celldata assay which contains the string or int cell labels. 
        This method is useful when computing Rand Index or Adjusted Rand Index after clustering. 

        Parameters
        ----------

        column : str
            This parameter is the column name of the string or int cell labels in the celldata assay.

        Returns
        -------

        Numpy array (int)
            Array containing the integer representation of data in the celldata dataframe under the 
            column passed into this function.

        """

        cellarray = self.getCellData(column)
        cell_types = self.getDistinctCellTypes(column)

        num_cell_labels = np.zeros(cellarray.size, dtype = np.int16) # Numeric cell labels

        # Find numeric cell labels for the cell array 
        for i in range(cell_types.size):
            mask = (cellarray == cell_types[i])
            num_cell_labels[mask] = i + 1
        
        return num_cell_labels
        