import math
import sys
import random

vertices = list()
edges = list()
parents = dict()
list_of_attributes=[]
prob_naive = dict()
prob_tan = dict()
weights = dict()

class Attribute:
    index = 0
    values = list()
    def __init__(self):
        self.setName("")
        self.setType("")
    def __str__(self):
        return str(self.Name)
    def setName(self, val):
        self.Name = val
    def setType(self, val):
        self.Type = val
    def setValues(self, val):
        self.values = val
    def getName(self):
        return str(self.Name)
    def getType(self):
        return str(self.Type)
    def getIndex(self):
        return self.index
    
    
def readArff(filename):
    global list_of_attributes
    arrfFile = open(filename)
    lines = [line.rstrip('\n') for line in arrfFile]
    data = [[]]
    index = 0
    for line in lines :
        if(line.startswith('@attribute')) :
            attributeLine = line
            attributeLineSplit = attributeLine.split(' ',2)
            #print(attributeLineSplit[0]," ",attributeLineSplit[1]," ",attributeLineSplit[2])
            if "{" not in attributeLineSplit[2] :
                #print("Real Value")
                attr = Attribute()
                attr.setName(attributeLineSplit[1].replace('\'',''))
                attr.setType("real")
                attr.index = index
                list_of_attributes.append(attr)
            else : 
                attr = Attribute()
                attr.setName(attributeLineSplit[1].replace('\'',''))
                #print(attributeLineSplit[1].replace('\'',''))
                attr.setType("class")
                attr.index = index
                #print(index)
                attributeValueList = attributeLineSplit[2].replace('{',"")
                attributeValueList = attributeValueList.replace('}',"")
                attributeValues = [x.strip(" ") for x in attributeValueList.split(",")]
                #print(attributeValues)
                attr.setValues(attributeValues)
                list_of_attributes.append(attr)
                #print(list_of_attributes[0])
                #print(attr.getName," ",attr.getIndex," ",attr.getType)
            index+=1
        elif(not line.startswith('@data') and not line.startswith('@relation') and not line.startswith('%')) :
            data.append(line.split(','))
    del data[0]
    #print(data)
    return data

def readTestArff(filename):
    arrfFile = open(filename)
    lines = [line.rstrip('\n') for line in arrfFile]
    data = [[]]
    index = 0
    for line in lines :
        if(line.startswith('@attribute')) :
            index+=1
        elif(not line.startswith('@data') and not line.startswith('@relation') and not line.startswith('%')) :
            data.append(line.split(','))
    del data[0]
    return data

def getInstances(attributeIndex, attributeValue):
    count = 0
    for line in data : 
        if(line[attributeIndex]==attributeValue) :
            count+=1
    return count
            
    
def getInstancesConditional(attribute1Index, attribute1Value, attribute2Index, attribute2Value):
    global data
    count = 0
    for line in data :
        if(line[attribute1Index] == attribute1Value and line[attribute2Index] == attribute2Value) :
            count+=1
    return count

def getInstancesConditionalTAN(attribute1Index, attribute1Value, attribute2Index, attribute2Value, attribute3Index, attribute3Value):
    global data
    count = 0
    for line in data :
        if(line[attribute1Index] == attribute1Value and line[attribute2Index] == attribute2Value
           and line[attribute3Index] == attribute3Value) :
            count+=1
    return count

def getProbability(instance_count, total_instances):
    return float(instance_count)/total_instances

def calculateProbabilitiesForNB():
    global data
    global list_of_attributes
    global prob_naive
    y1 = list_of_attributes[-1].values[0]
    y2 = list_of_attributes[-1].values[1]
    no_of_y1 = getInstances(len(list_of_attributes)-1, y1)
    no_of_y2 = getInstances(len(list_of_attributes)-1, y2)
    p_of_y1 = getProbability(no_of_y1+1, len(data)+2)
    p_of_y2 = getProbability(no_of_y2+1, len(data)+2)
    prob_naive[y1] = p_of_y1
    prob_naive[y2] = p_of_y2
    countList = list()
    for attr in list_of_attributes :
        totalCount1 = 0
        for value in attr.values :
            n1 = getInstancesConditional(attr.getIndex(), value, len(list_of_attributes)-1, y1)
            n2 = getInstancesConditional(attr.getIndex(), value, len(list_of_attributes)-1, y2)
            countList.append([value,n1+1,n2+1])
            totalCount1+=1
        for c in countList :
            p_of_x_y1 = getProbability(c[1], no_of_y1+totalCount1)
            p_of_x_y2 = getProbability(c[2], no_of_y2+totalCount1)
            index1 = attr.Name+"="+c[0]+"|"+y1
            prob_naive[index1] = p_of_x_y1
            index2 = attr.Name+"="+c[0]+"|"+y2
            prob_naive[index2] = p_of_x_y2
        countList = list()
            

def naiveBayes():
    global data
    global test_data
    global prob_naive
    calculateProbabilitiesForNB()
    for attr in list_of_attributes :
        if(attr.index == len(list_of_attributes)-1):
            print ""
            break
        print attr.Name + "" + list_of_attributes[-1].Name
    y1 = list_of_attributes[-1].values[0]
    y2 = list_of_attributes[-1].values[1]
    correctClassified = 0
    incorrectlyClassified = 0
    for line in test_data :
        numerator = prob_naive[y1]
        #print(numerator)
        denominator = prob_naive[y2]
        #print(denominator)
        index = 0
        for l in line :
            if(index==len(list_of_attributes)-1):
                break
            keyString1 = list_of_attributes[index].Name+"="+l+"|"+y1
            numerator*= prob_naive[y1]
            keyString2 = list_of_attributes[index].Name+"="+l+"|"+y2
            denominator*= prob_naive[y2]
            index+=1
        p_of_y1_line = getProbability(numerator, numerator+denominator)
        p_of_y2_line = getProbability(denominator, numerator+denominator)
        if(p_of_y2_line > p_of_y1_line):
            print y2 + " "+line[-1] + " ",
            print("%.16f" % p_of_y2_line)
            if(y2 == line[-1]):
                correctClassified+=1
            else :
                incorrectlyClassified+=1
        else :
            print y1 + " "+line[-1] + " ",
            print("%.16f" % p_of_y1_line)
            if(y1 == line[-1]):
                correctClassified+=1
            else : 
                incorrectlyClassified+=1
    print ""
    #print correctClassified
    print("y1",y1)
    print("y2",y2)
    print ("Correctly Classified",correctClassified)
    print("Total Test Data", correctClassified+incorrectlyClassified)
    print("Accuracy",float(correctClassified)/(correctClassified+incorrectlyClassified))
    return float(correctClassified)/(incorrectlyClassified+correctClassified) 



def computeWeights():
    global data
    global list_of_attributes
    global weights
    global prob_naive
    y1 = list_of_attributes[-1].values[0]
    y2 = list_of_attributes[-1].values[1]
    no_of_y1 = getInstances(len(list_of_attributes)-1, y1)
    no_of_y2 = getInstances(len(list_of_attributes)-1, y2)
    summation = 0
    #print(list_of_attributes)
    #print(len(data))
    for attr1 in list_of_attributes :
        if(attr1.index == len(list_of_attributes)-1):
            continue
        for attr2 in list_of_attributes :
            if(attr2.index == len(list_of_attributes)-1):
                continue
            if(attr1.Name == attr2.Name):
                continue
            else :
                for value1 in attr1.values :
                    for value2 in attr2.values :
                        no_x1_x2_y1 = getInstancesConditionalTAN(attr1.index, value1, attr2.index, value2, len(list_of_attributes)-1, y1)
                        p_no_x1_x2_y1 = getProbability(no_x1_x2_y1+1,len(data) + (len(attr1.values)*len(attr2.values)*2)) 
                        p_x1_x2_given_y1 = getProbability(no_x1_x2_y1+1,no_of_y1 + (len(attr1.values)*len(attr2.values)))
                        
                        no_x1_x2_y2 = getInstancesConditionalTAN(attr1.index, value1, attr2.index, value2, len(list_of_attributes)-1, y2)
                        p_no_x1_x2_y2 = getProbability(no_x1_x2_y2+1,len(data) + (len(attr1.values)*len(attr2.values)*2))
                        p_x1_x2_given_y2 = getProbability(no_x1_x2_y2+1,no_of_y2 + (len(attr1.values)*len(attr2.values)))
                         
                        keyIndex = attr1.Name+"="+value1+"|"+y1
                        p_x1_y1 = prob_naive[keyIndex]
                        keyIndex = attr2.Name+"="+value2+"|"+y2
                        p_x2_y2 = prob_naive[keyIndex]
                        keyIndex = attr1.Name+"="+value1+"|"+y2
                        p_x1_y2 = prob_naive[keyIndex]
                        keyIndex = attr2.Name+"="+value2+"|"+y1
                        p_x2_y1 = prob_naive[keyIndex]
                        
                        sum1 = p_no_x1_x2_y1 * math.log(float(p_x1_x2_given_y1)/(p_x1_y1*p_x2_y1),2)
                        sum2 = p_no_x1_x2_y2 * math.log(float(p_x1_x2_given_y2)/(p_x1_y2*p_x2_y2),2)
                        summation+=sum1+sum2
                keyString = attr1.Name+","+attr2.Name+"|Y"
                weights[keyString] = summation
                summation = 0

def getMaximumWeightEdge(vertices):
    weight_list = list()
    for v in vertices :
        for attr in list_of_attributes :
            if(attr.Name == v.Name or attr.Name=="class" or v.Name=="class" or attr.Name=="Class" or v.Name=="Class"):
                continue
            indexStr = v.Name+","+attr.Name+"|Y"
            #print(indexStr)
            if(attr not in vertices) :
                weight_list.append([weights[indexStr], v, attr])
    weight_list.sort(key=lambda x: x[0])
    for w in weight_list:
          highest_weight = weight_list[-1][0]
    for w in weight_list :
        if(w[0] == highest_weight):
            return w

def prims():
    global vertices
    global edges
    global parents
    vertices.append(list_of_attributes[0])
    
    while(len(vertices)<len(list_of_attributes)-1):
        edge = getMaximumWeightEdge(vertices)
        print(edge[0])
        vertices.append(edge[2])
        edges.append(edge)
        parents[edge[2].Name] = edge[1]
    for attr in list_of_attributes : 
        if(attr.Name.lower()=="class"):
            print ""
            break
        if(parents.has_key(attr.Name)):
            print attr.Name+ " " + parents[attr.Name].Name+ " "+ list_of_attributes[-1].Name+" harsh1"
        else  :
            print attr.Name+ " " + list_of_attributes[-1].Name+" harsh2"

def calculateProbabilitiesForTAN():
    y1 = list_of_attributes[-1].values[0]
    y2 = list_of_attributes[-1].values[1]
    #print(y1)
    #print(y2)
    for attr in list_of_attributes :
        for value1 in attr.values : 
            if(parents.has_key(attr.Name)):
                parent_of_x = parents[attr.Name]
                for value2 in parent_of_x.values :
                    no_x1_parentx1_y1 = getInstancesConditionalTAN(attr.index,value1, parent_of_x.index, value2, len(list_of_attributes)-1, y1)
                    no_x1_parentx1_y2 = getInstancesConditionalTAN(attr.index,value1, parent_of_x.index, value2, len(list_of_attributes)-1, y2)
                    no_parentx1_y1 = getInstancesConditional(parent_of_x.index, value2, len(list_of_attributes)-1, y1)
                    no_parentx1_y2 = getInstancesConditional(parent_of_x.index, value2, len(list_of_attributes)-1, y2)
                    p_x1_given_parentx1_y1 = getProbability(no_x1_parentx1_y1+1, no_parentx1_y1+len(attr.values))
                    indexString = attr.Name+"="+value1+"|"+parent_of_x.Name+"="+value2+",Y="+y1
                    #print(indexString)
                    prob_tan[indexString] = p_x1_given_parentx1_y1
                    p_x1_given_parentx1_y2 = getProbability(no_x1_parentx1_y2+1, no_parentx1_y2+len(attr.values))
                    indexString = attr.Name+"="+value1+"|"+parent_of_x.Name+"="+value2+",Y="+y2
                    #print(indexString)
                    prob_tan[indexString] = p_x1_given_parentx1_y2
        
def tan():
    global data
    global list_of_attributes
    global prob_naive
    #print("888888",list_of_attributes)
    #print(list_of_attributes[0].Name)
    y1 = list_of_attributes[-1].values[0]
    print(y1)
    y2 = list_of_attributes[-1].values[1]
    print(y2)
    calculateProbabilitiesForNB()
    computeWeights()
    prims()
    calculateProbabilitiesForTAN()
    correctClassified=0
    incorrectlyClassified=0
    true_p=0
    true_n=0
    false_p=0
    false_n=0
    for line in test_data : 
        numerator = prob_naive[y1]
        denominator = prob_naive[y2]
        index = 0
        for l in line :
            if(index==len(list_of_attributes)-1):
                break
            if(parents.has_key(list_of_attributes[index].Name)):
                parent = parents[list_of_attributes[index].Name]
                parent_value = line[parent.index]
                key1 = list_of_attributes[index].Name+"="+l+"|"+parent.Name+"="+parent_value+",Y="+y1
                key2 = list_of_attributes[index].Name+"="+l+"|"+parent.Name+"="+parent_value+",Y="+y2
                numerator*=prob_tan[key1]
                #print(prob_tan[key1])
                denominator*=prob_tan[key2]
            else :
                #key1 = list_of_attributes[index].Name+"="+l+"|"+y1
                #print(key1)
                #key2 = list_of_attributes[index].Name+"="+l+"|"+y2
                #print(key2)
                numerator*=prob_naive[y1]
                denominator*=prob_naive[y2]
            index+=1
        p_of_y1_x = getProbability(numerator, numerator+denominator)
        p_of_y2_x = getProbability(denominator, numerator+denominator)
        
        if(p_of_y1_x >=p_of_y2_x):
            print y1+" "+line[-1]+ " ",
            print("%.16f" % p_of_y1_x)
            if(line[-1]==0):
            	true_n+=1
            else:
            	false_n+=1
            if(y1==line[-1]):
                correctClassified+=1
            else : 
                incorrectlyClassified +=1
        else :
            print y2+" "+line[-1]+ " ",
            print("%.16f" % p_of_y2_x)
            if(line[-1]==1):
            	true_n+=1
            else:
            	false_n+=1
            if(y2==line[-1]):
                correctClassified+=1
            else : 
                incorrectlyClassified +=1
    
    
    print ""
    print ("Correctly Classified",correctClassified)
    print("Total Test Data", correctClassified+incorrectlyClassified)
    print("Accuracy",float(correctClassified)/(correctClassified+incorrectlyClassified))
    return float(correctClassified)/(correctClassified+incorrectlyClassified)
        
        
        
def learningCurve():
    global data
    global test_data
    listOfSampleSizes = [100]
    list1 = random.sample(data,50)
    data = list1
    print naiveBayes()
    #print accuracy1
    

def main():
    global data
    global test_data
    trainingSet = sys.argv[1]
    testSet = sys.argv[2]
    learningType = sys.argv[3]
    data = readArff(trainingSet)
    #print data
    test_data = readTestArff(testSet)
    #print test_data	
    if(learningType == "n"):  
        naiveBayes()
    elif(learningType == "t"):
        tan()
            
main()
