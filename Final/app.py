from flask import Flask, request, jsonify
from flask import render_template
from pymongo import MongoClient
from bson import json_util
from bson.json_util import dumps
import pandas as pd
import json
from pprint import pprint
from urlparse import urlparse

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'final'
COLLECTION_NAME = 'dataset'
FIELDS = {'_id': False}

""" Main method - CT"""
@app.route("/")
def index():
    cleanAndLoad()
    return render_template("index_main.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard1.html")

@app.route("/bubbleData")
def bubbleData():
    client = MongoClient()
    db = client.final
    coll = db.geodata
    data = coll.find( {}, { 'state_abr': 1, 'percent_opioid_claim': 1,'_id':0 } )
    json_data = []
    for d in data:
        json_data.append(d)
    json_data = json.dumps(json_data, default=json_util.default)
    client.close()
    return json_data


@app.route("/getGenderData")
def USSexData():
    client = MongoClient()
    db = client.final
    coll = db.nation_wide
    race = urlparse(request.args.get('race','White',type=str)).path
    year = request.args.get('year',type=int)
    print year
    if race == 'All Races-All Origins':
        print 'if'
        pipe =    [ {'$match':{'year': year} },
         {
           '$group':
             {
               '_id':"$gender",
               'totalAmount': { '$sum': '$deaths' }
             }
         },
         {'$project':{'label':'$_id','value':'$totalAmount','_id':0}}
       ]
    else:
        print year
        pipe =  [ {'$match':{ '$and':[{'race': race,'year':year}]}} ,
         {
           '$group':
             {
               '_id':{'gender':"$gender",'race':'$race','year':'$year'},
               'totalAmount': { '$sum': '$deaths' }
             }
         },
         {'$project':{'label':'$_id.gender','race':"$_id.race",'value':'$totalAmount','_id':0}}
       ]
    data = list(coll.aggregate(pipeline=pipe))
    json_data = []
    count = 0
    for d in data:
        count += d['value']
        json_data.append(d)
    json_data.append({'label':'Both Sexes','value':count})
    json_data = json.dumps(json_data, default=json_util.default)
    client.close()
    return json_data

@app.route("/getGenderDataByAge")
def USSexDataByAge():
    client = MongoClient()
    db = client.final
    coll = db.nation_wide
    race = urlparse(request.args.get('race','White',type=str)).path
    year = request.args.get('year',type=int)
    age = urlparse(request.args.get('age','All',type=str)).path
    print year
    if race == 'All Races-All Origins':
        print "all"
        pipe =    [ {'$match':{ '$and':[{'age_group': age,'year':year}]}} ,
         {
           '$group':
             {
               '_id':"$gender",
               'totalAmount': { '$sum': '$deaths' }
             }
         },
         {'$project':{'label':'$_id','value':'$totalAmount','_id':0}}
       ]
    else:
        print 'else'
        pipe =  [ {'$match':{ '$and':[{'race': race,'year':year,'age_group':age}]} },
     {
       '$group':
         {
           '_id':{'gender':"$gender",'race':'$race','year':'$year'},
           'totalAmount': { '$sum': '$deaths' }
         }
     },
     {'$project':{'label':'$_id.gender','race':"$_id.race",'value':'$totalAmount','_id':0}}
   ]

    data = list(coll.aggregate(pipeline=pipe))
    json_data = []
    count = 0
    for d in data:
        count += d['value']
        json_data.append(d)
    json_data.append({'label':'Both Sexes','value':count})
    json_data = json.dumps(json_data, default=json_util.default)
    client.close()
    return json_data

@app.route("/getAgeGroupData")
def USAgeGroupData():
    client = MongoClient()
    db = client.final
    coll = db.nation_wide

    race = urlparse(request.args.get('race','White',type=str)).path
    year = request.args.get('year',1999,type=int)
    if race == 'All Races-All Origins':
        pipe =    [ {'$match':{'year': year} },
         {
           '$group':
             {
               '_id':"$age_group",
               'totalAmount': { '$sum': '$deaths' }
             }
         },
         {'$project':{'label':'$_id','value':'$totalAmount','_id':0}}
       ]
        
    else:
        pipe =    [ {'$match':{ '$and':[{'race': race,'year':year}]}},
         {
           '$group':
             {
               '_id':{'age':"$age_group",'race':'$race','year':'$year'},
               'totalAmount': { '$sum': '$deaths' }
             }
         },
         {'$project':{'label':'$_id.age','race':"$_id.race",'value':'$totalAmount','_id':0}}
       ]
    data = list(coll.aggregate(pipeline=pipe))
    json_data = []
    count = 0
    for d in data:
        count += d['value']
        json_data.append(d)
    # json_data.append({'label':'All Ages','value':count})
    json_data = json.dumps(json_data, default=json_util.default)
    client.close()
    return json_data

@app.route("/getAgeGroupDataByGender")
def USAgeGroupDataByGender():
    client = MongoClient()
    db = client.final
    coll = db.nation_wide

    race = urlparse(request.args.get('race','White',type=str)).path
    year = request.args.get('year',1999,type=int)
    gender = urlparse(request.args.get('gender','Both Sexes',type=str)).path
    if race == 'All Races-All Origins' and gender != 'Both Sexes':
        pipe =    [ {'$match':{ '$and':[{'gender': gender,'year':year}]}},
         {
           '$group':
             {
               '_id':"$age_group",
               'totalAmount': { '$sum': '$deaths' }
             }
         },
         {'$project':{'label':'$_id','value':'$totalAmount','_id':0}}
       ]
    elif race == 'All Races-All Origins' and gender == 'Both Sexes':
        pipe =    [ {'$match':{'year': year} },
         {
           '$group':
             {
               '_id':"$age_group",
               'totalAmount': { '$sum': '$deaths' }
             }
         },
         {'$project':{'label':'$_id','value':'$totalAmount','_id':0}}
       ]

    elif race != 'All Races-All Origins' and gender == 'Both Sexes':
        pipe =    [ {'$match':{ '$and':[{'race': race,'year':year}]}},
         {
           '$group':
             {
               '_id':"$age_group",
               'totalAmount': { '$sum': '$deaths' }
             }
         },
         {'$project':{'label':'$_id','value':'$totalAmount','_id':0}}
       ]
    else:
        pipe =    [ {'$match':{ '$and':[{'race': race,'gender': gender,'year':year}]}},
         {
           '$group':
             {
               '_id':{'age':"$age_group",'race':'$race','year':'$year'},
               'totalAmount': { '$sum': '$deaths' }
             }
         },
         {'$project':{'label':'$_id.age','race':"$_id.race",'value':'$totalAmount','_id':0}}
       ]
    data = list(coll.aggregate(pipeline=pipe))
    json_data = []
    count = 0
    for d in data:
        count += d['value']
        json_data.append(d)
    # json_data.append({'label':'All Ages','value':count})
    json_data = json.dumps(json_data, default=json_util.default)
    client.close()
    return json_data

"""Not using anymore - CT"""
@app.route("/data")
def getData():
    #client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    client = MongoClient()
    #db = client[DBS_NAME]
    db = client.final
    #collection = connection[DBS_NAME][COLLECTION_NAME]
    #coll = db[COLLECTION_NAME]
    coll = db.dataset
    data = pd.DataFrame(list(coll.find({"Year": 2000})))
    # json_data = []
    # for d in data:
    #     json_data.append(d)
    # json_data = json.dumps(json_data, default=json_util.default)
    client.close()
    return data

"""filters the data by year - CT"""
@app.route("/filterDataByYear")
def filterDataByYear():
    client = MongoClient()
    db = client.final
    coll = db.dataset
    year = request.args.get('year',1999,type=int)
    data = list(coll.find({"Year": year},{'_id': False}))
    pd.DataFrame(data).to_csv('./static/data/temp-map-data/temp'+str(year)+'.csv', columns=['Id', 'State','Year', 'Deaths', 'Population', 'Crude Rate', 'Crude Rate Lower 95% Confidence Interval', 'Crude Rate Upper 95% Confidence Interval', 'Prescriptions Dispensed by US Retailers in that year (millions)'], sep=',', encoding='utf-8')
    json_data = []
    for d in data:
        json_data.append(d)
    json_data = json.dumps(json_data, default=json_util.default)
    print json_data
    client.close()
    return json_data

"""Just to render the map page - CT"""
@app.route("/filterData")
def filterData():
    #data = getData()
    #data.to_csv('./static/temp.csv', columns=['Id', 'State','Year', 'Deaths', 'Population', 'Crude Rate', 'Crude Rate Lower 95% Confidence Interval', 'Crude Rate Upper 95% Confidence Interval', 'Prescriptions Dispensed by US Retailers in that year (millions)'], sep=',', encoding='utf-8')
    return render_template("index.html")

""" method to get rx_year_death- AR"""
@app.route("/rx_death")
def getRxDeath():
    client = MongoClient()
    db = client.final
    coll = db.rx_death
    data = list(coll.find({},{'_id':0}))
    #print(data)
    json_data=[]
    for d in data:
        print(d)
        json_data.append(d)
    json_data=json.dumps(json_data,default=json_util.default)
    print(json_data)
    return json_data

""" Data Cleaning and Load in the mongoDB - AR """
@app.route("/cleanAndLoad")
def cleanAndLoad():
    print("hello")
    df = pd.read_csv('./static/data/dataset.csv')
    for j in range(3,9):  
        f=pd.to_numeric(df[df.columns[j]],errors="coerce")
        for i, row in df.iterrows():
            oldValue = row[df.columns[j]]
            if(oldValue=="Suppressed" or oldValue=="Unreliable"):
                df.set_value(i,df.columns[j],f.mean())

    """Setting up the crude rate - AR"""
    print(df.dtypes)
    df[['Population', 'Crude Rate', 'Crude Rate Lower 95% Confidence Interval', 'Crude Rate Upper 95% Confidence Interval', 'Prescriptions Dispensed by US Retailers in that year (millions)']] = df[[ 'Population', 'Crude Rate', 'Crude Rate Lower 95% Confidence Interval', 'Crude Rate Upper 95% Confidence Interval', 'Prescriptions Dispensed by US Retailers in that year (millions)']].astype(float)
    df[['Deaths']] = df[['Deaths']].astype(int)
    print(df.dtypes)
    for i, row in df.iterrows():
        lower = row[df.columns[6]]
        upper = row[df.columns[7]]
        df.set_value(i,df.columns[5],(lower+upper)/2)
    data_json = json.loads(df.to_json(orient='records'))
    """ Putting clean data in mongodb -AR"""
    client = MongoClient()
    coll = client.final.dataset
    coll.drop()
    coll.insert(data_json)
    """ Just saving a copy of db collection to the file- AR"""
    df.to_csv('./static/data/copyOfMainData.csv', columns=['Id', 'State','Year', 'Deaths', 'Population', 'Crude Rate', 'Crude Rate Lower 95% Confidence Interval', 'Crude Rate Upper 95% Confidence Interval', 'Prescriptions Dispensed by US Retailers in that year (millions)'], sep=',', encoding='utf-8')
    
    """Prescription rate vs Deaths over the years - AR"""
    
    #pipe = [{'$group':{'_id':'$Prescriptions Dispensed by US Retailers in that year (millions)','totalDeaths':{'$sum':'$Deaths'}}}]
    pipe = [{'$group':{'_id': {'rx':'$Prescriptions Dispensed by US Retailers in that year (millions)','year':'$Year'},'totalDeaths':{'$sum':'$Deaths'}}},{'$project':{'rx':'$_id.rx', 'year':'$_id.year','deaths':'$totalDeaths','_id':0}}]
    dataXYZ= pd.DataFrame(list(coll.aggregate(pipeline=pipe)))
    #dataXYZ.rename(columns={'_id':'rx','totalDeaths':'deaths'},inplace=True)
    dataXYZ.to_csv('./static/data/copyOfrxDeathYear.csv',index=None)
    coll_rx_death = client.final.rx_death  
    coll_rx_death.drop()
    dataXYZ_json = json.loads(dataXYZ.to_json(orient='records'))
    coll_rx_death.insert(dataXYZ_json)
    #pprint(data_json)
    
    """Reading nationwide data file"""
    nationWide_DF = pd.read_csv('./static/data/nationwide.csv')
    print(nationWide_DF.dtypes)
    nationWide_DF_new = nationWide_DF[['Year','Multiple Cause of death','Ten-Year Age Groups','Gender','Race','Deaths']]
    nationWide_DF_new.columns = ['year','cause','age_group','gender','race','deaths']
    nationWide_DF_new.to_csv('./static/data/copyOfnationWide.csv',index=None)
    coll_nationWide = client.final.nation_wide
    coll_nationWide.drop()
    nationWide_DF_new_json = json.loads(nationWide_DF_new.to_json(orient='records'))
    coll_nationWide.insert(nationWide_DF_new_json)
    #print(nationWide_DF_new)

    """ year cause death """
    pipe = [{'$group':{'_id': {'year':'$year','cause':'$cause'},'totalDeaths':{'$sum':'$deaths'}}},{'$project':{'year':'$_id.year', 'cause':'$_id.cause', 'deaths':'$totalDeaths','_id':0}}]
    abc  = pd.DataFrame(list(coll_nationWide.aggregate(pipeline=pipe)))
    #print(data_causeDeath)
    data_causeDeath = abc.pivot(index='year', columns='cause', values='deaths')
    print data_causeDeath
    data_causeDeath.to_csv('./static/data/copyOfYearcauseDeath.csv',index=True)
    coll_year_cause_death = client.final.year_cause_death  
    coll_year_cause_death.drop()
    data_year_cause_death_json = json.loads(data_causeDeath.to_json(orient='records'))
    print data_year_cause_death_json
    coll_year_cause_death.insert(data_year_cause_death_json)

    """ year age-group death """
    pipe = [{'$group':{'_id': {'year':'$year','age_group':'$age_group'},'totalDeaths':{'$sum':'$deaths'}}},{'$project':{'year':'$_id.year', 'age_group':'$_id.age_group', 'deaths':'$totalDeaths','_id':0}}]
    abc  = pd.DataFrame(list(coll_nationWide.aggregate(pipeline=pipe)))
    data_age_group_Death = abc.pivot(index='year', columns='age_group', values='deaths')
    #dataXYZ.rename(columns={'_id':'rx','totalDeaths':'deaths'},inplace=True)
    data_age_group_Death.to_csv('./static/data/copyOfYearAgeGroupDeath.csv',index=True)
    coll_year_age_group_death = client.final.year_age_group_death  
    coll_year_age_group_death.drop()
    data_year_age_group_death_json = json.loads(data_age_group_Death.to_json(orient='records'))
    coll_year_age_group_death.insert(data_year_age_group_death_json)

    """ year gender death """
    pipe = [{'$group':{'_id': {'year':'$year','gender':'$gender'},'totalDeaths':{'$sum':'$deaths'}}},{'$project':{'year':'$_id.year', 'gender':'$_id.gender', 'deaths':'$totalDeaths','_id':0}}]
    abc  = pd.DataFrame(list(coll_nationWide.aggregate(pipeline=pipe)))
    data_gender_Death = abc.pivot(index='year', columns='gender', values='deaths')
    #dataXYZ.rename(columns={'_id':'rx','totalDeaths':'deaths'},inplace=True)
    data_gender_Death.to_csv('./static/data/copyOfYearGenderDeath.csv',index=True)
    coll_year_gender_death = client.final.year_gender_death  
    coll_year_gender_death.drop()
    data_year_gender_death_json = json.loads(data_gender_Death.to_json(orient='records'))
    coll_year_gender_death.insert(data_year_gender_death_json)

    """ year race death """
    pipe = [{'$group':{'_id': {'year':'$year','race':'$race'},'totalDeaths':{'$sum':'$deaths'}}},{'$project':{'year':'$_id.year', 'race':'$_id.race', 'deaths':'$totalDeaths','_id':0}}]
    abc  = pd.DataFrame(list(coll_nationWide.aggregate(pipeline=pipe)))
    data_race_Death = abc.pivot(index='year', columns='race', values='deaths')
    #dataXYZ.rename(columns={'_id':'rx','totalDeaths':'deaths'},inplace=True)
    data_race_Death.to_csv('./static/data/copyOfYearRaceDeath.csv',index=True)
    coll_year_race_death = client.final.year_race_death  
    coll_year_race_death.drop()
    data_year_race_death_json = json.loads(data_race_Death.to_json(orient='records'))
    coll_year_race_death.insert(data_year_race_death_json)




    """Reading statelevel data file"""
    statelevel_DF = pd.read_csv('./static/data/statelevel.csv')
    print(statelevel_DF.dtypes)
    statelevel_DF_new = statelevel_DF[['State','State Code','Year','Ten-Year Age Groups','Gender','Race','Deaths']]
    statelevel_DF_new.columns = ['state','state_code','year','age_group','gender','race','deaths']
    statelevel_DF_new.to_csv('./static/data/copyOfstateLevel.csv',index=None)
    coll_statelevel = client.final.statelevel
    coll_statelevel.drop()
    statelevel_DF_new_json = json.loads(statelevel_DF_new.to_json(orient='records'))
    coll_statelevel.insert(statelevel_DF_new_json)

    """ Reading geodata file """
    geodata_DF = pd.read_csv('./static/data/geodata.csv')
    print(geodata_DF.dtypes)
    geodata_DF_new = geodata_DF[['fips','state','state_abr','region','provider_count','opioid_claim_count','total_claim_count','percent_opioid_claim']]
    geodata_DF_new.to_csv('./static/data/copyOfGeodata.csv',index=None)
    #geodata_DF_new.columns = ['state','state_code','year','age_group','gender','race','deaths']
    coll_geodata = client.final.geodata
    coll_geodata.drop()
    coll_geodata_DF_new_json = json.loads(geodata_DF_new.to_json(orient='records'))
    coll_geodata.insert(coll_geodata_DF_new_json)



    
if __name__ == "__main__":
   app.run(host='0.0.0.0',port=5000,debug=True)
