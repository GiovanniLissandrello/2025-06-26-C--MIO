from database.DB_connect import DBConnect
from model.arco import Arco
from model.costruttore import Costruttore
from model.posizionamento import Posizione


class DAO():

    @staticmethod
    def getAllConstructors():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from constructors"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Costruttore(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select year 
                    from seasons"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["year"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllPosizionamenti(anno1, anno2, idcostruttore):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select r2.year as anno, r.driverId as id, coalesce(r.`position`,0) as posizione
                    from constructors c , results r, races r2
                    where c.constructorId = r.constructorId 
                    and r.raceId = r2.raceId
                    and r2.year between %s and %s
                    and c.constructorId = %s"""

        cursor.execute(query,(anno1, anno2, idcostruttore,))

        res = []
        for row in cursor:
            res.append((row["anno"], Posizione(row["id"], row["posizione"])))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllArchi(anno1, anno2, idMap):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select t1.constructorid as id1, t2.constructorid as id2 , (t1.gare_completate1 + t2.gare_completate2) as peso
                    from (select c.constructorId , c.name , count(*) as gare_completate1
                    from constructors c , results r , races r2 
                    where c.constructorId = r.constructorId 
                    and r.raceId = r2.raceId 
                    and r2.year between %s and %s
                    and r.position is not null
                    group by c.constructorId , c.name) t1,
                    (select c.constructorId , c.name , count(*) as gare_completate2
                    from constructors c , results r , races r2 
                    where c.constructorId = r.constructorId 
                    and r.raceId = r2.raceId 
                    and r2.year between %s and %s
                    and r.position is not null
                    group by c.constructorId , c.name) t2
                    where t1.constructorid > t2.constructorid """

        cursor.execute(query, (anno1, anno2,anno1, anno2,))

        res = []
        for row in cursor:
            res.append(Arco(idMap[row["id1"]], idMap[row["id2"]], row["peso"]))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getNumCampionati(anno1,anno2,M,idMap):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select t1.constructorId as id1, count(*) as num_campionati
                    from (select c.constructorId , r2.year 
                    from constructors c , results r , races r2 
                    where c.constructorId = r.constructorId 
                    and r.raceId = r2.raceId 
                    and r2.year between %s and %s
                    group by c.constructorId , r2.year) t1
                    group by t1.constructorId
                    having num_campionati > %s"""
        cursor.execute(query, (anno1,anno2,M,))

        res = []
        for row in cursor:
            res.append(idMap[row["id1"]])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getNumGareCompletate(anno1, anno2, idcostruttore):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select c.constructorId , c.name, count(*) as gare_completate
                    from constructors c , results r , races r2 
                    where c.constructorId = r.constructorId 
                    and r.raceId = r2.raceId 
                    and r2.year between %s and %s
                    and r.position is not null
                    and c.constructorId = %s
                    group by c.constructorId , c.name """

        cursor.execute(query, (anno1, anno2, idcostruttore,))

        res = []
        for row in cursor:
            res.append(row["gare_completate"])

        cursor.close()
        cnx.close()
        return res