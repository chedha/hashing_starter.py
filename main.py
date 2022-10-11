# Demonstrate DIY hashing implmenentation

import json
from collections import namedtuple
import time
import sys

# TABLE_SIZE should be a prime number, see:
# https://medium.com/swlh/why-should-the-length-of-your-hash-table-be-a-prime-number-760ec65a75d1
# for a list of prime numbers, please see:
# https://en.wikipedia.org/wiki/List_of_prime_numbers#The_first_1000_prime_numbers
TABLE_SIZE = 4201


# One bucket in a hash table
class Bucket():

    def __init__(self, key_str, val_str):
        self.key = key_str
        self.val = val_str

    def print_me( self):
        print("key=" + self.key + "," + "val=" + self.val)


# holds all the buckets
class Hash_table():

    def __init__(self, n_items):
        self.name = "My Hash Table"
        self.n_buckets = n_items
        self.bucket_list = [Bucket("", "") for i in range(self.n_buckets)]
        self.collisions = 0
        self.keyCount = 0
        self.comparisons = 0

    def isFull(self):
      if self.keyCount == self.n_buckets:
        return True
      else:
        return False

    # Convenience dump for debugging
    def print_hash_table( self, start, limit ):

        for i in range( start, start+limit):
            self.bucket_list[i].print_me( )
            
    # This is the actual hashing function   
    # Fill this in with the function of your choice,  See zyBook
    def compute_hash_bucket(self, key_str):
        return int(key_str) % self.n_buckets

    # Quadratic Probe method to resolve collisions
    def quadraticProbe(self, key_str, position):
      posFound = False

      limit = 20000
      i = 1

      while i <= limit:
        # quadratic probe
        newPosition = position + i + (i**2)
        newPosition = newPosition % self.n_buckets
        # if newPosition is empty then break and return new position
        if self.bucket_list[newPosition].key == "":
          posFound = True
          break
        else:
          # increase i if position is not empty
          i += 1
      return posFound, newPosition

    def quadraticInsert(self, key_str, val_str):
      
      Bucket(key_str, val_str)

      isStored = False

      position = self.compute_hash_bucket(key_str)

      #check to see if position is empty

      if self.bucket_list[position].key == "":
        self.bucket_list[position] = Bucket(key_str, val_str)
        isStored = True
        self.keyCount += 1
        if self.keyCount == self.n_buckets:
          return isStored

      #if collision has occured
      else:
        self.collisions += 1
        isStored, position = self.quadraticProbe(key_str, position)
        if isStored:
          self.bucket_list[position] = Bucket(key_str, val_str)
          isStored = True
          self.keyCount += 1
          
      return isStored

    # Based on ZyBook, 4.3.4
    # code your own insert method here
    # insert resolving collisions by linear probin
    def linearInsert(self, key_str, val_str):
      
      Bucket(key_str, val_str)
            
      isStored = False

      position = self.compute_hash_bucket(key_str)

      #check to see if position is empty

      if self.bucket_list[position].key == "":
        self.bucket_list[position] = Bucket(key_str, val_str)
        isStored = True
        self.keyCount += 1
        if self.keyCount == self.n_buckets:
          return isStored

      #if collision has occured
      
      else:
      #  print(self.keyCount)
        if self.keyCount == self.n_buckets:
          return isStored
        while (self.bucket_list[position].key != ""):
          position += 1
          self.collisions += 1
          if position >= self.n_buckets:
            position = 0
     
      #  print(position)   
        self.bucket_list[position] = Bucket(key_str, val_str)
        isStored = True
        self.keyCount += 1
        
      
      return isStored   
      
    # Based on ZyBook, 4.3.8
    # search a hash table for a value, using linear probing
    # Code your own search method here -- remember 
    # that if you are probing you search method must be able 
    # to probe using the same algorith as your insert()
    def search_linear (self, key_str):
      isFound = False

      position = self.compute_hash_bucket(key_str)

      if self.bucket_list[position].key == key_str:
        return self.bucket_list[position]
        isFound = True

      else:
        temp = position - 1

        while (position < self.n_buckets):
          if self.bucket_list[position].key != key_str:
            position += 1
            self.comparisons += 1
          else:
            return self.bucket_list[position]

        position = temp

        while position >= 0:
          if self.bucket_list[position].key != key_str:
            position -= 1
            self.comparisons += 1
          else:
            return self.bucket_list[position]

      if not isFound:
        return "Key not found"

    

      

# 
# Utility functions
#
        
# Convert json dictionary into a a list of objects
# based on: https://pynative.com/python-convert-json-data-into-custom-python-object/
#
# These are the same and in the earlier list project
def custom_json_decoder(c_name, inDict):
    createdClass = namedtuple(c_name, inDict.keys())(*inDict.values())
    return createdClass


# Load and parse the JSON files
# create a list of objects from the specified JSON file
def load_lynx_json(c_name, f_name):
    with open(f_name, 'r') as fp:
        #Load the JSON
        json_dict = json.load(fp)
        object_list = []
        for i in range(len(json_dict)):
            tmp = custom_json_decoder(c_name, json_dict[i])
            object_list.append(tmp)
        return object_list


# 
# main starts here
#
def main():
    # Load the stops from json
    # assuming you are using Lynx stops
    master_stops_list = load_lynx_json('Stops', "stops.json")
    

    # create the (initial) hash table
    the_hash_table = Hash_table(TABLE_SIZE)
    

    # hash the stops using stop_code as key and stop__name as the stored value
    #for this_stop in master_stops_list:
    #  the_hash_table.insert(this_stop.code, this_stop.name)
  
    sucessful_inserts = 0
    stops_processed = 0

    # get time in nanoseconds -- maybe OS-specific?
    # See https://docs.python.org/3/library/time.html
    t0 = time.perf_counter_ns() 
    
    for this_stop in master_stops_list:
        stops_processed = stops_processed + 1
        if the_hash_table.linearInsert(this_stop.code, this_stop.name) == True:
            sucessful_inserts = sucessful_inserts + 1
    t1 = time.perf_counter_ns() - t0
    
    print( "Elapsed insert time = " + str(t1 ))

    print("stops_processed = " + str(stops_processed))
    print("sucessful_inserts = " + str(sucessful_inserts))
    print( "collisions = " + str(the_hash_table.collisions ))
    print( "Key count = " + str(the_hash_table.keyCount ))

    print()

    # Your test and debug code here...
    the_hash_table.print_hash_table(20, 10)
  
    print()
  
    t0 = time.perf_counter_ns()
    test_stop = the_hash_table.search_linear("1287")
    t1 = time.perf_counter_ns() - t0
  
    if test_stop == "Key not found":
      print("Key not found")
    else:
      print("test_stop = " + test_stop.val)
    print( "Elapsed search time = " + str(t1 ))
    
    

if __name__ == "__main__":
    main()
