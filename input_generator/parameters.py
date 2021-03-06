import os
from enum import Enum
class ReflectiveBoundaries(Enum):
    xMin = "xmin"
    xMax = "xmax"
    yMin = "ymin"
    yMax = "ymax"
    zMin = "zmin"
    zMax = "zmax"

class TransportModelType(Enum):
    Diffusion = "diffusion"
    SAAF = "saaf"

class Standard:
    newHolder = [] 

    def setDiscretization(self, value, limit=None):
        self.fieldAdder("ho spatial discretization",value,limit)
    def setEigenvalueProblem(self, value, limit=None):
        self.fieldAdder("do eigenvalue calculations",value,limit)
    def setFEPolynomialDegree(self, value, limit=None):
        self.fieldAdder("finite element polynomial degree",value,limit)
    def setFirstThermalGroup(self, value, limit=None):
        self.fieldAdder("thermal group boundary",value,limit)
    def setHaveReflectiveBC(self, value, limit=None):
        self.fieldAdder("have reflective boundary",value,limit)
    def setNCells(self, value, limit=None):
        self.fieldAdder("number of cells for x, y, z directions",value,limit)
    def setNEnergyGroups(self, value, limit=None):
        self.fieldAdder("number of groups",value,limit)
    def setOutputFilenameBase(self, value, limit=str):
        self.fieldAdder("output file name base",value,limit)
    def setReflectiveBoundary(self, value, limit=None):
        if isinstance(value,ReflectiveBoundaries):
            self.fieldAdder("reflective boundary names",value.value)
        else:
            print("ERROR: " + str(value) + " is not an accepted value for reflective boundary.")
    def setSpatialDimension(self, value, limit=[1,2,3]):
        self.fieldAdder("problem dimension",value,limit)
    def setSpatialMax(self, value, limit=None):
        self.fieldAdder("x, y, z max values of boundary locations",value,limit)
    def setTransportModel(self, value, limit=None):
        if isinstance(value,TransportModelType):
            self.fieldAdder("transport model",value.value)
        else:
            print("ERROR: " + str(value) + " is not an accepted value for transport model.")

    # Mesh
    def setMeshGenerated(self, value, limit=None):
        self.fieldAdder("is mesh generated by deal.II",value,limit)
    def setMeshFilename(self, value, limit=None):
        self.fieldAdder("mesh file name",value,limit)
    def setUniformRefinements(self, value, limit=None):
        self.fieldAdder("uniform refinements",value,limit)
    def setFuelPinRadius(self, value, limit=None):
        self.fieldAdder("fuel Pin radius",value,limit)
    def setFuelPinTriangulation(self, value, limit=None):
        self.fieldAdder("triangulation type of fuel Pin",value,limit)
    def setMeshPinResolved(self, value, limit=None):
        self.fieldAdder("is mesh pin-resolved",value,limit)

    # Material Parameters
    def setMaterialSubsection(self, value, limit=None):
        self.fieldAdder("material ID map",value,limit)
    def setMaterialMapFilename(self, value, limit=None):
        self.fieldAdder("material id file name",value,limit)
    def setMaterialFilenames(self, value, limit=None):
        self.fieldAdder("material id file name map",value,limit)
    def setNumberOfMaterials(self, value, limit=None):
        self.fieldAdder("number of materials",value,limit)
    def setFuelPinMaterialMapFilename(self, value, limit=None):
        self.fieldAdder("fuel pin material id file name",value,limit)

    # Acceleration Parameters
    def setPreconditioner(self, value, limit=None):
        self.fieldAdder("ho preconditioner name",value,limit)
    def setBSSOR_Factor(self, value, limit=None):
        self.fieldAdder("ho ssor factor",value,limit)
    def setDoNDA(self, value, limit=None):
        self.fieldAdder("do nda",value,limit)
    def setNDA_Discretization(self, value, limit=None):
        self.fieldAdder("nda spatial discretization",value,limit)
    def setNDALinearSolver(self, value, limit=None):
        self.fieldAdder("nda linear solver name",value,limit)
    def setNDAPreconditioner(self, value, limit=None):
        self.fieldAdder("nda preconditioner name",value,limit)
    def setNDA_BSSOR_Factor(self, value, limit=None):
        self.fieldAdder("nda ssor factor",value,limit)

    # Solvers
    def setEigenSolver(self, value, limit=None):
        self.fieldAdder("eigen solver name",value,limit)
    def setInGroupSolver(self, value, limit=None):
        self.fieldAdder("in group solver name",value,limit)
    def setLinearSolver(self, value, limit=None):
        self.fieldAdder("ho linear solver name",value,limit)
    def setMultiGroupSolver(self, value, limit=None):
        self.fieldAdder("mg solver name",value,limit)

    # Angular Quadrature
    def setAngularQuad(self, value, limit=None):
        self.fieldAdder("angular quadrature name",value,limit)
    def setAngularQuadOrder(self, value, limit=None):
        self.fieldAdder("angular quadrature order",value,limit)


    def fieldAdder(self,field,value,limitations=None):
        if limitations:
            if type(limitations) is type and type(value) is not limitations:
                print("ERROR: " + str(value) + " is an invalid type of value for " + field + ".")
                return 
            elif type(limitations) is list and value not in limitations: 
                print("ERROR: " + str(value) + " is not an accepted value for " + field + ".")
                return
        if type(value) is list: # you input a range of values for one 
            currAmount = len(self.newHolder)
            temp = []
            for i in range(currAmount):
                currStatus = self.newHolder[i]
                for j in value:
                    temp.append(currStatus + field + " = " + str(j) + "\n")
            self.newHolder = temp

        else:
            writtenUp = field + " = " + str(value)+"\n"
            if self.newHolder:
                for i in range(len(self.newHolder)):
                    currString = self.newHolder[i] + writtenUp
                    self.newHolder[i] = currString
            else: 
                self.newHolder.append(writtenUp)
    
    def snapshot(self):
        for i in range(len(self.newHolder)):
            print("File " + str(i+1) + "\n")
            print(self.newHolder[i])

    def saveAs(self, pathname): 
        temp = pathname.split("/")
        directories, filename = "/".join(temp[:-1])+"/", temp[-1]
        try:
            os.mkdir(directories)
        except FileExistsError:
            pass
        for i in range(len(self.newHolder)):
            with open(directories+filename+"-"+str(i) + ".input","w") as file:
                file.write(self.newHolder[i])
        print("Files saved to " + pathname)