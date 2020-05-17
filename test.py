gender='male'
cholesterol=1
gluc=1

gender_male=0
gender_female=0
if gender=='male' or gender=='Male':
    gender_male=1
    gender_female=0
if gender=='female' or gender=='Female':
    gender_male=0
    gender_female=1

cholesterol_normal=0
cholesterol_above_normal=0
cholesterol_well_above_normal=0
if cholesterol==1:
    cholesterol_normal=1
    cholesterol_above_normal = 0
    cholesterol_well_above_normal = 0
if cholesterol==2:
    cholesterol_normal = 0
    cholesterol_above_normal = 1
    cholesterol_well_above_normal = 0
if cholesterol==3:
    cholesterol_normal = 0
    cholesterol_above_normal = 0
    cholesterol_well_above_normal = 1

glucose_normal=0
glucose_above_normal=0
glucose_well_above_normal=0
if gluc==1:
    glucose_normal = 1
    glucose_above_normal = 0
    glucose_well_above_normal = 0
if gluc==2:
    glucose_normal = 0
    glucose_above_normal = 1
    glucose_well_above_normal = 0
if gluc==3:
    glucose_normal = 0
    glucose_above_normal = 0
    glucose_well_above_normal = 1

print(gender_male,gender_female,cholesterol_normal,cholesterol_above_normal,cholesterol_well_above_normal,
      glucose_normal,glucose_above_normal,glucose_well_above_normal)