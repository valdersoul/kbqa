import json, urllib  # Needed libs
from pprint import pprint  # Not necessary

"""
operations on WikiData.
"""
class wikidata:

    def __init__(self):
        global property_dict
        property_dict = {}
        self.url = "https://quarry.wmflabs.org/run/45013/output/1/json"
        # Fetch json from given lib
        res = json.loads(urllib.urlopen(self.url).read())
        for w in res["rows"]:
            property_dict[w[0]] = w[1]

    def entity2id(self,q):
        """
        # Get wikidata id from wikidata api
        :param self:
        :param q: entity name
        :return: subject_id and subject_description
        """
        ans = []
        url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&search=" + q + "&language=en"
        # url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&search=" + "+".join(
        #     q.split(" ")) + "&language=en"
        get = urllib.urlopen(url).read()
        # print get
        response = json.loads(get)
        # ans += response["search"]
        for s in response["search"]:
            ans.append({
                "s_id": s["id"],
                "subject_des": s["description"]
            })
        return ans


    def getp(self,p):
        """
        Get property name given property id
        :param p: property id
        :return: property name
        """
        return property_dict[p]


    def getc(self,c):
        """
        Get entity name given entity id
        :param c: entity id
        :return: entity name
        """
        url = "https://www.wikidata.org/w/api.php?action=wbgetentities&props=labels&ids=" + c + "&languages=en&format=json"
        response = json.loads(urllib.urlopen(url).read())
        return response["entities"][c]["labels"]["en"]["value"]


    def Related(self,name):
        """
        Get related property-entity (subject_id, subject_description, property_id, property, object_id, object) given entity name
        :param name: entity name
        :return: Return a list of dicts, each dict contains (pid, property, eid, entity)
        Fail to fetch eid would result in empty list
        """
        # Get related property-entity (property id, property name, entity id, entity name) given entity name
        #
        # Fail to fetch eid would result in empty list
        query = self.entity2id(name)
        # print "query" + query
        # if query == "Not Applicable": return []
        ans = []
        for i in range(len(query)):
            s_id = query[i]["s_id"]
            subject_des = query[i]["subject_des"]
            url = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + s_id + "&format=json&languages=en"
            # print urllib.urlopen(url).read()
            response = json.loads(urllib.urlopen(url).read())
            for p in response["entities"][s_id]["claims"]:
                for o in response["entities"][s_id]["claims"][p]:
                    # Enumerate property & entity (multi-property, multi-entity)
                    try:
                        # Some properties are not related to entities, thus try & except
                        o_id = o["mainsnak"]["datavalue"]["value"]["id"]
                        ans.append({
                            "s_id": s_id,
                            "s_des": subject_des,
                            "p_id": p,
                            "property": self.getp(p),
                            "o_id": o_id,
                            "object": self.getc(o_id)
                        })
                    # ans.append("\\property\\"+p+"\t"+getp(p)+"\t\\entity\\"+cid+"\t"+getc(cid))
                    # Print in a pid-pname-eid-ename fashion
                    except:
                        continue
        return ans

"""for test"""
wikidata = wikidata()
# For test only
entity = raw_input("Please input the entity name\n")
pprint(wikidata.Related(entity))
