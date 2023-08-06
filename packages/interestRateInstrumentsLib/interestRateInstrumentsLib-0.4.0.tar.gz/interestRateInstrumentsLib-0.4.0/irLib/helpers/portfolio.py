class portfolio:
    """
    1.  Shocking common parts of components like discount curve, any dependence on any 
        object simply by reference the object as an attributes of an instance of portfolio.
    2.  Show cashflow overtime by overseeing every components schedule, any kinds of 
        buy and sell at any time pt. Have to set behavior for received cash flow, like 
        reinvest or idle.
    3.  Sensitivity testing by shocking depended objects as mentioned in step 1, thereby
        calculating greeks as well.
    4.  Scenario testing, similar to 3, just rather than change 1 depended obj, changing > 1.
    """

    def __init__(self, **components):
        self.components = components

    def addComponent(self, component, alias):
        self.components[alias] = component

    def setDependedObjs(self, **objs):
        self.dependedObjs = objs

    # discount curve is just an example of objs one can shock
    def addDependedObj(self, obj, alias):
        self.dependedObjs[alias] = obj

    def calculateNPV(self, valuationDate):
        return sum([component.calculateNPV(valuationDate) for componentAlias, component in self.components.item()])
