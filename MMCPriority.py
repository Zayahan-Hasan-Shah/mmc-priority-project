import math
import random
from decimal import *
from texttable import Texttable
from patient import *
import csv
from tkinter import filedialog
import tkinter as tk

root=tk.Tk()
root.configure(bg="lightblue")
root.geometry("460x460")
root.resizable(False,False)

title=root.title("MMC Priority")

font_style = ("Helvetica", 12, "bold")
arr = tk.Label(root, text = "Arrival Rate", background=root.cget('bg'), highlightthickness=0, foreground="white", font=font_style).place(x = 110,y = 90)
ser = tk.Label(root, text = "Service Rate", background=root.cget('bg'), highlightthickness=0, foreground="white", font=font_style).place(x = 110,y = 130)

MA = tk.StringVar()
MS = tk.StringVar()

mSN=tk.Entry(root, textvariable = MS)
mSN.place(x = 230,y = 90)

mAN= tk.Entry(root, textvariable = MA)
mAN.place(x = 230,y = 130)


def code():  
    
    def getArrivalTimes(meanArrivalNumber):
        
        cumulativeProbability = 0
        cumulativeProbabilities = []
        x = 0
        while cumulativeProbability < 1.0:
            with localcontext() as ctx:
                ctx.prec = 5
                newValue = (Decimal(math.exp(-meanArrivalNumber))*ctx.power(Decimal(meanArrivalNumber),x)) / math.factorial(x)
                cumulativeProbability += newValue
                cumulativeProbabilities.append(float(cumulativeProbability))
            x += 1

        cpLookUp = [0]
        for i in range(len(cumulativeProbabilities) - 1):
            cpLookUp.append(cumulativeProbabilities[i])

        averageTimes = [i for i in range(len(cumulativeProbabilities))]

        interArrivals = []
        for i in range(len(cumulativeProbabilities)):
            randomNumber = random.random()
            for j in range(len(cumulativeProbabilities)):
                item = cumulativeProbabilities[j]
                if randomNumber < item:
                    interArrivals.append(j)
                    break
        # arrival time
        arrivalTimes = [interArrivals[0]]
        for i in range(1, len(interArrivals)):
            arrivalTimes.append(arrivalTimes[i - 1] + interArrivals[i])
        return {
            "cumulativeProbabilities": cumulativeProbabilities,
            "cpLookUp": cpLookUp,
            "averageTimes": averageTimes,
            "interArrivals": interArrivals,
            "arrivalTimes": arrivalTimes
        }
        
    # service time
    def getServiceTimes(length, meanServiceNumber):
        serviceTimes = []
        for i in range(length):
            serviceTime = -meanServiceNumber * math.log(random.random())
            serviceTimes.append(round(math.ceil(serviceTime)))
        return serviceTimes

    # priority
    def getPriorities(length, A, M, Z, C, a, b):
        priorities = []
        for i in range(length):
            R = (A * Z + C) % M
            S = R / M
            Y = round((b - a) * S + a)
            priorities.append(Y)
            Z = R
        return priorities

    def display(arrivalTimes, serviceTimes, priorities):
        table = Texttable()
        table.set_precision(5)
        tableRows = [["S. No.", "Cumulative Probabilities", "CP Lookup", "Average Times", "Inter Arrivals", "Arrival Times", "Service Times", "Priorities"]]
        for i in range((len(arrivalTimes['arrivalTimes']))):
            newRow = [
                i+1, 
                arrivalTimes["cumulativeProbabilities"][i],
                arrivalTimes["cpLookUp"][i],
                arrivalTimes["averageTimes"][i],
                arrivalTimes["interArrivals"][i],
                arrivalTimes["arrivalTimes"][i],
                serviceTimes[i],
                priorities[i]
            ]
            tableRows.append(newRow)
        table.add_rows(tableRows)
        table.set_max_width(200)
        print(table.draw())

##    def MMC_PRIORITY_SAVE(arrivalTimes, serviceTimes, priorities):
##            if True:
##                default_name = "MMC_PRIORITY_SIMULATION"
##                filename = filedialog.asksaveasfilename(defaultextension=".csv", initialfile= default_name, filetypes=[("CSV Files", "*.csv")])
##
##                # saving the results to a CSV file
##                with open(filename, mode='w', newline='') as file:
##                    writer = csv.writer(file)
##                    writer.writerow(
##                        [
##                        "S. No.",
##                        "Cumulative Probabilities", 
##                        "CP Lookup", 
##                        "Average Times", 
##                        "Inter Arrivals", 
##                        "Arrival Times", 
##                        "Service Times", 
##                        "Priorities"
##                        ]
##                    )  
##                    for i in range((len(arrivalTimes['arrivalTimes']))):
##                        writer.writerow(
##                            [
##                            i+1, 
##                                arrivalTimes["cumulativeProbabilities"][i],
##                                arrivalTimes["cpLookUp"][i],
##                                arrivalTimes["averageTimes"][i],
##                                arrivalTimes["interArrivals"][i],
##                                arrivalTimes["arrivalTimes"][i],
##                                serviceTimes[i],
##                                priorities[i] 
##                            ]
##                        )              
    meanArrivalNumber=float(mAN.get())
    meanServiceNumber=float(mSN.get())

    


    # meanArrivalNumber = 2.25
    # meanServiceNumber = 8.98
    A = 55
    M = 1994
    Z = 10112166
    C = 9
    a = 1
    b = 3
    # meanArrivalNumber = input("Enter the value of Mean Arrival Number:- ")
    # meanServiceNumber = input("Enter the value of Mean Service Number:- ")
    # meanArrivalNumber = mAN # float(meanArrivalNumber)
    # meanServiceNumber =  mSN # float(meanServiceNumber)
    
    # A = int(input("Enter the value of A:- "))
    # M = int(input("Enter the value of M:- "))
    # Z = int(input("Enter the value of Z:- "))
    # C = int(input("Enter the value of C:- "))
    # a = int(input("Enter the value of a:- "))
    # b = int(input("Enter the value of b:- "))

    
    arrivalTimes = getArrivalTimes(meanArrivalNumber)
    serviceTimes = getServiceTimes(len(arrivalTimes['arrivalTimes']), meanServiceNumber)
    priorities = getPriorities(len(arrivalTimes['arrivalTimes']), A, M, Z, C, a, b)
    display(arrivalTimes, serviceTimes, priorities)
##    MMC_PRIORITY_SAVE(arrivalTimes, serviceTimes, priorities)

    patients = [Patient(i+1, arrivalTimes['arrivalTimes'][i], serviceTimes[i], priorities[i], serviceTimes[i]) for i in range(len(arrivalTimes['arrivalTimes']))]

    serve_highest_priority_first(patients)


button = tk.Button(root, text="Submit", height=2, width=8, bg="white", fg="lightblue", bd=0, command=code, font=font_style)
button.place(x=200, y=180)
