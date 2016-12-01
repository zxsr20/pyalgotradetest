import matplotlib.pyplot as plt;
from matplotlib.pyplot import savefig
import DL2Data


def EquityPlot(data,title='title',file=''):
    data=orderDate(data)
    date=[i[0] for i in data];
    value=[i[1] for i in data];
    fig=plt.figure();
    ax=fig.add_subplot(1,1,1);
    ax.plot(value);
    #ax.bar(0,value);
    #plt.xticks(range(len(value)),date,rotation='45');
    ax.set_title(title);
    #plt.grid(True)
    plt.show();
    #savefig(file+title+".png");

def orderDate(data):
    return sorted(data, key=lambda data: data[0])

if __name__ == '__main__':
    data=[["2015-11-01",20],["2014-12-01",23],["2014-11-03",28],["2014-11-04",15],["2014-11-05",22],["2014-11-06",51]];
    
    #print orderDate(data)
    data=DL2Data.getPriceData()
    EquityPlot(data,title="test",file=r".\\");
    

    
    


