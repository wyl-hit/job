# coding=utf-8

import logging
import MySQLdb


class UrlDB():

    '''
    Insert into Data to mysql
    '''

    def __init__(self, host, username, password, db):
        try:
            self.conn = MySQLdb.connect(host=host, user=username,
                                        passwd=password, db=db, charset='utf8')
            self.cursor = self.conn.cursor()
        except Exception, e:
            self.status = 'Error:%s' % str(e)
        else:
            self.status = 'Ok'

    def __del__(self):
        ''' Close cursor and connction '''
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()

    def getIDFromMysql(self, sql):
        ''' Get ID from Mysql database '''
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.conn.commit()
        except Exception, e:
            self.status = "Error:%s" % str(e)
            return None
        else:
            self.status = 'Ok'

        if len(results) > 0:
            return results[0][0]
        else:
            return None

    def insertIntoDB(self, sql):
        ''' Insert the value to Mysql database '''
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            getid_sql = 'select last_insert_id()'
            self.cursor.execute(getid_sql)
            results = self.cursor.fetchall()
            self.conn.commit()
        except Exception, e:
            self.status = 'Error:%s' % str(e)
            return None
        else:
            self.status = 'Ok'

        if len(results) > 0:
            return results[0][0]
        else:
            return None

    def getLastInsertID(self):
        self.cursor.execute('select last_insert_id()')
        results = self.cursor.fetchall()
        self.conn.commit()

        if len(results) > 0:
            return results[0][0]
        else:
            return 1

    def writeToDB(self, whois_dict):
        ''' Write the whois information to mysql '''

        contacts_admin_id = 1
        contacts_tech_id = 1
        contacts_registrant_id = 1

        if 'admin' in whois_dict['contacts'].keys()  and         \
                whois_dict['contacts']['admin'] is not None and        \
                whois_dict['contacts']['admin']['name'] != '' and      \
                whois_dict['contacts']['admin']['email'] != '':
            # print whois_dict['contacts']['admin']
            contacts_admin_id = self._writeToDB(
                'whois_contacts', whois_dict['contacts']['admin'])

        if 'tech' in whois_dict['contacts'].keys() and           \
                whois_dict['contacts']['tech'] is not None and         \
                whois_dict['contacts']['tech']['name'] != '' and       \
                whois_dict['contacts']['tech']['email'] != '':
            # print whois_dict['contacts']['tech']
            contacts_tech_id = self._writeToDB(
                'whois_contacts', whois_dict['contacts']['tech'])

        if 'registrant' in whois_dict['contacts'].keys() and      \
                whois_dict['contacts']['registrant'] is not None and    \
                whois_dict['contacts']['registrant']['name'] != '' and  \
                whois_dict['contacts']['registrant']['email'] != '':
            # print whois_dict['contacts']['registrant']
            contacts_registrant_id = self._writeToDB(
                'whois_contacts', whois_dict['contacts']['registrant'])

        if contacts_admin_id == 1 and contacts_tech_id == 1 and contacts_registrant_id == 1:
            logging.critical('%s For detail in %s' % (whois_dict['domain']['name'],
                                                      whois_dict['whois_server']))

        #domain(auto_id, domain_id, name, status, admin, tech, registrant, creation_date, update_date,expiration_date)
        self._writeToDB('whois_domain', whois_dict['domain'],
                        admin=contacts_admin_id,
                        tech=contacts_tech_id,
                        registrant=contacts_registrant_id)

    def _writeToDB(self, table, args, admin=0, tech=0, registrant=0):
        ''' Dump SQL sentenct and write to mysql '''

        if table == 'whois_contacts':
            # first check whether the record exist in db
            check_sql = 'select contacts_id from %s where name="%s" and email="%s"' \
                % (table, args['name'], args['email'])
            results = self.getIDFromMysql(check_sql)
            if results is not None:
                return results

            # insert the record into db
            insert_sql = 'insert into %s(name, phone, fax, email, org,       \
                    country, city, street, postalcode) values ("%s", "%s", "%s", \
                    "%s", "%s", "%s", "%s", "%s", "%s")' % (table, args['name'],
                                                            args['phone'], args['fax'], args['email'], args[
                                                                'organization'], args['country'],
                                                            args['city'], args['street'], args['postalcode'])
            results = self.insertIntoDB(insert_sql)
            if self.status.startswith('Error:'):
                logging.error(self.status)

            return self.getLastInsertID()

        elif table == 'whois_domain':
            # check whether the record exists in the db
            check_sql = 'select auto_id from %s where domain_id="%s" and name="%s"' %\
                (table, args['id'], args['name'])
            results = self.getIDFromMysql(check_sql)
            if results is not None:
                return results

            # insert the record into db
            insert_sql = 'insert into %s(domain_id, name, admin, tech,\
                    registrant, create_date, update_date, expiration_date)    \
                    values("%s", "%s", %d, %d, %d, "%s", "%s", "%s")' % \
                (table, args['id'], args['name'], admin, tech, registrant,
                 args['creation_date'], args['updated_date'],
                 args['expiration_date'])

            results = self.insertIntoDB(insert_sql)
            if self.status.startswith('Error:'):
                logging.error(self.status)
