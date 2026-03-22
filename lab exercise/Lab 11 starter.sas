******************************************************************************
** 	Lab 11 Starter!															**
**	1. understanding "small strata" problems								**
** 	2. effect measure modification											**
******************************************************************************;



libname Raw "/courses/d16994e5ba27fe300/RAW DATA/week _14";
data emm;
set raw.lab11_emm;
run;

*Question 1 hints:

1. restrict data to those where vaccine = 2 (receiving 3 vaccinates)
2. estimate risk of hospitalization separately for each agecat
3. use proc freq (question 1a), proc logistic (question 1b), and proc genmod (question 1c);

proc sort data = emm; by descending covid_clinicvisit descending agecat;
run;

proc freq data = emm order = data;
where vaccine = 2;
table agecat*covid_clinicvisit/measures chisq fisher;
run;

proc logistic descending;
where vaccine = 2;
class agecat (ref = '3')/param = ref;
model covid_clinicvisit = agecat;
run;

proc genmod descending;
where vaccine = 2;
class agecat (ref = '3')/param = ref;
model covid_clinicvisit = agecat/link = log dist = binomial;
estimate "RR 1 vs 3" agecat 1 0/exp;
estimate "RR 2 vs 3" agecat 0 1/exp;
run;




*Question 2 hints:
now focus on those where vaccine = 0 or 1
estimate the OR and 95% CIs (with vaccine = 0 as reference)
assess whether age (continuous) is an effect measure modifier of the vaccine --> hospitalization OR.;

data q2;
set emm;
where vaccine ne 2;
run;

proc logistic descending data = q2;
model covid_clinicvisit = vaccine;
run;

proc logistic descending data = q2;
model covid_clinicvisit = vaccine age age*vaccine;
run;

proc logistic descending data = q2;
model covid_clinicvisit = vaccine|age;
run;


proc genmod descending data = q2;
model covid_clinicvisit = vaccine|age/link = log dist = binomial;
output out = risk_plot predicted = phat;
run;
proc sgplot data = risk_plot;
scatter x = age y = phat/group = vaccine;
run;


*;





*Question 3: graph!;
