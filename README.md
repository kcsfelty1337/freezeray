icepick.py profides a class, icepick, that contains the following methods:
        toBaseKit(item):
                All of the to'x'Kit methods take a string argument and concats the implied strings so as to query the API for the exact item
        toSpecKit(item):
                All of the to'x'Kit methods take a string argument and concats the implied strings so as to query the API for the exact item
        toProfKit(item):
                All of the to'x'Kit methods take a string argument and concats the implied strings so as to query the API for the exact item
        toSpecfab(item):
                All of the to'x'Kit methods take a string argument and concats the implied strings so as to query the API for the exact item
        toProfFab(item):
                All of the to'x'Kit methods take a string argument and concats the implied strings so as to query the API for the exact item
        getPrice(item):
                Queries a MySQL db for item prices, should be faster than asking the API
        getWeapons():
                Generates a list of all the TF2 weapons on the market, requires a file with the information
        getBackpackItems(steamID):
                Queries API for a what TF2 items a certain 64 bit id holds
        sortDict(data,sorted):
                Takes a dict and sorts by the values (iterates through based on key values), pass boolean true to sort from high to low
        cheapSpecKit():
                Finds the cheapest specialized kit on the market (excludes bad items)
        cheapBasicKit():
                Finds the cheapest basic kit on the market (excludes bad items)
        averagePrice(parts):
                finds the average of a list, could be done without this method but it adds clarity
        costBuildProf():
                Generates cost to build a prof kit
        costBuildSpec():
                Generates cost to build a specialized kit
        profitableProf():
                Builds a list of profitable professional kits (these kits will sell for more than price of fab and parts, accounts for tax)
        profitableSpec():
                Builds a list of profitable specialized kits (these kits will sell for more than price of fab and parts, accounts for tax)
        queryPriceAPI(item):
                Actual method for talking to Steam API, use it if you want a new price immediatley
        updatePrices():
                Runs through ever basic, spec and prof kit and fab as well as robot parts

