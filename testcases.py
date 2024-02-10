import os

os.system("echo GET_MERCHANT 100120 | nc 34.125.204.13 3389") # for retrieval 

os.system("echo ADD_MERCHANTS 100120 4 | nc 34.125.204.13 8080") # for adding 4 new merchants to a pincode
os.system("echo ADD_NEW_MERCHANT c1808474-f7cc-4728-b4dd-bcd554badb30 100120 100122 | nc 34.125.204.13 8080") # for adding a merchant that services given pincodes
os.system("echo REMOVE_MERCHANTS 100120 c1808474-f7cc-4728-b4dd-bcd554badb30 | nc 34.125.204.13 8080") #for removing merchants from a particular pincode