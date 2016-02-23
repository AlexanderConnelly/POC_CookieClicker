
"""
Cookie Clicker Simulator
"""


import math

#####################################
#CodeSkulptor Imports Only:
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(20)
#import poc_clicker_provided as provided
######################################

# Constants
SIM_TIME = 10000000000.0


#Cookie Clicker Simulator Build Information


BUILD_GROWTH = 1.15

class BuildInfo:
    """
    Class to track build information.
    """
    
    def __init__(self, build_info = None, growth_factor = BUILD_GROWTH):
        self._build_growth = growth_factor
        if build_info == None:
            self._info = {"Cursor": [15.0, 0.1],
                          "Grandma": [100.0, 0.5],
                          "Farm": [500.0, 4.0],
                          "Factory": [3000.0, 10.0],
                          "Mine": [10000.0, 40.0],
                          "Shipment": [40000.0, 100.0],
                          "Alchemy Lab": [200000.0, 400.0],
                          "Portal": [1666666.0, 6666.0],
                          "Time Machine": [123456789.0, 98765.0],
                          "Antimatter Condenser": [3999999999.0, 999999.0]}
        else:
            self._info = {}
            for key, value in build_info.items():
                self._info[key] = list(value)

        self._items = sorted(self._info.keys())
            
    def build_items(self):
        """
        Get a list of buildable items
        """
        return list(self._items)
            
    def get_cost(self, item):
        """
        Get the current cost of an item
        Will throw a KeyError exception if item is not in the build info.
        """
        return self._info[item][0]
    
    def get_cps(self, item):
        """
        Get the current CPS of an item
        Will throw a KeyError exception if item is not in the build info.
        """
        return self._info[item][1]
    
    def update_item(self, item):
        """
        Update the cost of an item by the growth factor
        Will throw a KeyError exception if item is not in the build info.
        """
        cost, cps = self._info[item]
        self._info[item] = [cost * self._build_growth, cps]
        
    def clone(self):
        """
        Return a clone of this BuildInfo
        """
        return BuildInfo(self._info, self._build_growth)


class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._game_time = 0.0
        self._cps = 1.0
        self._game_history = [(0.0, None, 0.0, 0.0)]
        
        
    def __str__(self):
        """
        Return human readable state
        """
        string = 'Time: ' + str(self._game_time) + ' Current Cookies: ' + str(self._current_cookies) + ' CPS: ' + str(self._cps) + ' Total Cookies: ' + str(self._total_cookies)# + ' History: (length: ' + str(len(self._game_history))+'): '+ str(self._game_history)            
        return string
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._game_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._game_history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        
        #print('cookies requested '+str(cookies))
        if self._current_cookies >= cookies:
            return 0.0
        else:
            seconds_remain = (float(cookies)-(self._current_cookies))/self._cps
            
            return math.ceil(seconds_remain)
        
        
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        #print ('wait time granted ' + str(time))
        if time >0.0:
            self._game_time+=float(time)
            self._current_cookies += (self._cps * float(time))
            self._total_cookies += (self._cps * float(time))
        
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies -= float(cost)
            self._cps += float(additional_cps)
            self._game_history.append((self._game_time,item_name,cost,self._total_cookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    
    cookie_clicker = ClickerState()
    
    builder = build_info
    #Check the current time and break out of the loop if the duration has been passed.
    while cookie_clicker.get_time() <= duration:
        #Call the strategy function with the appropriate arguments to determine which item to purchase next. If the strategy function returns None, 
        #you should break out of the loop, as that means no more items will be purchased. 
        buy_next = strategy(cookie_clicker.get_cookies(),cookie_clicker.get_cps(),cookie_clicker.get_history(),duration - cookie_clicker.get_time(),builder)
        if buy_next == None:
            cookie_clicker.wait(duration)
            break
        #Determine how much time must elapse until it is possible to purchase the item.
        #If you would have to wait past the duration of the simulation to purchase the item, you should end the simulation.
        get_cost = builder.get_cost(buy_next)
        
        get_cps = builder.get_cps(buy_next)
        
        #wait if necessary
        wait_time = cookie_clicker.time_until(get_cost)
        cookie_clicker.wait(wait_time)
        if cookie_clicker.get_cookies() >= get_cost:
            cookie_clicker.buy_item(buy_next,get_cost,get_cps)
            builder.update_item(buy_next)
    #print cookie_clicker._game_history
    return str(cookie_clicker)


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    
    if build_info.get_cost('Cursor') < (cookies + cps*time_left):
        return "Cursor"
    else:
        return None
def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    items = build_info.build_items()
    #find cheapest option and return it
    cheapest = float('Inf')
    cheapest_item = ''
    for item in items:
        print item
        print str(build_info.get_cost(item)) + ' money left' +str(cookies + cps*time_left)
        if build_info.get_cost(item) < cheapest and build_info.get_cost(item) <= (cookies + cps*time_left):
            cheapest = build_info.get_cost(item)
            cheapest_item = item
    if cheapest_item == '':
        cheapest_item = None
    return (cheapest_item)

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    items = build_info.build_items()
    #find cheapest option and return it
    expensive = -1.0
    expensive_item = ''
    for item in items:
       # print item
        if build_info.get_cost(item) > expensive  and build_info.get_cost(item) <= (cookies + cps*time_left):
            expensive = build_info.get_cost(item)
            expensive_item = item
    if expensive_item =='':
        expensive_item = None
    return (expensive_item)
    

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    # return the option with the highest CPS addition/cookie value?
    items = build_info.build_items()
    #find cheapest option and return it
    best_cps = -1.0
    best_option = ''
    for item in items:
        
        
        if build_info.get_cps(item)/build_info.get_cost(item) > best_cps:
            best_cps = build_info.get_cps(item)/build_info.get_cost(item)
            best_option = item
       
    
    return best_option
    
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
print strategy_cheap(2.0, 1.0, [(0.0, None, 0.0, 0.0)], 1.0, BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15)) 
print strategy_expensive(0.0, 1.0, [(0.0, None, 0.0, 0.0)], 5.0, BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15)) 
print simulate_clicker(BuildInfo({'Cursor': [15.0, 0.10000000000000001]}, 1.15), 5000.0,strategy_none)
#a_build = BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15)
#b_build = BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15)
#print strategy_cheap(2.0, 1.0, [(0.0, None, 0.0, 0.0)], 1.0, a_build)
#print strategy_expensive(2.0, 1.0, [(0.0, None, 0.0, 0.0)], 1.0, a_build)
#print a_build.build_items()
#obj = ClickerState()
#obj.wait(45.0)
#obj.buy_item('item', 1.0, 3.5) 
#print obj.time_until(49.0)
#print obj._game_history
