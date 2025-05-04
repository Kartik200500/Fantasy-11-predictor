from flask import Flask, request, render_template,redirect,url_for
import matplotlib.pyplot as plt
#import seborn as sns
import pandas as pd
import numpy as np

app = Flask(__name__)

Team_1=  []
Team_2 = []
Team1_Squad = {}
Team2_Squad = {}

match=pd.read_csv('https://storage.googleapis.com/cricket_ipl_data/IPL%20Matches%202008-2025.csv')
byb= pd.read_csv('https://storage.googleapis.com/cricket_ipl_data/IPl%20Ball-by-Ball%202008-2024.csv')
byb.head()

# Fantasy Points

Batsman_points = {'Run':1, 'bFour':1, 'bSix':2, '30Runs':4,
        'Half_century':8, 'Century':16, 'Duck':-2, '170sr':6,
                 '150sr':4, '130sr':2, '70sr':-2, '60sr':-4, '50sr':-6}

Bowling_points = {'Wicket':25, 'LBW_Bowled':8, '3W':4, '4W':8, 
                  '5W':16, 'Maiden':12, '5rpo':6, '6rpo':4, '7rpo':2, '10rpo':-2,
                 '11rpo':-4, '12rpo':-6}

Fielding_points = {'Catch':8, '3Cath':4, 'Stumping':12, 'RunOutD':12,
                  'RunOutInd':6}

# Storing team players
# Here I have to do manual work... choosing the players after the toss and putting them here

#TEAM 1
srh = [
    'H Klaasen', 'Pat Cummins', 'Abhishek Sharma', 'Travis Head', 'Nitish Kumar Reddy',
    'Mohammad Shami', 'Harshal Patel', 'Ishan Kishan', 'Rahul Chahar', 'Smaran Ravichandran',
    'Atharva Taide', 'Abhinav Manohar', 'Simarjeet Singh', 'Zeeshan Ansari', 'Jaydev Unadkat',
    'Wiaan Mulder', 'Kamindu Mendis', 'Aniket Verma', 'Eshan Malinga', 'Sachin Baby'
]


srh_fp = {
    'H Klaasen': 111, 'Pat Cummins': 111, 'Abhishek Sharma': 111, 'Travis Head': 111,
    'Nitish Kumar Reddy': 111, 'Mohammad Shami': 111, 'Harshal Patel': 111, 'Ishan Kishan': 111,
    'Rahul Chahar': 111, 'Smaran Ravichandran': 111, 'Atharva Taide': 111, 'Abhinav Manohar': 111,
    'Simarjeet Singh': 111, 'Zeeshan Ansari': 111, 'Jaydev Unadkat': 111, 'Wiaan Mulder': 111,
    'Kamindu Mendis': 111, 'Aniket Verma': 111, 'Eshan Malinga': 111, 'Sachin Baby': 111
}


#TEAM 2
pbks = [
    'Shashank Singh', 'Prabhsimran Singh', 'Arshdeep Singh', 'Shreyas Iyer', 'Yuzvendra Chahal',
    'Marcus Stoinis', 'Glenn Maxwell', 'Nehal Wadhera', 'Harpreet Brar', 'Vishnu Vinod',
    'Vijaykumar Vyshak', 'Yash Thakur', 'Marco Jansen', 'Josh Inglis', 'Lockie Ferguson',
    'Azmatullah Omarzai', 'Harnoor Pannu', 'Kuldeep Sen', 'Priyansh Arya', 'Aaron Hardie',
    'Suryash Shedge', 'Musheer Khan', 'Xavier Bartlett', 'Pyla Avinash', 'Praveen Dubey'
]

pbks_fp = {
    'Shashank Singh': 111, 'Prabhsimran Singh': 111, 'Arshdeep Singh': 111, 'Shreyas Iyer': 111,
    'Yuzvendra Chahal': 111, 'Marcus Stoinis': 111, 'Glenn Maxwell': 111, 'Nehal Wadhera': 111,
    'Harpreet Brar': 111, 'Vishnu Vinod': 111, 'Vijaykumar Vyshak': 111, 'Yash Thakur': 111,
    'Marco Jansen': 111, 'Josh Inglis': 111, 'Lockie Ferguson': 111, 'Azmatullah Omarzai': 111,
    'Harnoor Pannu': 111, 'Kuldeep Sen': 111, 'Priyansh Arya': 111, 'Aaron Hardie': 111,
    'Suryash Shedge': 111, 'Musheer Khan': 111, 'Xavier Bartlett': 111, 'Pyla Avinash': 111,
    'Praveen Dubey': 111
}


#TEAM 3
csk = ['Matheesha Pathirana', 'Shivam Dube', 'MS Dhoni', 'Devon Conway', 'Rahul Tripathi',
       'Ravichandran Ashwin', 'Syed Khaleel Ahmed', 'Noor Ahmad',
       'Vijay Shankar', 'Sam Curran', 'Shaik Rasheed', 'Anshul Kamboj', 'Mukesh Choudhary',
       'Deepak Hooda', 'Dewald Brevis', 'Nathan Ellis', 'Ramakrishna Ghosh',
       'Kamlesh Nagarkoti', 'Jamie Overton', 'Shreyas Gopal', 'Vansh Bedi',
       'C Andre Siddarth', 'Ravindra Jadeja']


csk_fp = {
    'Matheesha Pathirana': 111, 'Shivam Dube': 111, 'MS Dhoni': 111, 'Devon Conway': 111,
    'Rahul Tripathi': 111,'Ravichandran Ashwin': 111,
    'Syed Khaleel Ahmed': 111, 'Noor Ahmad': 111, 'Vijay Shankar': 111, 'Sam Curran': 111,
    'Shaik Rasheed': 111, 'Anshul Kamboj': 111, 'Mukesh Choudhary': 111, 'Deepak Hooda': 111,
    'Dewald Brevis': 111, 'Nathan Ellis': 111, 'Ramakrishna Ghosh': 111,
    'Kamlesh Nagarkoti': 111, 'Jamie Overton': 111, 'Shreyas Gopal': 111,
    'Vansh Bedi': 111, 'C Andre Siddarth': 111, 'Ravindra Jadeja': 111
}


#TEAM 4
kkr = [
    'RK Singh', 'Varun Chakaravarthy', 'Sunil Narine', 'Andre Russell', 'Harshit Rana',
    'Ramandeep Singh', 'Venkatesh Iyer', 'Quinton de Kock', 'Rahmanullah Gurbaz',
    'Anrich Nortje', 'Angkrish Raghuvanshi', 'Vaibhav Arora', 'Mayank Markande',
    'Rovman Powell', 'Manish Pandey', 'Spencer Johnson', 'Luvnith Sisodia',
    'Ajinkya Rahane', 'Anukul Roy', 'Moeen Ali', 'Chetan Sakariya'
]


kkr_fp = {
    'RK Singh': 111, 'Varun Chakaravarthy': 111, 'Sunil Narine': 111, 'Andre Russell': 111,
    'Harshit Rana': 111, 'Ramandeep Singh': 111, 'Venkatesh Iyer': 111, 'Quinton de Kock': 111,
    'Rahmanullah Gurbaz': 111, 'Anrich Nortje': 111, 'Angkrish Raghuvanshi': 111, 'Vaibhav Arora': 111,
    'Mayank Markande': 111, 'Rovman Powell': 111, 'Manish Pandey': 111, 'Spencer Johnson': 111,
    'Luvnith Sisodia': 111, 'Ajinkya Rahane': 111, 'Anukul Roy': 111, 'Moeen Ali': 111,
    'Chetan Sakariya': 111
}


#TEAM 5
dc = ['Axar Patel', 'Kuldeep Yadav', 'T Stubbs', 'Abishek Porel', 
      'Mitchell Starc', 'KL Rahul', 'Jake Fraser-Mcgurk', 'T Natarajan', 
      'Karun Nair', 'Sameer Rizvi', 'Ashutosh Sharma', 'Mohit Sharma', 'Faf du Plessis', 
      'Mukesh Kumar', 'Darshan Nalkande', 'Vipraj Nigam', 'Dushmantha Chameera', 
      'Donovan Ferreira', 'Ajay Mandal', 'Manvanth Kumar', 'Madhav Tiwari', 'Tripurana Vijay']


dc_fp = {
    'Axar Patel': 111, 'Kuldeep Yadav': 111, 'T Stubbs': 111, 'Abishek Porel': 111, 
    'Mitchell Starc': 111, 'KL Rahul': 111, 'Jake Fraser-Mcgurk': 111, 
    'T Natarajan': 111, 'Karun Nair': 111, 'Sameer Rizvi': 111, 'Ashutosh Sharma': 111, 
    'Mohit Sharma': 111, 'Faf du Plessis': 111, 'Mukesh Kumar': 111, 
    'Darshan Nalkande': 111, 'Vipraj Nigam': 111, 'Dushmantha Chameera': 111, 
    'Donovan Ferreira': 111, 'Ajay Mandal': 111, 'Manvanth Kumar': 111, 'Madhav Tiwari': 111, 
    'Tripurana Vijay': 111 }


#TEAM 6
rcb = [
    'Virat Kohli', 'Rajat Patidar', 'Yash Dayal', 'Liam Livingstone', 'Phil Salt',
    'Jitesh Sharma', 'Josh Hazlewood', 'Rasikh Dar', 'Suyash Sharma', 'Krunal Pandya',
    'Bhuvneshwar Kumar', 'Swapnil Singh', 'Tim David', 'Romario Shepherd', 'Nuwan Thushara',
    'Manoj Bhandage', 'Jacob Bethell', 'Devdutt Padikkal', 'Swastik Chikara', 'Mohit Rathee',
    'Abhinandan Singh', 'Lungi Ngidi'
]
rcb_fp = {
    'Virat Kohli': 414, 'Rajat Patidar': 111, 'Yash Dayal': 111, 'Liam Livingstone': 111,
    'Phil Salt': 111, 'Jitesh Sharma': 111, 'Josh Hazlewood': 111, 'Rasikh Dar': 111,
    'Suyash Sharma': 111, 'Krunal Pandya': 111, 'Bhuvneshwar Kumar': 111, 'Swapnil Singh': 111,
    'Tim David': 111, 'Romario Shepherd': 111, 'Nuwan Thushara': 111, 'Manoj Bhandage': 111,
    'Jacob Bethell': 111, 'Devdutt Padikkal': 111, 'Swastik Chikara': 111, 'Mohit Rathee': 111,
    'Abhinandan Singh': 111, 'Lungi Ngidi': 111
}

               
#TEAM 7
mi = [
    'JJ Bumrah', 'Suryakumar Yadav', 'Hardik Pandya', 'Rohit Sharma', 'Tilak Varma', 'Trent Boult',
    'Naman Dhir', 'Robin Minz', 'Karn Sharma', 'Ryan Rickelton', 'Deepak Chahar', 'Mujeeb-ur-Rahman',
    'Will Jacks', 'Ashwani Kumar', 'Mitchell Santner', 'Reece Topley', 'Shrijith Krishnan', 'Raj Bawa',
    'Satyanarayana Raju', 'Bevon Jacobs', 'Arjun Tendulkar', 'Corbin Bosch', 'Vignesh Puthur'
]

mi_fp = {
    'JJ Bumrah': 382, 'Suryakumar Yadav': 307, 'Hardik Pandya': 111, 'Rohit Sharma': 393,
    'Tilak Varma': 111, 'Trent Boult': 111, 'Naman Dhir': 111, 'Robin Minz': 111,
    'Karn Sharma': 111, 'Ryan Rickelton': 111, 'Deepak Chahar': 111, 'Mujeeb-ur-Rahman': 111,
    'Will Jacks': 111, 'Ashwani Kumar': 111, 'Mitchell Santner': 111, 'Reece Topley': 111,
    'Shrijith Krishnan': 111, 'Raj Bawa': 111, 'Satyanarayana Raju': 111, 'Bevon Jacobs': 111,
    'Arjun Tendulkar': 111, 'Corbin Bosch': 111, 'Vignesh Puthur': 111
}


#TEAM 8
rr = [
    'Sanju Samson', 'Yashasvi Jaiswal', 'Riyan Parag', 'Dhruv Jurel', 'Shimron Hetmyer',
    'Sandeep Sharma', 'Jofra Archer', 'Mahesh Theekshana', 'Wanindu Hasaranga', 'Akash Madhwal',
    'Kumar Kartikeya Singh', 'Nitish Rana', 'Tushar Deshpande', 'Shubham Dubey', 'Yudhvir Charak',
    'Fazalhaq Farooqi', 'Vaibhav Suryavanshi', 'Kwena Maphaka', 'Ashok Sharma', 'Kunal Singh Rathore'
]


rr_fp = {
    'Sanju Samson': 111, 'Yashasvi Jaiswal': 111, 'Riyan Parag': 111, 'Dhruv Jurel': 111,
    'Shimron Hetmyer': 111, 'Sandeep Sharma': 111, 'Jofra Archer': 111, 'Mahesh Theekshana': 111,
    'Wanindu Hasaranga': 111, 'Akash Madhwal': 111, 'Kumar Kartikeya Singh': 111, 'Nitish Rana': 111,
    'Tushar Deshpande': 111, 'Shubham Dubey': 111, 'Yudhvir Charak': 111, 'Fazalhaq Farooqi': 111,
    'Vaibhav Suryavanshi': 111, 'Kwena Maphaka': 111, 'Ashok Sharma': 111, 'Kunal Singh Rathore': 111
}


#TEAM 9
gt = [
    'Rashid Khan', 'Shubman Gill', 'Sai Sudharsan', 'Rahul Tewatia', 'Shahrukh Khan',
    'Kagiso Rabada', 'Jos Buttler', 'Mohammad Siraj', 'Prasidh Krishna', 'Nishant Sindhu',
    'Mahipal Lomror', 'Kumar Kushagra', 'Anuj Rawat', 'Manav Suthar', 'Washington Sundar',
    'Gerald Coetzee', 'Arshad Khan', 'Gurnoor Brar', 'Sherfane Rutherford', 'R Sai Kishore',
    'Ishant Sharma', 'Jayant Yadav', 'Dasun Shanaka', 'Karim Janat', 'Kulwant Khejroliya'
]


gt_fp = {
    'Rashid Khan': 111, 'Shubman Gill': 111, 'Sai Sudharsan': 111, 'Rahul Tewatia': 111, 'Shahrukh Khan': 111,
    'Kagiso Rabada': 111, 'Jos Buttler': 111, 'Mohammad Siraj': 111, 'Prasidh Krishna': 111, 'Nishant Sindhu': 111,
    'Mahipal Lomror': 111, 'Kumar Kushagra': 111, 'Anuj Rawat': 111, 'Manav Suthar': 111, 'Washington Sundar': 111,
    'Gerald Coetzee': 111, 'Arshad Khan': 111, 'Gurnoor Brar': 111, 'Sherfane Rutherford': 111, 'R Sai Kishore': 111,
    'Ishant Sharma': 111, 'Jayant Yadav': 111, 'Dasun Shanaka': 111, 'Karim Janat': 111, 'Kulwant Khejroliya': 111
}


#TEAM 10

lsg = [
    'Nicholas Pooran', 'Ravi Bishnoi', 'Mayank Yadav', 'Ayush Badoni', 'Shardul Thakur',
    'Rishabh Pant', 'David Miller', 'Mitchell Marsh', 'Aiden Markram', 'Avesh Khan',
    'Abdul Samad', 'Aryan Juyal', 'Akash Deep', 'Himmat Singh', 'M Siddharth',
    'Digvesh Singh', 'Shahbaz Ahmed', 'Akash Singh', 'Shamar Joseph', 'Prince Yadav',
    'Yuvraj Chaudhary', 'Rajvardhan Hangargekar', 'Arshin Kulkarni', 'Matthew Breetzke'
]


lsg_fp = {
    'Nicholas Pooran': 111, 'Ravi Bishnoi': 111, 'Mayank Yadav': 111, 'Ayush Badoni': 111, 'Shardul Thakur': 111,
    'Rishabh Pant': 111, 'David Miller': 111, 'Mitchell Marsh': 111, 'Aiden Markram': 111, 'Avesh Khan': 111,
    'Abdul Samad': 111, 'Aryan Juyal': 111, 'Akash Deep': 111, 'Himmat Singh': 111, 'M Siddharth': 111,
    'Digvesh Singh': 111, 'Shahbaz Ahmed': 111, 'Akash Singh': 111, 'Shamar Joseph': 111, 'Prince Yadav': 111,
    'Yuvraj Chaudhary': 111, 'Rajvardhan Hangargekar': 111, 'Arshin Kulkarni': 111, 'Matthew Breetzke': 111
}


'''
team1 = lsg; team2 = gt              #team1 v Team2

for i in range(len(team1)):
    ffp = []
    for j in range(len(team2)):
        bat_vs_bowl = byb[(byb["batsman"]==team1[i]) & (byb["bowler"]==team2[j])]
        bowls_played = len(bat_vs_bowl.batsman_runs)
        runs_scored = sum(bat_vs_bowl.batsman_runs)
        fours = len(bat_vs_bowl[bat_vs_bowl['batsman_runs']==4])
        sixes = len(bat_vs_bowl[bat_vs_bowl['batsman_runs']==6])
        wicket = sum(bat_vs_bowl.is_wicket)
        if bowls_played <=6*10 and wicket >=5:
            penalty = -16
            k =  print (team1[i], "'s wicket taken",wicket,"times by", team2[j])
        elif bowls_played <=6*8 and wicket >=4:
            penalty = -8
            l = print (team1[i], "'s wicket taken",wicket,"times by", team2[j])
        elif bowls_played <=6*6 and wicket >=3:
            penalty = -4
            p =print (team1[i], "'s wicket taken",wicket,"times by", team2[j])
        else:
            penalty = 0
        try:    
            strike_rate = int(runs_scored/bowls_played*100)
        except: 
            strike_rate = 'NA'

        if bowls_played >=8 and strike_rate!='NA':
            if strike_rate >=170:
               n =  print (team1[i] ,"beaten", team2[j], "Runs", runs_scored,"bowls",bowls_played,"strike rate", strike_rate,'Out',wicket,'times', "Fours", fours,"Sixes", sixes)            
            elif strike_rate >=150:
               m =  print (team1[i] ,"beaten", team2[j], "Runs", runs_scored,"bowls",bowls_played,"strike rate", strike_rate,'Out',wicket,'times', "Fours", fours,"Sixes", sixes)            
                        
        bowl_vs_bat = byb[(byb["bowler"]==team1[i]) & (byb["batsman"]==team2[j])]
        wicket_took = sum(bowl_vs_bat.is_wicket)
        fantasy_points1 = runs_scored + fours*Batsman_points['bFour'] + sixes*Batsman_points['bSix'] - wicket*Bowling_points['Wicket'] + wicket_took*Bowling_points['Wicket'] + penalty
        pd.DataFrame(ffp.append(fantasy_points1))
        #print (team1[i] ,"against", team2[j], "Runs", runs_scored, 
        #     "bowls",bowls_played,"strike rate", strike_rate,
         #      'Out',wicket,'times', "Fours", fours,"Sixes", sixes)

team1 = gt; team2 = lsg                     #Team2 v Team1

for i in range(len(team1)):
    ffp=[]
    for j in range(len(team2)):
        bat_vs_bowl = byb[(byb["batsman"]==team1[i]) & (byb["bowler"]==team2[j])]
        bowls_played = len(bat_vs_bowl.batsman_runs)
        runs_scored = sum(bat_vs_bowl.batsman_runs)
        fours = len(bat_vs_bowl[bat_vs_bowl['batsman_runs']==4])
        sixes = len(bat_vs_bowl[bat_vs_bowl['batsman_runs']==6])
        wicket = sum(bat_vs_bowl.is_wicket)
        if bowls_played <=6*10 and wicket >=5:
            penalty = -16
            print (team1[i], "'s wicket taken",wicket,"times by", team2[j])
        elif bowls_played <=6*8 and wicket >=4:
            penalty = -8
            print (team1[i], "'s wicket taken",wicket,"times by", team2[j])
        elif bowls_played <=6*6 and wicket >=3:
            penalty = -4
            print (team1[i], "'s wicket taken",wicket,"times by", team2[j])
        else:
            penalty = 0
        try:    
            strike_rate = int(runs_scored/bowls_played*100)
        except: 
            strike_rate = 'NA'

        if bowls_played >=8 and strike_rate!='NA':
            if strike_rate >=170:
                print (team1[i] ,"beaten", team2[j], "Runs", runs_scored,"bowls",bowls_played,"strike rate", strike_rate,'Out',wicket,'times', "Fours", fours,"Sixes", sixes)            
            elif strike_rate >=150:
                print (team1[i] ,"beaten", team2[j], "Runs", runs_scored,"bowls",bowls_played,"strike rate", strike_rate,'Out',wicket,'times', "Fours", fours,"Sixes", sixes)            
                        
        bowl_vs_bat = byb[(byb["bowler"]==team1[i]) & (byb["batsman"]==team2[j])]
        wicket_took = sum(bowl_vs_bat.is_wicket)
        fantasy_points1 = runs_scored + fours*Batsman_points['bFour'] + sixes*Batsman_points['bSix'] - wicket*Bowling_points['Wicket'] + wicket_took*Bowling_points['Wicket'] + penalty
        ffp.append(fantasy_points1)
        #print (team1[i] ,"against", team2[j], "Runs", runs_scored, 
             #   "bowls",bowls_played,"strike rate", strike_rate,
              # 'Out',wicket,'times', "Fours", fours,"Sixes", sixes, 'fantasy_points', fantasy_points1)

'''

def get_players(team1,team2,team1_fp):
    fantasy_team_players = []

    for i in range(len(team1)):
        unq_ids = byb[byb["batsman"]==team1[i]]['id'].unique()
        mathces_played = len(unq_ids)
#         print ( "Number of matches played" , len(unq_ids),team1[i])
        bbr = []
        for x in unq_ids:
            bat_run = sum(byb[(byb["batsman"]==team1[i])&(byb['id']==x)]['batsman_runs'])
            bbr.append(bat_run)

        r30,r50,r100 =0,0,0
        for m in bbr:
            if m>=100:
                r100+=1
            elif m>=50:
                r50+=1
            elif m>=30:
                r30+=1
        try:
            catches = len(byb[(byb['fielder']==team1[i]) & (byb['dismissal_kind']=='caught')])/mathces_played
            run_outs = len(byb[(byb['fielder']==team1[i]) & (byb['dismissal_kind']=='run out')])/mathces_played
            extra_points = r30/mathces_played*Batsman_points['30Runs'] +r50/mathces_played*Batsman_points['Half_century'] +r100/mathces_played*Batsman_points['Century'] +catches*Fielding_points['Catch']+run_outs*Fielding_points['RunOutInd']
        except:
            catches, run_outs, extra_points = 0,0,0
        
        # Extra Points for bowlers to be estimated here
        wickets_taken = []
        for x in unq_ids:
            twx = sum(byb[(byb["bowler"]==team1[i]) & (byb['id']==x)]['is_wicket'])
            wickets_taken.append(twx)

        w3,w4,w5 = 0,0,0
        for z in wickets_taken:
            if z>=5:
                w5+=1
            elif z>=4:
                w4+=1
            elif z>=3:
                w3+=1
        try:
            lbws = len((byb[(byb['bowler']==team1[i]) & (byb['dismissal_kind']=='lbw')]))/mathces_played      
            bowled = len((byb[(byb['bowler']==team1[i]) & (byb['dismissal_kind']=='bowled')]))/mathces_played      
            wexp = w3/mathces_played*Bowling_points['3W'] + w4/mathces_played*Bowling_points['4W'] + w5/mathces_played*Bowling_points['5W'] + lbws*Bowling_points['LBW_Bowled'] + bowled*Bowling_points['LBW_Bowled']
        except:
            lbws, bowled, wexp = 0,0,0
        
        ffp = []
        for j in range(len(team2)):
            bat_vs_bowl = byb[(byb["batsman"]==team1[i]) & (byb["bowler"]==team2[j])]
            bowls_played = len(bat_vs_bowl.batsman_runs)
            runs_scored = sum(bat_vs_bowl.batsman_runs)
            fours = len(bat_vs_bowl[bat_vs_bowl['batsman_runs']==4])
            sixes = len(bat_vs_bowl[bat_vs_bowl['batsman_runs']==6])
            wicket = sum(bat_vs_bowl.is_wicket)
            if bowls_played <=6*10 and wicket >=5:
                penalty = -16
                print (team1[i], "ka wicket taken",wicket,"times by", team2[j])
            elif bowls_played <=6*8 and wicket >=4:
                penalty = -8
                print (team1[i], "ka wicket taken",wicket,"times by", team2[j])
            elif bowls_played <=6*6 and wicket >=3:
                penalty = -4
                print (team1[i], "'s wicket taken",wicket,"times by", team2[j])
            else:
                penalty = 0

            try:    
                strike_rate = int(runs_scored/bowls_played*100)
            except: 
                strike_rate = 'NA'            
            if bowls_played >=10 and strike_rate!='NA':
                if strike_rate >=170:
                    print (team1[i] ,"beaten", team2[j], "Runs", runs_scored,"bowls",bowls_played,"strike rate", strike_rate,'Out',wicket,'times', "Fours", fours,"Sixes", sixes)            
                elif strike_rate >=150:
                    print (team1[i] ,"beaten", team2[j], "Runs", runs_scored,"bowls",bowls_played,"strike rate", strike_rate,'Out',wicket,'times', "Fours", fours,"Sixes", sixes)            
   
            bowl_vs_bat = byb[(byb["bowler"]==team1[i]) & (byb["batsman"]==team2[j])]
            wicket_took = sum(bowl_vs_bat.is_wicket)
            fantasy_points1 = runs_scored + fours*Batsman_points['bFour'] + sixes*Batsman_points['bSix'] - wicket*Bowling_points['Wicket'] + wicket_took*Bowling_points['Wicket'] + penalty 
            ffp.append(fantasy_points1)
            print (team1[i] ,"against", team2[j], "Runs", runs_scored, 
                     "bowls",bowls_played,"strike rate", strike_rate,
                     'Out',wicket,'times', "Fours", fours,"Sixes", sixes, "fatansy points",fantasy_points1)
        sum_ffp = sum(ffp)
        if team1_fp[team1[i]] > 0:
            recent_performace_points = np.log(team1_fp[team1[i]])
        elif team1_fp[team1[i]] <0:
            recent_performace_points = -np.log(abs(team1_fp[team1[i]]))
        else:
            recent_performace_points = 0
        # Trying a new method for recent performancec point
        recent_performace_points = team1_fp[team1[i]]/3
        weight1 = 0.5
        weight2 = 1 - weight1
        final_fantasy_point = (sum_ffp + extra_points + wexp)*weight1 + recent_performace_points*weight2
        final_fantasy_point = round(final_fantasy_point,2)
        fantasy_team_players.append((final_fantasy_point,team1[i]))
        fantasy_team_players.sort(reverse=True)
#         print ("Fatasy points of",team1[i],final_fantasy_point)
    return fantasy_team_players

'''
def selection1():
    players_df = pd.read_excel('{Team_1}.xlsx')
    df['player_name'] = df['player_name'].str.strip()
    players = players_df['player_name'].tolist()
    selected_players = request.form.getlist('player')
    # Ensure exactly 11 players are selected
    if len(selected_players) == 11:
        # Store selected players in the Team list
        Team_1 = selected_players

def selection2(Team_2):
    players_df = pd.read_excel('{Team_2}.xlsx')
    players = players_df['player_name'].tolist()
'''

@app.route('/')
def home():
    # Render the 'login.html' template
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/process_login', methods=['POST'])
def process_login():
    # Process the login form data (replace this with your actual login logic)
    email = request.form.get('email')
    password = request.form.get('password')

    # Perform login validation here (replace this with your actual validation logic)

    # For demonstration purposes, let's assume successful login
    if email == "user@example.com" and password == "password":
        # Redirect to the '/index' route upon successful login
        return redirect(url_for('index'))

    # If login fails, you can render the login template again with an error message
    return render_template('login.html', login_error=True)

@app.route('/index', methods=['GET', 'POST'])

def select_team():
    
    global Team_1, Team_2, Team1_Squad, Team2_Squad,user_choice1,user_choice2
    if request.method == 'POST':
        if 'team1' in request.form:
            user_choice1 = request.form['team1']
    # rest of your code
        else:
    # handle the case where 'team1' is not present in the form
            error_message = 'Please select a team for Team 1.'
            print(error_message)
    
        if 'team2' in request.form:
            user_choice2 = request.form['team2']
    # rest of your code
        else:
    # handle the case where 'team1' is not present in the form
            error_message = 'Please select a team for Team 2.'
            print(error_message)

        p1 = f'Teams\{user_choice1}.xlsx'
        p1_df = pd.read_excel(p1)
        players1 = p1_df['player_name'].tolist()

        p2 = f'Teams\{user_choice2}.xlsx'
        p2_df = pd.read_excel(p2)
        players2 = p2_df['player_name'].tolist()

        if user_choice1 == 'SRH':
            Team1_Squad = srh_fp
        elif user_choice1 == 'PBKS':
            Team1_Squad = pbks_fp
        elif user_choice1 == 'CSK':
            Team1_Squad = csk_fp
        elif user_choice1 == 'KKR':
            Team1_Squad = kkr_fp
        elif user_choice1 == 'DC':
            Team1_Squad = dc_fp
        elif user_choice1 == 'RCB':
            Team1_Squad = rcb_fp
        elif user_choice1 == 'MI':
            Team1_Squad = mi_fp
        elif user_choice1 == 'RR':
            Team1_Squad = rr_fp
        elif user_choice1 == 'GT':
            Team1_Squad = gt_fp
        elif user_choice1 == 'LSG':
            Team1_Squad = lsg_fp
        else:
            print("Invalid choice.")

        if user_choice2 == 'SRH':
            Team2_Squad = srh_fp
        elif user_choice2 == 'PBKS':
            Team2_Squad = pbks_fp
        elif user_choice2 == 'CSK':
            Team2_Squad = csk_fp
        elif user_choice2 == 'KKR':
            Team2_Squad = kkr_fp
        elif user_choice2 == 'DC':
            Team2_Squad = dc_fp
        elif user_choice2 == 'RCB':
            Team2_Squad = rcb_fp
        elif user_choice2 == 'MI':
            Team2_Squad = mi_fp
        elif user_choice2 == 'RR':
            Team2_Squad = rr_fp
        elif user_choice2 == 'GT':
            Team2_Squad = gt_fp
        elif user_choice2 == 'LSG':
            Team2_Squad = lsg_fp
        else:
            print("Invalid choice.")

        selected_players1 = request.form.getlist('player1')
        selected_players2 = request.form.getlist('player2')
        print(selected_players1)
        print(selected_players2)

        if len(selected_players1) == 11 and len(selected_players2) == 11:
            Team_1 = selected_players1
            Team_2 = selected_players2
              
        else:
            error_message = 'Please select exactly 11 players for both teams.'
            return render_template('player.html', players1=players1, players2=players2, error_message=error_message)

        t1 = get_players(Team_1, Team_2, Team1_Squad)
        t2 = get_players(Team_2, Team_1, Team2_Squad)

        t3 = t1 + t2
        t3.sort(reverse=True)
        Team = pd.DataFrame(t3)
        Result = Team[1].head(11)
        Result = pd.DataFrame(Result)
        print('\nFinal Predicted Team',Result)

        predicted_team = Result.to_html()  # Convert the result to HTML

        return render_template('result.html', predicted_team=predicted_team)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
