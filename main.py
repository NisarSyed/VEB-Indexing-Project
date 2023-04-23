from src.veb_tree import *
from src.gui import *
import pandas as pd
import time
import os
import pickle

class Index:
    def __init__(self, path: str) -> None:
        self.data = self.load_data(path)
        self.itemIDIndex = VEBTree(len(self.data))
        
        
        start = time.time()
        if os.path.exists("itemIndex"):
            self.itemIDIndex = pickle.load(open("itemIndex", "rb"))
        else:
            self.itemIDIndex = self.createIndex('item_id', self.data)
            pickle.dump(self.itemIDIndex, open("itemIndex", "wb"))
        
        if os.path.exists("priceIndex"):
            self.priceIndex = pickle.load(open("priceIndex", "rb"))
            #self.get_sorted_indices(self.priceIndex, 'price')
        else:
            self.priceIndex = self.createIndex('price', self.data)
            pickle.dump(self.priceIndex, open("priceIndex", "wb"))
        end = time.time()
        print(f'Time Taken: {end-start}')

    def createIndex(self, indexBy: str, data: pd.DataFrame) -> VEBTree:
        map = {}
        for _, record in self.data.iterrows():
            map[record[indexBy]] = record

        index = VEBTree(len(map))

        for item in map:
            index.insert(item)
        return index
        
    def load_data(self, path: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        df = df.drop(df.columns[21:26], axis=1)
        df = df.drop(df.index[584524:])
        df = df.drop(['increment_id','discount_amount','sales_commission_code','BI Status',' MV ','Year','Month','M-Y','FY'], axis=1)
        return df
    
    def search(self, attribute: str, value: int) -> pd.DataFrame:
        if attribute == 'item_id':
            index = self.itemIDIndex.search(value)
        elif attribute == 'price':
            index = self.priceIndex.search(value)
        
        return self.data[self.data[attribute] == index]
    
    def rangeSearch(self, attribute: str, start: int, end: int) -> pd.DataFrame:
        if attribute == 'item_id':
            index = self.itemIDIndex
        elif attribute == 'price':
            index = self.priceIndex

        result = pd.DataFrame()
        result = pd.concat([result, self.data[self.data[attribute] == index.search(start)]])
        while True:
            next_item = index.successor(start)
            if next_item == None or next_item > end:
                break
            result = pd.concat([result, self.data[self.data[attribute] == next_item]])
            start = next_item
        return result

    # def sort(self, attribute: str) -> pd.DataFrame:
    #     return self.data.sort_values(by=[attribute], ascending=False)
    
    def successor1(self, attribute: str, value: int) :
       
        if attribute == 'item_id':
            index = self.itemIDIndex
        elif attribute == 'price':
            index = self.priceIndex
        
        return self.data[self.data[attribute] == index.successor(value)]
    
    def check(self):
        # check whether the order id is present in the data or not
        # if present then return the data
        # else return false
        pass
    def get_sorted_indices(self, indices: List[int], sort_by: str) -> List[int]:
        if sort_by == 'item_id':
            indices = list(indices)
            sorted_indices = sorted(indices, key=lambda x: self.data[sort_by][x])
            print(sorted_indices)
            return sorted_indices
        elif sort_by == 'price':    
            indices = list(indices)
            sorted_indices = sorted(indices, key=lambda x: self.data[sort_by][x], reverse=True)
            print(sorted_indices)
            return sorted_indices

if __name__ == "__main__":
    app = Index('data\Pakistan Largest Ecommerce Dataset.csv')
    # result = app.rangeSearch('price', 0, 100)
    # print(result[['item_id', 'price']])
    gui  = GUI(app.data)
    gui.run()
    
    #app.rangeSearch('price', 0, 100)
    
    
    
    
