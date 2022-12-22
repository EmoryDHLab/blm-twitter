import csv
import pandas as pd


def naive_send_to_bin():
    f = open(sys.argv[1],"r")
    ta = csv.reader(f)
    loss = list()
    one = pd.DataFrame(columns = ["tweetid","author","tweet","date"])
    two = pd.DataFrame(columns = ["tweetid","author","tweet","date"])
    three = pd.DataFrame(columns = ["tweetid","author","tweet","date"])
    four = pd.DataFrame(columns = ["tweetid","author","tweet","date"])
    five = pd.DataFrame(columns = ["tweetid","author","tweet","date"])
    six = pd.DataFrame(columns = ["tweetid","author","tweet","date"])
    seven = pd.DataFrame(columns = ["tweetid","author","tweet","date"])
    x = 0
    row = next(ta)
    nextie = next(ta)
    stopping = False
    while not stopping:
        if is_date(row[-1]) and len(row) == 4:
            smoothie = days_since(row[-1])
            if smoothie < 244:
                one.loc[len(one.index)] = row
            elif smoothie < 359:
                two.loc[len(two.index)] = row
            elif smoothie < 607:
                three.loc[len(three.index)] = row
            elif smoothie < 919:
                four.loc[len(four.index)] = row
            elif smoothie < 2338:
                five.loc[len(five.index)] = row
            elif smoothie < 2410:
                six.loc[len(six.index)] = row
            else:
                seven.loc[len(seven.index)] = row
            row = nextie
            try:
                nextie = next(ta)
            except StopIteration:
                print(f"Iterations completed at index {x}. Sorting into bins now.")
                stopping = True
        elif is_date(row[-1]) and len(row) < 4:
            raise ValueError("Row printed incorrectly!\nRow: " + str(row) + "\nNextie: " + str(nextie))
        else:
            if len(nextie) < 1:
                row[-1] += " "
            else:
                row[-1] += nextie[0]
                if len(nextie) == 3:    raise ValueError("Nextie printed incorrectly!")
                if len(nextie) == 2:
                    row.append(nextie[1])
            nextie = next(ta)
        row[-1] = row[-1][:10]
        print(f"Row {x}: {row}")
        x += 1
    f.close()
    print(one.size)
    print(two.size)
    print(three.size)
    print(four.size)
    print(five.size)
    print(six.size)
    print(seven.size)
    with open('./bins/bad_data.csv','w') as lossfile:
        cw = csv.writer(lossfile)
        cw.writerows(loss)
    with open('./bins/0-253.csv','w') as onefile:
        one.to_csv(onefile)
    with open('./bins/244-358.csv','w') as twofile:
        two.to_csv(twofile)
    with open('./bins/359-606.csv', 'w') as threefile:
        three.to_csv(threefile)
    with open('./bins/607-918.csv', 'w') as fourfile:
        four.to_csv(fourfile)
    with open('./bins/919-2337.csv','w') as fivefile:
        five.to_csv(fivefile)
    with open('./bins/2338-2409.csv','w') as sixfile:
        six.to_csv(sixfile)
    with open('./bins/2410-2860.csv','w') as sevenfile:
        seven.to_csv(sevenfile)

naive_send_to_bin()
