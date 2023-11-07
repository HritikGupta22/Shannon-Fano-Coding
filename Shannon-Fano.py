from math import log2
import sys
class ShannonFanoCoder:
    def _getUniqueChar(self,Sample_String:str):
        unique=[]
        for i in Sample_String:
            if i not in unique:
                unique.append(i)
        return unique
    def _getCharFreq(self,Sample_String:str):
        unique=self._getUniqueChar(Sample_String)
        self.FrequencyMap=[]
        for i in unique:
            self.FrequencyMap.append([i,Sample_String.count(i),Sample_String.count(i)/len(Sample_String),""])
        return self.FrequencyMap
    def _partition(self,Start:int,End:int):
        if(Start+1==End):
            return
        PrefixSum=[self.FrequencyMap[Start][1]]
        Delta=[]
        for i in range(1,End-Start):
            PrefixSum.append(PrefixSum[i-1]+self.FrequencyMap[i+Start][1])
        SuffixSum=[PrefixSum[len(PrefixSum)-1]]
        for i in  range(1,End-Start):
            SuffixSum.append(SuffixSum[i-1]-self.FrequencyMap[i-1+Start][1])
        for i in range(0,len(PrefixSum)):
            if(i==len(PrefixSum)-1):
                Delta.append(PrefixSum[i])
                break
            Delta.append(abs(PrefixSum[i]-SuffixSum[i+1]))
        part=Delta.index(min(Delta))
        for i in range(Start,Start+part+1):
            self.FrequencyMap[i][3]+="0"
        for i in range(Start+part+1,End):
            self.FrequencyMap[i][3]+="1"
        self._partition(Start,Start+part+1)
        self._partition(Start+part+1,End)
    def __init__(self,Sample_String) -> None:
        self.FrequencyMap=[]
        self._getCharFreq(Sample_String)
        self.FrequencyMap=sorted(self.FrequencyMap,key=lambda x: x[1],reverse=True)
        self._partition(0,len(self.FrequencyMap))
    def getAvgLength(self)->float:
        avgL=0
        for i in self.FrequencyMap:
            avgL+=i[2]*len(i[3])
        return avgL
    def getEntropy(self)->float:
        Hx=0
        for i in self.FrequencyMap:
            Hx+=-1*i[2]*log2(i[2])
        return Hx
    def getCode(self,Char):
        for i in self.FrequencyMap:
            if(i[0]==Char):
                return i[3]


                
class UserInterface:
    def __init__(self,filename) -> None:
        f=open(filename,'r')
        self.filename=filename
        self.Sample_String=f.read()
        f.close()
        self.sfc=ShannonFanoCoder(self.Sample_String)
    def display(self)->None:
        print("Shannon Fano Coding\n")
        print("This Program encodes a text file using this technique to minimize the number of bits used for encoding.\n")
        print("Character Count- ",len(self.Sample_String),'\n')
        print("Symbol Count- ",len(self.sfc.FrequencyMap),'\n')
        print("S.no.\tSymbol\tOccurence\tProbability\tCodeword\tlength of codeword\n")
        for i in range(0,len(self.sfc.FrequencyMap)):
            print(i,'.\t',self.sfc.FrequencyMap[i][0],'\t  ',end="")
            print(self.sfc.FrequencyMap[i][1],'\t\t ',end="")
            print("{:.4f}".format(self.sfc.FrequencyMap[i][2]),'\t',end="")
            print(self.sfc.FrequencyMap[i][3],'\t\t',end="")
            print(len(self.sfc.FrequencyMap[i][3]),'\n',end="")
        print('---------------------------------------------\n')
        print("Average word length ","{:.3f}".format(self.sfc.getAvgLength()),'\n')
        print("Entropy ","{:.3f}".format(self.sfc.getEntropy()),'\n')
        print("Efficiency ","{:.3f}%".format((100*self.sfc.getEntropy())/self.sfc.getAvgLength()),'\n')
        print("Redundancy ","{:.3f}%".format(100-((100*self.sfc.getEntropy())/self.sfc.getAvgLength())),'\n')
        print('---------------------------------------------\n')
        print("Bits required for ASCII coding: ",len(self.Sample_String)*8,'\n')
        print("Bits required Now: ","{:.3f}".format(self.sfc.getAvgLength()*len(self.Sample_String)),'\n')
        print("Percentage compression: ","{:.3f}%".format((8-self.sfc.getAvgLength())/0.08),'\n')
        return
ui=UserInterface(sys.argv[1])
ui.display()
        


