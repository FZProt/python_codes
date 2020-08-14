import math
import collections, operator
from collections import OrderedDict

def predicted_burst_calc(burst_lengths, alpha,id):
    predicted_bursts = list()
    #predicted_bursts.append(id)
    predicted_burst=id
    for i in range(len(burst_lengths)):
        predicted_burst = alpha*burst_lengths[i]+(1-alpha)*predicted_burst
        predicted_bursts.append(int(math.ceil(predicted_burst)))
    print("predicted_burst: ",predicted_bursts)
    return predicted_bursts


def sjf(dictOfPredictedBursts):
    print("\na. SJF [All processes arrive at 0]:")
    initial_time=0
    sorted_dict = dict(sorted(dictOfPredictedBursts.items()))
    #print(sorted_dict)
    sequence=[]
    for key,value in sorted_dict.items():
        sequence.append(value+1)
    print("- Sequence: ", sequence)
    time=initial_time
    total=0
    intervals=[0]
    for key,value in sorted_dict.items():
        total=total+time
        time = time + key
        intervals.append(time)
    print("- Intervals: ", intervals)
    avg = total/len(sorted_dict)
    print("- Average Waiting Time: ", avg)


def srtf(arrivals, predicted_bursts):
    bursts=predicted_bursts.copy()
    a=0
    sequence=[]
    intervals=[]
    last_left=[]
    current=arrivals.index(min(arrivals))+1
    for i in range(len(bursts)):
        last_left.append(0)
    wt=0
    while not (all(elem == 10000 for elem in bursts)):
        if a in arrivals:
            intervals.append(a)
            last_left[current-1]=a
            current = arrivals.index(a)+1
            sequence.append(current)
            if last_left[current-1]!=0:
                wt=wt+(a-last_left[current-1])
            bursts[current-1]= bursts[current-1]-1

        elif bursts[current-1]==0:
            intervals.append(a)
            bursts[current-1]=10000
            if not (all(elem == 10000 for elem in bursts)):
                current=bursts.index(min(bursts))+1
                sequence.append(current)
                if last_left[current-1]!=0:
                    wt=wt+(a-last_left[current-1])
                bursts[current-1]= bursts[current-1]-1

        else:
            bursts[current-1]= bursts[current-1]-1
        a=a+1

    avg=wt/len(arrivals)
    print("\nb. SRTF:")
    print("Process sequence: ", sequence)
    print("Process intervals: ", intervals)
    print("Average WT: ",avg)


def pps(arrivals, priority, predicted_bursts):
    bursts=predicted_bursts.copy()
    a=0
    sequence=[]
    intervals=[]
    last_left=[]
    waiting=[]
    current=arrivals.index(min(arrivals))+1
    for i in range(len(bursts)):
        last_left.append(0)
    wt=0
    for i in range(len(bursts)):
        waiting.append(1000)
    #print("hiiiiii",bursts)
    while not (all(elem == 10000 for elem in bursts)):
        #print("innnn")
        if a in arrivals:
            arrived = arrivals.index(a)
            waiting[arrived]=priority[arrived]
            if waiting.index(min(waiting))==arrived:
                last_left[current-1]=a
                current=arrived+1
                intervals.append(a)
                sequence.append(current)
                if last_left[current-1]!=0:
                    wt=wt+(a-last_left[current-1])
            last_left[arrived]=a
            bursts[current-1]= bursts[current-1]-1

        elif bursts[current-1]==0:
            intervals.append(a)
            bursts[current-1]=10000
            waiting[current-1]=10000
            if not (all(elem == 10000 for elem in bursts)):
                current=waiting.index(min(waiting))+1
                sequence.append(current)
                if last_left[current-1]!=0:
                    wt=wt+(a-last_left[current-1])
                bursts[current-1]= bursts[current-1]-1
        else:
            bursts[current-1]= bursts[current-1]-1
        a=a+1
    avg=wt/len(arrivals)
    print("\nb. PPS:")
    print("Process sequence: ", sequence)
    print("Process intervals: ", intervals)
    print("Average WT: ",avg)


def rr(burst_lengths, predicted_bursts):
    bursts=predicted_bursts.copy()
    Q = round(0.5*bursts[0]+0.5*burst_lengths[0])
    a=0
    sequence=[]
    intervals=[0]
    last_left=[]
    current=1
    for i in range(len(bursts)):
        last_left.append(0)
    wt=0
    while not (all(elem == 10000 for elem in bursts)):
        if current>len(bursts):
            current=1
        if bursts[current-1]==10000:
            current=current+1
        else:
            wt=wt+a-last_left[current-1]
            if bursts[current-1]-Q >0:
                bursts[current-1]= bursts[current-1]-Q
                a=a+Q
                last_left[current-1]=a

            elif bursts[current-1]-Q ==0:
                bursts[current-1]==10000
                a=a+Q

            else:
                a=a+bursts[current-1]
                bursts[current-1]=10000
            sequence.append(current)
            current=current+1
            intervals.append(a)

    avg=wt/len(bursts)
    print("\nd. RR [All processes arrive at 0]:")
    print("- Quantum (Q): ", Q)
    print("- Sequence: ", sequence)
    print("- Intervals: ", intervals)
    print("- Average Waiting Time: ", avg)


def main():
    id = int(input("Enter id: "))
    burst_lengths = [int(i) for i in input("Given CPU burst: ").split()]
    arrivals = [int(i) for i in input("Arrival times: ").split()]
    priority = [int(i) for i in input("Process priority: ").split()]
    alpha = 0.5
    predicted_bursts = list()
    predicted_bursts=predicted_burst_calc(burst_lengths, alpha,id)
    dictOfPredictedBursts = {predicted_bursts[i] : i for i in range(len(predicted_bursts))}

    sjf(dictOfPredictedBursts)
    srtf(arrivals, predicted_bursts)
    pps(arrivals, priority, predicted_bursts)
    rr(burst_lengths, predicted_bursts)


if __name__ == "__main__":
    main()
