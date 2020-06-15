import numpy as np
from datetime import datetime
import pandas as pd
import joblib

def outprint(stringx):
    print(stringx)
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    print(dt_string)

outprint("starting to read data finished")

#df = pd.read_csv("datasets/test-dataset.csv")
df = pd.read_csv("datasets/openpowerlifting-2020-05-10.csv")


outprint("data reading finished")

Sex = ['M','F']
Sex_Values = ['Male','Female']
Lift_Values = ['Squat','Bench','Deadlift']
equip_avaliable_types = ['Single-ply', 'Multi-ply', 'Wraps', 'Raw','Straps']
equip_types = ['Raw','Equipped','All']
m_weightclasses = [59, 66, 74, 83, 93, 105, 120,130]
f_weighclasses = [47, 52, 57, 63, 72, 84,100]

wclasses =[m_weightclasses,f_weighclasses]

deadlifts = []
deadlifts_labels = []
deadlifts_hist_data = []
squats = []
squats_labels = []
squats_hist_data = []
bench = []
bench_labels = []
bench_hist_data = []

for sex_ind,sex in enumerate(Sex):
    deadlifts.append([])
    squats.append([])
    bench.append([])
    deadlifts_labels.append([])
    squats_labels.append([])
    bench_labels.append([])
    deadlifts_hist_data.append([])
    squats_hist_data.append([])
    bench_hist_data.append([])
    weightclass = wclasses[sex_ind]
    for weight_ind,weight in enumerate(weightclass):
        deadlifts[sex_ind].append([])
        squats[sex_ind].append([])
        bench[sex_ind].append([])
        deadlifts_labels[sex_ind].append([])
        squats_labels[sex_ind].append([])
        bench_labels[sex_ind].append([])
        deadlifts_hist_data[sex_ind].append([])
        squats_hist_data[sex_ind].append([])
        bench_hist_data[sex_ind].append([])
        for equip in equip_types:
            deadlifts[sex_ind][weight_ind].append([])
            squats[sex_ind][weight_ind].append([])
            bench[sex_ind][weight_ind].append([])
            deadlifts_labels[sex_ind][weight_ind].append([])
            squats_labels[sex_ind][weight_ind].append([])
            bench_labels[sex_ind][weight_ind].append([])
            deadlifts_hist_data[sex_ind][weight_ind].append([])
            squats_hist_data[sex_ind][weight_ind].append([])
            bench_hist_data[sex_ind][weight_ind].append([])


outprint("sorting data")

exclusion_counter = 0

equip_types_counters = [0, 0, 0, 0, 0]


for ind in df.index:
    if ind % 100000 == 0:
        print("processed {} thousand users".format(ind/1000))
        outprint("Exluceded {} entries due to invalid data".format(exclusion_counter))
    person_sex = df['Sex'][ind]
    person_weight = df['BodyweightKg'][ind]
    best_dl = df['Best3DeadliftKg'][ind]
    best_squat = df['Best3SquatKg'][ind]
    best_bench = df['Best3BenchKg'][ind]
    person_equipment =  df['Equipment'][ind]

    if person_equipment in ['Straps']:
        print("person_equipment is straps")
        print("lift vals are {} {} {}".format(best_dl,best_squat,best_bench))

    if person_equipment in ['Straps','Raw']:
        person_equipment = 'Raw'
    elif person_equipment in ['Single-ply','Wraps','Multi-ply']:
        person_equipment = 'Equipped'
    else:
        print("equipment type not found")
    #print(person_equipment)

    if person_sex in Sex:
        sex_ind = Sex.index(person_sex)
        weightclass = wclasses[sex_ind]

        #print("max weight")
        #print(weightclass[len(weightclass)-2])
        if person_weight > weightclass[len(weightclass)-2]:
            weight_class = weightclass[len(weightclass)-1]
            weight_ind = weightclass.index(weight_class)
        else:
            for test_weight_ind, weight in enumerate(weightclass):
                if person_weight < weight:
                    weight_class= weight
                    weight_ind = test_weight_ind
                    break

        if weight_class in weightclass:

                if person_equipment in equip_types:

                    equip_ind = equip_types.index(person_equipment)
                    #print(equip_ind)
                    equip_types_counters[equip_ind] += 1
                    equip_types_counters[2] += 1

                    deadlifts[sex_ind][weight_ind][equip_ind].append(best_dl)
                    squats[sex_ind][weight_ind][equip_ind].append(best_squat)
                    bench[sex_ind][weight_ind][equip_ind].append(best_bench)


                    deadlifts[sex_ind][weight_ind][2].append(best_dl)
                    squats[sex_ind][weight_ind][2].append(best_squat)
                    bench[sex_ind][weight_ind][2].append(best_bench)

                else:
                    exclusion_counter +=1

        else:
            #print("weight is {}, sex is {}".format(person_weight,person_sex))
            #print("sex ind is {}, weight ind is {}".format(sex_ind,weight_ind))
            exclusion_counter +=1
    else:
        #print("weight is {}, sex is {}".format(person_weight,person_sex))
        #print("sex ind is {}, weight ind is {}".format(sex_ind,weight_ind))
        exclusion_counter+=1


print(equip_types)
print(equip_types_counters)



lifts = [squats,bench,deadlifts]
lifts_labels = [squats_labels,bench_labels,deadlifts_labels]
lifts_hist_data = [squats_hist_data,bench_hist_data,deadlifts_hist_data]


outprint("generating hist data")

for lift_ind,lift_type in enumerate(lifts):
    for sex_ind,sex in enumerate(Sex):
        weightclass = wclasses[sex_ind]
        for weight_ind,weight in enumerate(weightclass):
            for equip_ind,equip in enumerate(equip_types):
                lift_data = lifts[lift_ind][sex_ind][weight_ind][equip_ind]
                lift_counts, hist_bins = np.histogram(lift_data, bins=100, range=(0, 500))

                #print(lift_ind,sex_ind,weight_ind)
                lifts_hist_data[lift_ind][sex_ind][weight_ind][equip_ind] = lift_counts

                num_lifters_total = sum(lift_counts) #get total number of lifters in weightclass

                for ind, bin_val in enumerate(hist_bins):
                    num_better = sum(lift_counts[(ind+1):])
                    frac = num_better/num_lifters_total*100 #to make it a percent
                    lifts_labels[lift_ind][sex_ind][weight_ind][equip_ind].append(frac)

print("Equipment types list:")
print(equip_types)

#save("testsave.lst",lifts_hist_data)

joblib.dump(lifts_hist_data,"dataArrays/lift_hists.pkl")
joblib.dump(hist_bins,"dataArrays/hist_bins.pkl")
joblib.dump(lifts_labels,"dataArrays/hist_lables.pkl")
