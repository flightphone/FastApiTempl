import json
import sqlalchemy
from sqlalchemy import text
from sqlalchemy import Engine

# создание движка
#engine = sqlalchemy.create_engine("postgresql+psycopg2://postgres:aA12345678@localhost/sales")
#SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
#engine = sqlalchemy.create_engine(
#    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
#)



class Finder:
    def CompilerFilterOrder(self):
        if self.Fcols == None:
            return
        fls = []
        ords = []
        Fcols_sort = []
        for f in self.Fcols:
            if f['FieldName'] != self.tag and f['FindString'] != '': 
                fls.append(f" ({f['FieldName']} like '%{f['FindString']}%') ")
            if f['FieldName'] != self.tag and f['Sort'] != "Нет" and f['SortOrder'] != None:
                Fcols_sort.append(f)
        
        
        Fcols_sort.sort(key = lambda e: int(e['SortOrder']))
        for f in Fcols_sort:
            s = ''
            if (f['Sort'] == 'ASC'):
                s = ' ' + f['FieldName']
            if (f['Sort'] == 'DESC'):
                s = ' ' + f['FieldName'] + ' desc'
            ords.append(s)   

        self.addFilter = ' and '.join(fls)
        self.OrdField = ','.join(ords)
        

    def start_db(self, id, page, Fc, engine:Engine):
        self.tag = "__all__"
        self.addFilter = ''
        self.OrdField = ''
        self.Fcols = None
        with open(f'JSON/FinderStart{id}.json') as f:
            result = json.load(f)
        
        result['page'] = int(page)
        if Fc!= '':
            self.Fcols = json.loads(Fc)
            self.CompilerFilterOrder()

        sql = result['SQLText']
        decSQL = sql
        localOrdField = ''
        n = sql.lower().find('order by')
        if (n != -1):
            decSQL = sql[:n]
            localOrdField = sql[(n + 8):];

        
        if (self.OrdField == ''):
            self.OrdField = localOrdField
            
        
        if (self.addFilter!=''):
            if (decSQL.lower().find(" where ") == -1 and decSQL.lower().find(" where\n") == -1 and decSQL.lower().find("\nwhere\n") == -1 and decSQL.lower().find("\nwhere ") == -1):
                decSQL += " where "
            else:
                decSQL += " and "

            decSQL += self.addFilter

        sqltotal = decSQL
        if (self.OrdField != ''):
            decSQL = decSQL + " order by " + self.OrdField
        sql = decSQL        
        sqltotal = f'select count(*) n_total from ({sqltotal}) a'

        
        with engine.connect() as connection:
            cur = connection.execute(text(sqltotal))
            #r = cur.fetchall()
            r = [e._asdict() for e in cur]
            
            total = int(r[0]['n_total'])
            result['MaxPage'] = total // int(result['nrows'])
            if total % int(result['nrows']) != 0:
                result['MaxPage'] += 1
            if int(result['page']) > result['MaxPage']:
                result['page'] = result['MaxPage']  
            if int(result['page']) == 0:    
                result['page'] = 1
            result['TotalTab']  = [{'n_total': total}]              

            offset = (int(result['page']) - 1) * int(result['nrows'])
            sql = f"{sql}  limit {result['nrows']}  offset {offset}"
            cur = connection.execute(text(sql))
            result['MainTab'] = [e._asdict() for e in cur] #cur.fetchall()

    
        
        return result    

    def start(self, id, Fc):
        with open(f'JSON/FinderStart{id}.json') as f:
            result = json.load(f)
    
        if Fc!="":
            Fcols = json.loads(Fc)
            fstr = Fcols[-1]["FindString"]
            if fstr!= "":
                fstr = fstr.lower()
                data = []    
                for row in result['MainTab']:
                    add = False
                    for field in row:
                        if str(row[field]).lower().find(fstr) > -1:
                            add = True
                            break
                    if add:
                        data.append(row)
        
                result['MainTab'] = data
        result['TotalTab']  = [{'n_total': len(result['MainTab'])}]              
        return result