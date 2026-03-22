******************************************************************************
** 	Lab 11 																	**
**	1. understanding "small strata" problems								**
** 	2. effect measure modification											**
******************************************************************************;


libname Raw "/courses/d16994e5ba27fe300/RAW DATA/week _13";
data emm;
set raw.lab11_emm;
run;


/*lab assignment*/

*question 1, part a. PROC FREQ;

proc sort data = emm; by descending covid_clinicvisit descending agecat;
proc freq data = emm order = data;
where vaccine = 2;
table agecat*covid_clinicvisit/chisq exact;
run;

*the point of this question is to have you understand that inference is REALLY HARD
 with a small sample size. here, there is only one 5-11 year old who has 3 doses of the vaccine,
 only 10 12-15 year olds (and only 1 of them tested positive for covid).
 therefore, i can't really say anything about whether the risk of covid detection differs by age group here.
 (if  you were to conduct a "fishers exact test" you would get a large p-value here)
  

*question 1, part b. PROC LOGISTIC
Run a PROC Logistic to estimate whether odds of testing positive for COVID 
restricted to the population that received 3 doses of the Pfizer vaccine (vaccine = 2) differs by variable Agecat.;

proc logistic descending data = emm; where vaccine = 2;
class agecat (ref = '3')/param = ref;
model covid_clinicvisit = agecat;
run;

*warning sign #1. you get a yellow "danger" triangle in the program tab.
 checking the log, we get the following message:
 
 There is possibly a quasi-complete separation of data points. 
 The maximum likelihood estimate may not exist.
 WARNING: The LOGISTIC procedure continues in spite of the above warning. 
 Results shown are based on the last maximum likelihood 
 iteration. Validity of the model fit is questionable.
 
 
 PRO TIP!!! when a computer tells you the "validity of the model fit is questionable"
 YOU SHOULD NOT USE THE RESULTS!!!!!!
 
 SO, the odds ratios are not interpretable because the validity of the model fit is questionable.
 also, check out the ones in the output (and look at the CIs). HUGE CIs --> no power.
 
 				OR		LCL			UCL
 agecat 1 vs 3	<0.001	<0.001	>999.999
 agecat 2 vs 3	1.667	0.167	16.633
;


*question 1, part c. PROC GENMOD.
 a note on getting RRs from proc genmod.
 look at the output 'class level information.'
 copy down the 1/0 order for the comparison of interest.
 example here.;
 
proc genmod data = emm descending; where vaccine = 2;
class agecat (ref = '3')/param = ref;
model covid_clinicvisit = agecat/link = log dist = binomial;
estimate "RR 1 vs 3" agecat 1 0/exp;
estimate "RR 2 vs 3" agecat 0 1/exp;
run;

*in this scenario, SAS provides a point estimate and 95% CI for one of the comparisons (agecat 2 vs agecat 3)
 but not 1 vs 3. 
 any time you see extremely wide CIs this means your sample size is too small!!!!
 You cant/should not interpret these either!;


************************************************************************************************************
** Question 2
************************************************************************************************************;

data emmb; set emm; where vaccine in (0,1);
run;
*can use proc freq or logistic;

proc logistic descending data = emmb;
class vaccine (ref = '0')/param = ref;
model covid_clinicvisit = vaccine; run;

proc sort data = emmb; by descending vaccine descending covid_clinicvisit;
proc freq data = emmb order = data;
table vaccine * covid_clinicvisit/measures;
run;


*OR (95% CI) = 0.247 (0.227-0.269)
*children receiving 2 doses of vaccine had 0.25 times the odds of 
 visiting an ER or UCC due to covid compared to children receiving no vaccine.
 
 a range of reasonable estimates for the true OR consistent with our data is 
 between 0.23 and 0.27.
 
 our CI is very tight because large N. it would take A LOT of bias to move
 this finding toward the null substantially.
 

*Part B. EMM;

proc logistic descending data = emmb;
class vaccine (ref = '0')/param = ref;
model covid_clinicvisit = vaccine age vaccine*age;
run;


proc logistic descending data = emmb;
class vaccine (ref = '0') agecat/param = ref;
model covid_clinicvisit = vaccine agecat vaccine*agecat;
run;

*PRO TIP: a SAS shortcut to tell the computer to use all combinations of two variables looks like this!;
proc logistic descending data = emmb;
class vaccine (ref = '0')/param = ref;
model covid_clinicvisit = vaccine|age;
run; 

*statistically, what we are looking for is whether the OR changes by age.
 the p-value for the interaction term tells us whether there is multiplicative-scale interaction
 on the odds ratio scale. small P-value suggests yes it is acting as an EMM.
 
 (interaction p-value <0.0001);
 
*Part C. EMM for RR;

proc genmod descending data = emmb;
class vaccine (ref = '0')/param = ref;
model covid_clinicvisit = vaccine|age / link = log dist = binomial;
run;


*Question 3 plot how effect measure is modified by age.;

 
proc genmod descending data = emmb;
class vaccine (ref = '0')/param = ref;
model covid_clinicvisit = vaccine|age / link = log dist  = binomial;
output out = risk_plot predicted = prob_covidvisit;
run;

*plotting risk on y-axis;
proc sgplot data = risk_plot;
scatter x = age y = prob_covidvisit/group = vaccine;
run;

*BONUS Q4;

*plotting RR and RD on y-axis. probably many other ways to do this.;

proc means mean data = risk_plot; where vaccine = 0;
class age;
var prob_covidvisit; 
output out = temp1 mean = prob_vaccine0;run;
proc means mean data = risk_plot; where vaccine = 1;
class age;
var prob_covidvisit; 
output out = temp2 mean = prob_vaccine1;run;
data RRplot;
merge temp1 temp2; by age;
if age = . then delete; 
RR = prob_vaccine1/prob_vaccine0;
RD = prob_vaccine1 - prob_vaccine0;
run;

proc sgplot data = RRplot;
scatter X = age y = RR; 
scatter x = age y = RD;
run;


