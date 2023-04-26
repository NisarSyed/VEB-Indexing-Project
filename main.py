from src.veb_tree import *
from src.gui import *
import pandas as pd
import time
import os
import pickle

class Index:
    def __init__(self, path: str) -> None:
        self.data = self.load_data(path)
        
        start = time.time()
        if os.path.exists("itemIndex"):
            self.itemIDIndex = pickle.load(open("itemIndex", "rb"))
        else:
            self.itemIDIndex = self.createIndex('item_id', self.data)
            pickle.dump(self.itemIDIndex, open("itemIndex", "wb"))
        
        if os.path.exists("priceIndex"):
            self.priceIndex = pickle.load(open("priceIndex", "rb"))
        else:
            self.priceIndex = self.createIndex('price', self.data)
            pickle.dump(self.priceIndex, open("priceIndex", "wb"))
        end = time.time()
        print("Time Taken: ", end - start)

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
        df['created_at'] = pd.to_datetime(df['created_at'])
        return df
    
    def search(self, attribute: str, value: int) -> pd.DataFrame:
        if attribute == 'item_id':
            index = self.itemIDIndex.search(value)
        elif attribute == 'price':
            index = self.priceIndex.search(value)

        if index == None:
            return pd.DataFrame()
        
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
    
    def filter(self, category:str, result: pd.DataFrame):
        return result[result['category_name_1'] == category]
    
    def filterByDate(self, start: str, end: str, result: pd.DataFrame):
        return result[(result['created_at'] >= start) & (result['created_at'] <= end)]
    
    # Intersection of ranged results from two indexes
    def intersection(self, result1: pd.DataFrame, result2: pd.DataFrame) -> pd.DataFrame:
        return pd.merge(result1, result2, on='item_id')
    
    def get_sorted_indices(self, result:pd.DataFrame) -> pd.DataFrame:
        #sort the given result by id
        result = result.sort_values(by=['item_id'])
        return result


if __name__ == "__main__":
    # app = Index('data\Pakistan Largest Ecommerce Dataset.csv')
    app = GUI('data\Pakistan Largest Ecommerce Dataset.csv')
    app.run()